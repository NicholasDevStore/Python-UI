from PySide2 import QtWidgets
import getpass
from datetime import datetime
import re
    
class MyWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
 
        super(MyWidget, self).__init__(parent)

        mainLayout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel("Share Password Locally")
        mainLayout.addWidget(self.label)

        hCredentialLayout = QtWidgets.QHBoxLayout() #Credentials
        self.credentialLabel = QtWidgets.QLabel("Share theses credentials with (Superhero name)")
        self.credentialCombo = QtWidgets.QComboBox()
        self.credentialCombo.setObjectName('_RECIPIENT_')
        initText = ['user1', 'user2', 'user3', 'user4', 'user5', 'user6', 'user7', 'group1', 'group2', 'group3', 'everyone']
        self.credentialCombo.addItems(initText)

        hCredentialLayout.addWidget(self.credentialLabel)
        hCredentialLayout.addWidget(self.credentialCombo)
        mainLayout.addLayout(hCredentialLayout)
        
        hTitleLayout = QtWidgets.QHBoxLayout() #Site Title
        self.titleLabel = QtWidgets.QLabel("Site Title:")
        self.titleLine = QtWidgets.QLineEdit()
        self.credentialCombo.setObjectName('_TITLE_')
        hTitleLayout.addWidget(self.titleLabel)
        hTitleLayout.addWidget(self.titleLine)
        mainLayout.addLayout(hTitleLayout)

        hUrlLayout = QtWidgets.QHBoxLayout() #Site URL
        self.urlLabel = QtWidgets.QLabel("Site Title:")
        self.urlLine = QtWidgets.QLineEdit('https://')
        self.urlLine.setObjectName('_URL_')
        hUrlLayout.addWidget(self.urlLabel)
        hUrlLayout.addWidget(self.urlLine)
        mainLayout.addLayout(hUrlLayout)

        hEmailLayout = QtWidgets.QHBoxLayout() #Acct email
        self.emailLabel = QtWidgets.QLabel("Acct email:")
        self.emailLine = QtWidgets.QLineEdit('account@example.org')
        self.emailLine.setObjectName('_EMAIL_')
        hEmailLayout.addWidget(self.emailLabel)
        hEmailLayout.addWidget(self.emailLine)
        mainLayout.addLayout(hEmailLayout)

        hUsernameLayout = QtWidgets.QHBoxLayout() #Username
        self.userNameLabel = QtWidgets.QLabel("Username:")
        self.userNameLine = QtWidgets.QLineEdit()
        self.userNameLine.setObjectName('_USERNAME_')
        hUsernameLayout.addWidget(self.userNameLabel)
        hUsernameLayout.addWidget(self.userNameLine)
        mainLayout.addLayout(hUsernameLayout)

        hPasswordLayout = QtWidgets.QHBoxLayout() #Password
        self.passwordLabel = QtWidgets.QLabel("Password:")
        self.passwordLine = QtWidgets.QLineEdit('use HSXKPasswd to create one if needed')
        # self.passwordLine.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)
        self.passwordLine.setObjectName('_PASSWORD_')
        hPasswordLayout.addWidget(self.passwordLabel)
        hPasswordLayout.addWidget(self.passwordLine)
        mainLayout.addLayout(hPasswordLayout)

        hNotesLayout = QtWidgets.QHBoxLayout() #Notes
        self.notesLabel = QtWidgets.QLabel("Notes:")
        self.notesEdit = QtWidgets.QTextEdit()
        self.notesEdit.setObjectName('_NOTES_')
        hNotesLayout.addWidget(self.notesLabel)
        hNotesLayout.addWidget(self.notesEdit)
        mainLayout.addLayout(hNotesLayout)

        hButtonLayout = QtWidgets.QHBoxLayout()
        self.saveButton = QtWidgets.QPushButton("Save")
        self.exitButton = QtWidgets.QPushButton("Exit")
        hButtonLayout.addWidget(self.saveButton)
        hButtonLayout.addWidget(self.exitButton)
        mainLayout.addLayout(hButtonLayout)

        self.saveButton.clicked.connect(self.saveCredential)
        self.exitButton.clicked.connect(self.exitButtonClick)
        
        self.setLayout(mainLayout)
        self.setWindowTitle("Share Password Locally")
    
    def exitButtonClick(self):

        self.close()

    def cleanup(self, string):

        return re.sub(r'\W+', '_', string)

    def saveCredential(self):

        basepath = '/path/to/encrypted/volume'
        title = self.titleLine.text()
        mytimestamp = self.cleanup( datetime.today().strftime('%Y-%m-%d-%H:%M:%S') )
        fullpath = basepath + "/" + self.credentialCombo.currentText() + "/" + self.cleanup(title) + "_" + mytimestamp + ".txt"

        sharedby = getpass.getuser()

        output_text = "[Title:]\t%s\n[Shared by:]\t%s\n[URL:]\t\t%s\n[Accnt email:]\t%s\n[Username:]\t%s\n[Password:]\t%s\n[Notes:]\n%s\n[Date:]\t%s\n" % (title, sharedby, self.urlLine.text(), self.emailLine.text(), self.userNameLine.text(), self.passwordLine.text(), self.notesEdit.toPlainText(), mytimestamp)

        output_file = open(fullpath, 'w')
        output_file.write(output_text)
        output_file.close()

        msgBox = QtWidgets.QMessageBox();
        msgBox.setText("Saved");
        msgBox.exec();


if __name__ == '__main__':

    import sys

    app = QtWidgets.QApplication(sys.argv)

    wid = MyWidget()
    wid.show()

    sys.exit(app.exec_())