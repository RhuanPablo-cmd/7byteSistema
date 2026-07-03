# Pessoal baixa o  pip install PyQt5  

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLineEdit
from PyQt5 import uic

# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         uic.loadUi("Telas.ui/menu_principal.ui", self)

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()

        uic.loadUi("Telas.ui/login.ui", self)

        # Conecta os botões às funções
        self.entrarButton.clicked.connect(self.fazer_login)
        self.toggleSenhaButton.clicked.connect(self.alternar_senha)

    def fazer_login(self):
        usuario = self.usuarioLineEdit.text().strip()
        senha = self.senhaLineEdit.text().strip()

        print(f"Usuário: {usuario} | Senha: {senha}")

        if usuario == "Admin" and senha == "1234":
            print("Login OK!")
        else:
            QMessageBox.warning(
                self,
                "Erro",
                "Usuário ou senha inválidos."
            )

    def alternar_senha(self):
        if self.senhaLineEdit.echoMode() == QLineEdit.Password:
            self.senhaLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.senhaLineEdit.setEchoMode(QLineEdit.Password)

    

app = QApplication(sys.argv)

janela = LoginWindow()
janela.show()

sys.exit(app.exec_())


