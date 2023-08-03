# Copyright (c) 2022 Ultimaker B.V.
# Uranium is released under the terms of the LGPLv3 or higher.

from typing import Union, Dict, Optional

from PyQt6.QtCore import QObject, QUrl

from UM.PluginObject import PluginObject


class Stage(QObject, PluginObject):
    """Stages handle combined views in an Uranium application.

    The active stage decides which QML component to show where.
    Uranium has no notion of specific view locations as that's application specific.
    """

    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        self._components: Dict[str, QUrl] = {}
        self._icon_source: QUrl = QUrl()

    def onStageSelected(self) -> None:
        """Something to do when this Stage is selected"""
        pass

    def onStageDeselected(self) -> None:
        """Something to do when this Stage is deselected"""
        pass

    def addDisplayComponent(self, name: str, source: Union[str, QUrl]) -> None:
        """Add a QML component to the stage"""

        if type(source) == str:
            source = QUrl.fromLocalFile(source)
        self._components[name] = source

    def getDisplayComponent(self, name: str) -> QUrl:
        """Get a QUrl by name."""

        if name in self._components:
            return self._components[name]
        return QUrl()
