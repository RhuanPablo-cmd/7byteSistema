# Instale o PyQt5 com: pip install PyQt5

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QMessageBox, QLineEdit
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Telas.ui/menu_principal.ui", self)

        self.nav_buttons = [
            self.btnDashboard,
            self.btnProdutos,
            self.btnEntrada,
            self.btnSaida,
            self.btnRelatorios,
            self.btnConfig,
        ]

        self.btnDashboard.clicked.connect(
            lambda: self.trocar_pagina(self.page_dashboard, self.btnDashboard, "Dashboard")
        )
        self.btnProdutos.clicked.connect(
            lambda: self.trocar_pagina(self.page_produtos, self.btnProdutos, "Produtos")
        )
        self.btnEntrada.clicked.connect(
            lambda: self.trocar_pagina(self.page_entrada, self.btnEntrada, "Entrada de Produto")
        )
        self.btnSaida.clicked.connect(
            lambda: self.trocar_pagina(self.page_saida, self.btnSaida, "Saída de Produto")
        )
        self.btnRelatorios.clicked.connect(
            lambda: self.trocar_pagina(self.page_relatorios, self.btnRelatorios, "Relatório - Movimentações")
        )
        self.btnConfig.clicked.connect(
            lambda: self.trocar_pagina(self.page_config, self.btnConfig, "Configurações")
        )

        self.btnNovoProduto.clicked.connect(
            lambda: self.trocar_pagina(self.page_produtos, self.btnProdutos, "Produtos")
        )
        self.btnSalvarProduto.clicked.connect(
            lambda: self.trocar_pagina(self.page_produtos, self.btnProdutos, "Produtos")
        )

        self.btnCancelarSaida.clicked.connect(
            lambda: self.trocar_pagina(self.page_dashboard, self.btnDashboard, "Dashboard")
        )
        self.btnRegistrarSaida.clicked.connect(
            lambda: self.trocar_pagina(self.page_dashboard, self.btnDashboard, "Dashboard")
        )

        self.btnSair.clicked.connect(self.sair)

        self.trocar_pagina(self.page_dashboard, self.btnDashboard, "Dashboard")

    def trocar_pagina(self, pagina, botao_ativo, titulo):
        self.stackedWidget.setCurrentWidget(pagina)
        self.pageTitleLabel.setText(titulo)

        for btn in self.nav_buttons:
            btn.setChecked(btn is botao_ativo)

    def sair(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("Telas.ui/login.ui", self)

        # Conecta os botões da tela de login
        self.entrarButton.clicked.connect(self.fazer_login)
        self.toggleSenhaButton.clicked.connect(self.alternar_senha)

    def fazer_login(self):
        usuario = self.usuarioLineEdit.text().strip()
        senha = self.senhaLineEdit.text().strip()

        print(f"Usuário: {usuario} | Senha: {senha}")

        if usuario == "Admin" and senha == "1234":
            self.main_window = MainWindow()
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Erro", "Usuário ou senha inválidos.")

    def alternar_senha(self):
        if self.senhaLineEdit.echoMode() == QLineEdit.Password:
            self.senhaLineEdit.setEchoMode(QLineEdit.Normal)
        else:
            self.senhaLineEdit.setEchoMode(QLineEdit.Password)


app = QApplication(sys.argv)

janela = LoginWindow()
janela.show()

sys.exit(app.exec_())


