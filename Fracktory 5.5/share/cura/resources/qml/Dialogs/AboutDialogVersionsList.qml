import QtQuick 2.2
import QtQuick.Controls 2.9

import UM 1.6 as UM
import Cura 1.5 as Cura


ListView
{
    id: projectBuildInfoList
    visible: false
    anchors.top: creditsNotes.bottom
    anchors.topMargin: UM.Theme.getSize("default_margin").height
    width: parent.width
    height: base.height - y - (2 * UM.Theme.getSize("default_margin").height + closeButton.height)

    ScrollBar.vertical: UM.ScrollBar
    {
        id: projectBuildInfoListScrollBar
    }

    delegate: Row
    {
        spacing: UM.Theme.getSize("narrow_margin").width
        UM.Label
        {
            text: (model.name)
            width: (projectBuildInfoList.width* 0.4) | 0
            elide: Text.ElideRight
        }
        UM.Label
        {
            text: (model.version)
            width: (projectBuildInfoList.width *0.6) | 0
            elide: Text.ElideRight
        }

    }
    model: ListModel
    {
        id: developerInfo
    }
    Component.onCompleted:
    {
        var conan_installs = [['boost', '1.82.0'], ['curaengine_grpc_definitions', '0.1.0'], ['zlib', '1.2.13'], ['pyarcus', '5.3.0'], ['curaengine', '5.5.0'], ['pysavitar', '5.3.0'], ['pynest2d', '5.3.0'], ['curaengine_plugin_gradual_flow', '0.1.0'], ['uranium', '5.5.0'], ['cura_binary_data', '5.5.0'], ['cpython', '3.10.4'], ['fdm_materials', '5.5.0'], ['protobuf', '3.21.9'], ['asio-grpc', '2.6.0'], ['grpc', '1.50.1'], ['openssl', '1.1.1l'], ['arcus', '5.3.0'], ['clipper', '6.4.2'], ['rapidjson', '1.1.0'], ['stb', '20200203'], ['spdlog', '1.10.0'], ['fmt', '9.0.0'], ['range-v3', '0.12.0'], ['scripta', '0.1.0'], ['neargye-semver', '0.3.0'], ['savitar', '5.3.0'], ['nest2d', '5.3.0'], ['docopt.cpp', '0.6.3'], ['ctre', '3.7.2'], ['expat', '2.4.1'], ['libffi', '3.2.1'], ['mpdecimal', '2.5.0'], ['libuuid', '1.0.3'], ['libxcrypt', '4.4.25'], ['bzip2', '1.0.8'], ['gdbm', '1.19'], ['sqlite3', '3.36.0'], ['tk', '8.6.10'], ['ncurses', '6.2'], ['xz_utils', '5.2.5'], ['abseil', '20220623.0'], ['c-ares', '1.19.0'], ['re2', '20230301'], ['googleapis', 'cci.20221108'], ['grpc-proto', 'cci.20220627'], ['pugixml', '1.12.1'], ['nlopt', '2.7.0'], ['tcl', '8.6.10'], ['fontconfig', '2.13.93'], ['xorg', 'system'], ['freetype', '2.12.1'], ['libpng', '1.6.37'], ['brotli', '1.0.9']];
        var python_installs = [['certifi', '2023.7.22'], ['setuptools', '65.5.0'], ['pip', '23.3.1'], ['packaging', '23.2'], ['sip', '6.7.12'], ['pyyaml', '6.0.1'], ['tqdm', '4.66.1'], ['ply', '3.11'], ['idna', '3.4'], ['charset-normalizer', '3.3.1'], ['jinja2', '3.1.2'], ['requests', '2.31.0'], ['pygments', '2.16.1'], ['python-dateutil', '2.8.2'], ['pyjwt', '2.8.0'], ['markupsafe', '2.1.3'], ['conan', '1.61.0'], ['urllib3', '1.26.18'], ['patch-ng', '1.17.4'], ['six', '1.16.0'], ['distro', '1.8.0'], ['pluginbase', '1.0.1'], ['fasteners', '0.19'], ['bottle', '0.12.25'], ['node-semver', '0.6.1'], ['colorama', '0.4.6']];
        developerInfo.append({ name : "<H1>Conan Installs</H1>", version : '' });
        for (var n in conan_installs)
        {
            developerInfo.append({ name : conan_installs[n][0], version : conan_installs[n][1] });
        }
        developerInfo.append({ name : '', version : '' });
        developerInfo.append({ name : "<H1>Python Installs</H1>", version : '' });
        for (var n in python_installs)
        {
            developerInfo.append({ name : python_installs[n][0], version : python_installs[n][1] });
        }

    }
}
