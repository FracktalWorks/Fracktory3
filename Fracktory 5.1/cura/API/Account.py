# Copyright (c) 2021 Ultimaker B.V.
# Cura is released under the terms of the LGPLv3 or higher.
import enum
from datetime import datetime
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty, QTimer, pyqtEnum
from typing import Any, Optional, Dict, TYPE_CHECKING, Callable

from UM.Logger import Logger
from UM.Message import Message
from UM.i18n import i18nCatalog
from cura.OAuth2.AuthorizationService import AuthorizationService
from cura.OAuth2.Models import OAuth2Settings, UserProfile
from cura.UltimakerCloud import UltimakerCloudConstants

if TYPE_CHECKING:
    from cura.CuraApplication import CuraApplication

i18n_catalog = i18nCatalog("cura")


class SyncState(enum.IntEnum):
    """QML: Cura.AccountSyncState"""
    SYNCING = 0
    SUCCESS = 1
    ERROR = 2
    IDLE = 3

class Account(QObject):
    """The account API provides a version-proof bridge to use Ultimaker Accounts

    Usage:

    .. code-block:: python

      from cura.API import CuraAPI
      api = CuraAPI()
      api.account.login()
      api.account.logout()
      api.account.userProfile    # Who is logged in
    """

    # The interval in which sync services are automatically triggered
    SYNC_INTERVAL = 60.0  # seconds
    pyqtEnum(SyncState)

    loginStateChanged = pyqtSignal(bool)
    """Signal emitted when user logged in or out"""

    userProfileChanged = pyqtSignal()
    """Signal emitted when new account information is available."""

    additionalRightsChanged = pyqtSignal("QVariantMap")
    """Signal emitted when a users additional rights change"""

    accessTokenChanged = pyqtSignal()
    syncRequested = pyqtSignal()
    """Sync services may connect to this signal to receive sync triggers.
    Services should be resilient to receiving a signal while they are still syncing,
    either by ignoring subsequent signals or restarting a sync.
    See setSyncState() for providing user feedback on the state of your service. 
    """
    lastSyncDateTimeChanged = pyqtSignal()
    syncStateChanged = pyqtSignal(int)  # because SyncState is an int Enum
    manualSyncEnabledChanged = pyqtSignal(bool)
    updatePackagesEnabledChanged = pyqtSignal(bool)

    CLIENT_SCOPES = "account.user.read drive.backup.read drive.backup.write packages.download " \
                    "packages.rating.read packages.rating.write connect.cluster.read connect.cluster.write connect.material.write " \
                    "library.project.read library.project.write cura.printjob.read cura.printjob.write " \
                    "cura.mesh.read cura.mesh.write"

    def __init__(self, application: "CuraApplication", parent = None) -> None:
        super().__init__(parent)
        self._application = application
        self._new_cloud_printers_detected = False

        self._error_message: Optional[Message] = None
        self._logged_in = False
        self._user_profile: Optional[UserProfile] = None
        self._additional_rights: Dict[str, Any] = {}
        self._sync_state = SyncState.IDLE
        self._manual_sync_enabled = False
        self._update_packages_enabled = False
        self._update_packages_action: Optional[Callable] = None
        self._last_sync_str = "-"

        self._callback_port = 32118
        self._oauth_root = UltimakerCloudConstants.CuraCloudAccountAPIRoot

        self._oauth_settings = OAuth2Settings(
            OAUTH_SERVER_URL= self._oauth_root,
            CALLBACK_PORT=self._callback_port,
            CALLBACK_URL="http://localhost:{}/callback".format(self._callback_port),
            CLIENT_ID="um----------------------------ultimaker_cura",
            CLIENT_SCOPES=self.CLIENT_SCOPES,
            AUTH_DATA_PREFERENCE_KEY="general/ultimaker_auth_data",
            AUTH_SUCCESS_REDIRECT="{}/app/auth-success".format(self._oauth_root),
            AUTH_FAILED_REDIRECT="{}/app/auth-error".format(self._oauth_root)
        )

        self._authorization_service = AuthorizationService(self._oauth_settings)

        # Create a timer for automatic account sync
        self._update_timer = QTimer()
        self._update_timer.setInterval(int(self.SYNC_INTERVAL * 1000))
        # The timer is restarted explicitly after an update was processed. This prevents 2 concurrent updates
        self._update_timer.setSingleShot(True)
        self._update_timer.timeout.connect(self.sync)

        self._sync_services: Dict[str, int] = {}
        """contains entries "service_name" : SyncState"""

    def initialize(self) -> None:
        self._authorization_service.initialize(self._application.getPreferences())
        self._authorization_service.onAuthStateChanged.connect(self._onLoginStateChanged)
        self._authorization_service.onAuthenticationError.connect(self._onLoginStateChanged)
        self._authorization_service.accessTokenChanged.connect(self._onAccessTokenChanged)
        self._authorization_service.loadAuthDataFromPreferences()

    @pyqtProperty(int, notify=syncStateChanged)
    def syncState(self):
        return self._sync_state

    def setSyncState(self, service_name: str, state: int) -> None:
        """ Can be used to register sync services and update account sync states

        Contract: A sync service is expected exit syncing state in all cases, within reasonable time

        Example: `setSyncState("PluginSyncService", SyncState.SYNCING)`
        :param service_name: A unique name for your service, such as `plugins` or `backups`
        :param state: One of SyncState
        """
        prev_state = self._sync_state

        self._sync_services[service_name] = state

        if any(val == SyncState.SYNCING for val in self._sync_services.values()):
            self._sync_state = SyncState.SYNCING
            self._setManualSyncEnabled(False)
        elif any(val == SyncState.ERROR for val in self._sync_services.values()):
            self._sync_state = SyncState.ERROR
            self._setManualSyncEnabled(True)
        else:
            self._sync_state = SyncState.SUCCESS
            self._setManualSyncEnabled(False)

        if self._sync_state != prev_state:
            self.syncStateChanged.emit(self._sync_state)

            if self._sync_state == SyncState.SUCCESS:
                self._last_sync_str = datetime.now().strftime("%d/%m/%Y %H:%M")
                self.lastSyncDateTimeChanged.emit()

            if self._sync_state != SyncState.SYNCING:
                # schedule new auto update after syncing completed (for whatever reason)
                if not self._update_timer.isActive():
                    self._update_timer.start()

    def setUpdatePackagesAction(self, action: Callable) -> None:
        """ Set the callback which will be invoked when the user clicks the update packages button

        Should be invoked after your service sets the sync state to SYNCING and before setting the
        sync state to SUCCESS.

        Action will be reset to None when the next sync starts
        """
        self._update_packages_action = action
        self._update_packages_enabled = True
        self.updatePackagesEnabledChanged.emit(self._update_packages_enabled)

    def _onAccessTokenChanged(self):
        self.accessTokenChanged.emit()

    @property
    def is_staging(self) -> bool:
        """Indication whether the given authentication is applied against staging or not."""

        return "staging" in self._oauth_root

    @pyqtProperty(bool, notify=loginStateChanged)
    def isLoggedIn(self) -> bool:
        return self._logged_in

    def _onLoginStateChanged(self, logged_in: bool = False, error_message: Optional[str] = None) -> None:
        if error_message:
            if self._error_message:
                self._error_message.hide()
            Logger.log("w", "Failed to login: %s", error_message)
            self._error_message = Message(error_message,
                                          title = i18n_catalog.i18nc("@info:title", "Login failed"),
                                          message_type = Message.MessageType.ERROR)
            self._error_message.show()
            self._logged_in = False
            self.loginStateChanged.emit(False)
            if self._update_timer.isActive():
                self._update_timer.stop()
            return

        if self._logged_in != logged_in:
            self._logged_in = logged_in
            self.loginStateChanged.emit(logged_in)
            if logged_in:
                self._authorization_service.getUserProfile(self._onProfileChanged)
                self._setManualSyncEnabled(False)
                self._sync()
            else:
                if self._update_timer.isActive():
                    self._update_timer.stop()

    def _onProfileChanged(self, profile: Optional[UserProfile]) -> None:
        self._user_profile = profile
        self.userProfileChanged.emit()

    def _sync(self) -> None:
        """Signals all sync services to start syncing

        This can be considered a forced sync: even when a
        sync is currently running, a sync will be requested.
        """

        self._update_packages_action = None
        self._update_packages_enabled = False
        self.updatePackagesEnabledChanged.emit(self._update_packages_enabled)
        if self._update_timer.isActive():
            self._update_timer.stop()
        elif self._sync_state == SyncState.SYNCING:
            Logger.debug("Starting a new sync while previous sync was not completed")

        self.syncRequested.emit()

    def _setManualSyncEnabled(self, enabled: bool) -> None:
        if self._manual_sync_enabled != enabled:
            self._manual_sync_enabled = enabled
            self.manualSyncEnabledChanged.emit(enabled)

    @pyqtSlot()
    @pyqtSlot(bool)
    def login(self, force_logout_before_login: bool = False) -> None:
        """
        Initializes the login process. If the user is logged in already and force_logout_before_login is true, Cura will
        logout from the account before initiating the authorization flow. If the user is logged in and
        force_logout_before_login is false, the function will return, as there is nothing to do.

        :param force_logout_before_login: Optional boolean parameter
        :return: None
        """
        if self._logged_in:
            if force_logout_before_login:
                self.logout()
            else:
                # Nothing to do, user already logged in.
                return
        self._authorization_service.startAuthorizationFlow(force_logout_before_login)

    @pyqtProperty(str, notify = userProfileChanged)
    def userName(self):
        if not self._user_profile:
            return ""
        return self._user_profile.username

    @pyqtProperty(str, notify = userProfileChanged)
    def profileImageUrl(self):
        if not self._user_profile:
            return ""
        return self._user_profile.profile_image_url

    @pyqtProperty(str, notify=accessTokenChanged)
    def accessToken(self) -> Optional[str]:
        return self._authorization_service.getAccessToken()

    @pyqtProperty("QVariantMap", notify = userProfileChanged)
    def userProfile(self) -> Dict[str, Optional[str]]:
        """None if no user is logged in otherwise the logged in  user as a dict containing containing user_id, username and profile_image_url """
        if not self._user_profile:
            return {}
        return self._user_profile.__dict__

    @pyqtProperty(str, notify=lastSyncDateTimeChanged)
    def lastSyncDateTime(self) -> str:
        return self._last_sync_str

    @pyqtProperty(bool, notify=manualSyncEnabledChanged)
    def manualSyncEnabled(self) -> bool:
        return self._manual_sync_enabled

    @pyqtProperty(bool, notify=updatePackagesEnabledChanged)
    def updatePackagesEnabled(self) -> bool:
        return self._update_packages_enabled

    @pyqtSlot()
    @pyqtSlot(bool)
    def sync(self, user_initiated: bool = False) -> None:
        if user_initiated:
            self._setManualSyncEnabled(False)

        self._sync()

    @pyqtSlot()
    def onUpdatePackagesClicked(self) -> None:
        if self._update_packages_action is not None:
            self._update_packages_action()

    @pyqtSlot()
    def popupOpened(self) -> None:
        self._setManualSyncEnabled(True)

    @pyqtSlot()
    def logout(self) -> None:
        if not self._logged_in:
            return  # Nothing to do, user isn't logged in.

        self._authorization_service.deleteAuthData()

    def updateAdditionalRight(self, **kwargs) -> None:
        """Update the additional rights of the account.
        The argument(s) are the rights that need to be set"""
        self._additional_rights.update(kwargs)
        self.additionalRightsChanged.emit(self._additional_rights)

    @pyqtProperty("QVariantMap", notify = additionalRightsChanged)
    def additionalRights(self) -> Dict[str, Any]:
        """A dictionary which can be queried for additional account rights."""
        return self._additional_rights
