// Copyright (c) 2018 Ultimaker B.V.
// Cura is released under the terms of the LGPLv3 or higher.

import QtQuick 2.7
import QtQuick.Controls 2.3

import UM 1.5 as UM
import Cura 1.0 as Cura

ListView
{
    id: listView
    model: Cura.GlobalStacksModel {}
    section.property: "hasRemoteConnection"
    property real contentHeight: childrenRect.height

    ScrollBar.vertical: UM.ScrollBar
    {
        id: scrollBar
    }

    section.delegate: UM.Label
    {
        text: section == "true" ? catalog.i18nc("@label", "Connected printers") : catalog.i18nc("@label", "Preset printers")
        width: parent.width - scrollBar.width
        height: UM.Theme.getSize("action_button").height
        leftPadding: UM.Theme.getSize("default_margin").width
        font: UM.Theme.getFont("medium")
        color: UM.Theme.getColor("text_medium")
    }

    delegate: MachineSelectorButton
    {
        text: model.name ? model.name : ""
        width: listView.width - scrollBar.width
        outputDevice: Cura.MachineManager.printerOutputDevices.length >= 1 ? Cura.MachineManager.printerOutputDevices[0] : null

        checked: Cura.MachineManager.activeMachine ? Cura.MachineManager.activeMachine.id == model.id : false

        onClicked:
        {
            toggleContent()
            Cura.MachineManager.setActiveMachine(model.id)
        }
    }
}
