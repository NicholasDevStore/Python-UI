import QtQuick 2.0
import QtQuick.Layouts 1.14
import QtQuick.Controls 2.14
import QtQuick.Dialogs 1.1

Item {
    id: root
    readonly property int default_margin: 5
    property var initComboText: ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'group1', 'group2', 'group3', 'everyone']

    signal close_clicked()
    signal save_clicked(string cre, string title, string url, string email, string username, string password, string notes)

    function showMessageDialog() {
        messageDialog.open()
    }

    MessageDialog {
        id: messageDialog
        title: "Information"
        icon: StandardIcon.Information
        text: "Saved"
        standardButtons: StandardButton.Ok
    }

    width: 500
    height: 600
    ColumnLayout {

        anchors.fill: parent
        anchors.margins: 10
        spacing: 6

        Label {
            Layout.alignment: Qt.AlignLeft
            horizontalAlignment: Qt.AlignLeft
            verticalAlignment: Qt.AlignVCenter
            text: qsTr('Share Password Locally')
        }

        RowLayout {

            Layout.fillWidth: true
            Label {
                Layout.alignment: Qt.AlignLeft
                horizontalAlignment: Qt.AlignLeft
                verticalAlignment: Qt.AlignVCenter
                text: qsTr('Share these credentials with (Superhero name)')
            }

            ComboBox {
                id: credentialCombo
                editable: false                
                model: initComboText
                KeyNavigation.tab: siteTitleInput
            }
        }

        RowLayout {

            Layout.fillWidth: true
            Layout.preferredHeight: 30
            Layout.margins: default_margin

            Label {
                Layout.alignment: Qt.AlignLeft
                horizontalAlignment: Qt.AlignLeft
                verticalAlignment: Qt.AlignVCenter
                text: qsTr('Site Title:')
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height
                Layout.alignment: Qt.AlignVCenter

                border {
                    width: 1
                    color: "#ACACAC"
                }

                TextInput {
                    id: siteTitleInput

                    anchors {
                        fill: parent
                        verticalCenter: parent.verticalCenter
                        margins: default_margin
                    }

                    height: parent.height - 2 * parent.border.width
                    width: parent.width - 2 * parent.border.width

                    font {
                        family: qsTr("Segoe UI")
                        pointSize: 12
                    }

                    KeyNavigation.tab: siteUrlInput
                    clip: true
                    text: qsTr("https://www.example.com")
                }
            }
        }

        RowLayout {

            Layout.fillWidth: true
            Layout.preferredHeight: 30
            Layout.margins: default_margin

            Label {
                Layout.alignment: Qt.AlignLeft
                horizontalAlignment: Qt.AlignLeft
                verticalAlignment: Qt.AlignVCenter
                text: qsTr('Site URL:')
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height
                Layout.alignment: Qt.AlignVCenter

                border {
                    width: 1
                    color: "#ACACAC"
                }

                TextInput {
                    id: siteUrlInput

                    anchors {
                        fill: parent
                        verticalCenter: parent.verticalCenter
                        margins: default_margin
                    }
                    height: parent.height - 2 * parent.border.width
                    width: parent.width - 2 * parent.border.width

                    font {
                        family: qsTr("Segoe UI")
                        pointSize: 12
                    }

                    KeyNavigation.tab: acctEmailInput
                    clip: true
                    text: qsTr("https://")
                }
            }
        }

        RowLayout {

            Layout.fillWidth: true
            Layout.preferredHeight: 30
            Layout.margins: default_margin

            Label {
                Layout.alignment: Qt.AlignLeft
                horizontalAlignment: Qt.AlignLeft
                verticalAlignment: Qt.AlignVCenter
                text: qsTr('Acct email:')
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height
                Layout.alignment: Qt.AlignVCenter

                border {
                    width: 1
                    color: "#ACACAC"
                }

                TextInput {
                    id: acctEmailInput

                    anchors {
                        fill: parent
                        verticalCenter: parent.verticalCenter
                        margins: default_margin
                    }
                    height: parent.height - 2 * parent.border.width
                    width: parent.width - 2 * parent.border.width

                    font {
                        family: qsTr("Segoe UI")
                        pointSize: 12
                    }

                    KeyNavigation.tab: usernameInput
                    clip: true
                    text: qsTr("account@example.org")
                }
            }
        }

        RowLayout {

            Layout.fillWidth: true
            Layout.preferredHeight: 30
            Layout.margins: default_margin

            Label {
                Layout.alignment: Qt.AlignLeft
                horizontalAlignment: Qt.AlignLeft
                verticalAlignment: Qt.AlignVCenter
                text: qsTr('Username:')
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height
                Layout.alignment: Qt.AlignVCenter

                border {
                    width: 1
                    color: "#ACACAC"
                }

                TextInput {
                    id: usernameInput

                    anchors {
                        fill: parent
                        verticalCenter: parent.verticalCenter
                        margins: default_margin
                    }
                    height: parent.height - 2 * parent.border.width
                    width: parent.width - 2 * parent.border.width

                    font {
                        family: qsTr("Segoe UI")
                        pointSize: 12
                    }

                    KeyNavigation.tab: passwdInput
                    clip: true
                    text: qsTr("")
                }
            }
        }

        RowLayout {

            Layout.fillWidth: true
            Layout.preferredHeight: 30
            Layout.margins: default_margin

            Label {
                Layout.alignment: Qt.AlignLeft
                horizontalAlignment: Qt.AlignLeft
                verticalAlignment: Qt.AlignVCenter
                text: qsTr('Password:')
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: parent.height
                Layout.alignment: Qt.AlignVCenter

                border {
                    width: 1
                    color: "#ACACAC"
                }

                TextInput {
                    id: passwdInput

                    anchors {
                        fill: parent
                        verticalCenter: parent.verticalCenter
                        margins: default_margin
                    }
                    height: parent.height - 2 * parent.border.width
                    width: parent.width - 2 * parent.border.width

                    font {
                        family: qsTr("Segoe UI")
                        pointSize: 12
                    }
                    passwordCharacter: "*"

                    KeyNavigation.tab: notesEdit
                    clip: true
                    text: qsTr("use HSXKPasswd to create one if needed")

                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.preferredHeight: 260
            Layout.margins: default_margin

            Label {
                Layout.alignment: Qt.AlignLeft
                horizontalAlignment: Qt.AlignLeft
                verticalAlignment: Qt.AlignVCenter
                text: qsTr('Notes:')
            }

            Rectangle {
                Layout.fillWidth: true
                Layout.preferredHeight: 250
                Layout.alignment: Qt.AlignVCenter

                border {
                    width: 1
                    color: "#ACACAC"
                }

                TextEdit {
                    id: notesEdit

                    anchors {
                        fill: parent
                        verticalCenter: parent.verticalCenter
                        margins: default_margin
                    }
                    height: parent.height - 2 * parent.border.width
                    width: parent.width - 2 * parent.border.width

                    font {
                        family: qsTr("Segoe UI")
                        pointSize: 12
                    }

                    KeyNavigation.tab: saveButton
                    clip: true
                    wrapMode: TextEdit.Wrap
                    text: qsTr("")
                }
            }
        }

        RowLayout {
            Layout.fillWidth: true
            spacing: 15

            Button {
                id: saveButton
                Layout.fillWidth: true
                Layout.preferredHeight: 30
                Layout.alignment: Qt.AlignVCenter

                text: qsTr("Save")

                onClicked: {

                    console.log(qsTr("Site Title: %1").arg(siteTitleInput.text))
                    console.log(qsTr("Site Url: %1").arg(siteUrlInput.text))
                    console.log(qsTr("Acct Email: %1").arg(acctEmailInput.text))
                    console.log(qsTr("Username: %1").arg(usernameInput.text))
                    console.log(qsTr("Password: %1").arg(passwdInput.text))
                    save_clicked(credentialCombo.currentText, siteTitleInput.text, siteUrlInput.text, acctEmailInput.text, usernameInput.text, passwdInput.text, notesEdit.text)
                }
            }

            Button {
                Layout.fillWidth: true
                Layout.preferredHeight: 30
                Layout.alignment: Qt.AlignVCenter

                text: qsTr("Exit")

                onClicked: {
                    close_clicked()
                }
            }
        }
    }
}
