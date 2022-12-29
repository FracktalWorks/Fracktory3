# Uranium is released under the terms of the LGPLv3 or higher.

import codecs
import json
import platform

import urllib.request



from UM.Application import Application
from UM.Job import Job
from UM.Logger import Logger
from UM.Message import Message
from UM.Version import Version
from UM.i18n import i18nCatalog

i18n_catalog = i18nCatalog("uranium")


class UpdateCheckerJob(Job):
    """This job checks if there is an update available on the provided URL."""

    def __init__(self, silent = False, display_same_version = True, url = None, callback = None, set_download_url_callback = None):
        super().__init__()
        self.silent = silent
        self.display_same_version = display_same_version
        self._url = url
        self._callback = callback
        self._set_download_url_callback = set_download_url_callback

    def run(self):
        if not self._url:
            Logger.log("e", "Can not check for a new release. URL not set!")
        no_new_version = True

        application_name = Application.getInstance().getApplicationName()
        Logger.log("i", "Checking for new version of %s" % application_name)
        try:
            headers = {"User-Agent": "%s - %s" % (application_name, Application.getInstance().getVersion())}
            request = urllib.request.Request(self._url, headers = headers)
            latest_version_file = urllib.request.urlopen(request)
        except Exception as e:
            Logger.log("w", "Failed to check for new version: %s" % e)
            if not self.silent:
                Message(i18n_catalog.i18nc("@info", "Could not access update information."),
                    title = i18n_catalog.i18nc("@info:title", "Version Upgrade")
                ).show()
            return

        try:
            reader = codecs.getreader("utf-8")
            data = json.load(reader(latest_version_file))
            try:
                if Application.getInstance().getVersion() != "master":
                    local_version = Version(Application.getInstance().getVersion())
                else:
                    if not self.silent:
                        Message(i18n_catalog.i18nc("@info", "The version you are using does not support checking for updates."), title = i18n_catalog.i18nc("@info:title", "Warning")).show()
                    return
            except ValueError:
                Logger.log("w", "Could not determine application version from string %s, not checking for updates", Application.getInstance().getVersion())
                if not self.silent:
                    Message(i18n_catalog.i18nc("@info", "The version you are using does not support checking for updates."), title = i18n_catalog.i18nc("@info:title", "Version Upgrade")).show()
                return

            latest_version_array = data["tag_name"].split("v")[1].split(".")
            latest_version = Version(list(map(int, latest_version_array)))
            if local_version < latest_version:
                Logger.log("i", "Found a new version of the software. Spawning message")
                message = Message(i18n_catalog.i18nc("@info", "A new version is available!"),
                                  title=i18n_catalog.i18nc("@info:title", "Version Upgrade"))
                message.addAction("download", i18n_catalog.i18nc("@action:button", "Download"), "[no_icon]", "[no_description]")
                browser_download_url = ""
                if self._set_download_url_callback:
                    for asset in data["assets"]:
                        os = "Windows" if ".exe" in asset["name"] else "Darwin" if ".dmg" in asset["name"] else "Linux"
                        if os == platform.system():
                            browser_download_url = asset["browser_download_url"]
                            break
                    self._set_download_url_callback(browser_download_url)
                message.actionTriggered.connect(self._callback)
                message.show()
                no_new_version = False

        except Exception:
            Logger.logException("e", "Exception in update checker while parsing the JSON file.")
            Message(i18n_catalog.i18nc("@info", "An error occurred while checking for updates."), title = i18n_catalog.i18nc("@info:title", "Error")).show()
            no_new_version = False  # Just to suppress the message below.

        if no_new_version and not self.silent:
            Message(i18n_catalog.i18nc("@info", "No new version was found."), title = i18n_catalog.i18nc("@info:title", "Version Upgrade")).show()
