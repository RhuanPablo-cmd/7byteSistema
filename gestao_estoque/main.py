import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Telas.ui/login.ui", self)
        self.entrarButton.clicked.connect(self.fazer_login)
        
    def fazer_login(self):
        print("Botão Clicado!")
    
    def fazer_login(self):
        usuario = self.usuarioLineEdit.text()
        senha = self.senhaLineEdit.text()
        print(f"Usuário: {usuario} | Senha: {senha}")
        
    def fazer_login(self):
        usuario = self.usuarioLineEdit.text().strip()
        senha = self.senhaLineEdit.text().strip()
        
        if usuario == "Admin" and senha == "1234":
            print("Login OK!")
        else: 
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidas.")
        
app = QApplication(sys.argv)
janela = LoginWindow()
janela.show()
sys.exit(app.exec_())