import csv
import hashlib
import os
import sqlite3
import sys

from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QTableWidgetItem,
    QLineEdit,
    QWidget,
)
from PyQt5 import uic


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASE_PATH = os.path.join(BASE_DIR, "base_dados", "estoque.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "base_dados", "estoque.sql")
UI_DIR = os.path.join(BASE_DIR, "Telas.ui")


class Database:
    def __init__(self):
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
        self.connection = sqlite3.connect(DATABASE_PATH)
        self.connection.row_factory = sqlite3.Row
        with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
            self.connection.executescript(schema_file.read())

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def authenticate(self, username, password):
        return self.connection.execute(
            "SELECT id, username FROM users WHERE username = ? AND password_hash = ? AND active = 1",
            (username, self.hash_password(password)),
        ).fetchone()

    def list_products(self, search=""):
        return self.connection.execute(
            """SELECT id, name, category, unit_price, quantity,
                      unit_price * quantity AS total
               FROM products
               WHERE name LIKE ? OR category LIKE ?
               ORDER BY name""",
            (f"%{search}%", f"%{search}%"),
        ).fetchall()

    def save_product(self, name, category, unit_price, quantity):
        cursor = self.connection.execute(
            "INSERT INTO products (name, category, unit_price, quantity) VALUES (?, ?, ?, ?)",
            (name, category, unit_price, quantity),
        )
        self.connection.commit()
        return cursor.lastrowid

    def product_by_name(self, name):
        return self.connection.execute(
            "SELECT * FROM products WHERE name = ?", (name,)
        ).fetchone()

    def register_movement(self, product_id, movement_type, quantity, movement_date, notes):
        product = self.connection.execute(
            "SELECT quantity, unit_price FROM products WHERE id = ?", (product_id,)
        ).fetchone()
        if product is None:
            raise ValueError("Produto não encontrado.")
        new_quantity = product["quantity"] + quantity if movement_type == "ENTRADA" else product["quantity"] - quantity
        if new_quantity < 0:
            raise ValueError("A saída não pode ser maior que o estoque disponível.")
        with self.connection:
            self.connection.execute(
                "UPDATE products SET quantity = ? WHERE id = ?", (new_quantity, product_id)
            )
            self.connection.execute(
                """INSERT INTO movements
                   (product_id, movement_type, quantity, movement_date, notes)
                   VALUES (?, ?, ?, ?, ?)""",
                (product_id, movement_type, quantity, movement_date, notes),
            )

    def list_movements(self, movement_type, start_date, end_date):
        query = """SELECT m.movement_date, m.movement_type, p.name, p.category,
                          p.unit_price, m.quantity, p.unit_price * m.quantity AS total, m.notes
                   FROM movements m JOIN products p ON p.id = m.product_id
                   WHERE m.movement_date BETWEEN ? AND ?"""
        parameters = [start_date, end_date]
        if movement_type != "Todos":
            query += " AND m.movement_type = ?"
            parameters.append(movement_type.upper())
        query += " ORDER BY m.movement_date DESC, m.id DESC"
        return self.connection.execute(query, parameters).fetchall()


class MainWindow(QMainWindow):
    def __init__(self, database):
        super().__init__()
        self.database = database
        uic.loadUi(os.path.join(UI_DIR, "menu_principal.ui"), self)

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

        self.btnNovoProduto.clicked.connect(self.novo_produto)
        self.btnCancelarCadastro.clicked.connect(self.mostrar_produtos)
        self.btnSalvarProduto.clicked.connect(self.salvar_produto)
        self.btnNovoProdutoEntrada.clicked.connect(self.abrir_cadastro)
        self.btnCancelarEntrada.clicked.connect(self.mostrar_produtos)
        self.btnRegistrarEntrada.clicked.connect(self.registrar_entrada)
        self.btnNovoProdutoSaida.clicked.connect(self.abrir_cadastro)
        self.btnCancelarSaida.clicked.connect(self.mostrar_produtos)
        self.btnRegistrarSaida.clicked.connect(self.registrar_saida)
        self.btnGerarRelatorio.clicked.connect(self.gerar_relatorio)
        self.btnExportarExcel.clicked.connect(self.exportar_relatorio)
        self.btnSalvarConfig.clicked.connect(self.salvar_configuracoes)
        self.buscarProdutoLineEdit.textChanged.connect(self.carregar_produtos)
        self.btnSair.clicked.connect(self.sair)

        self.carregar_produtos()
        self.carregar_combos_produtos()
        self.trocar_pagina(self.page_dashboard, self.btnDashboard, "Dashboard")

    def trocar_pagina(self, pagina, botao_ativo, titulo):
        self.stackedWidget.setCurrentWidget(pagina)
        self.pageTitleLabel.setText(titulo)

        for btn in self.nav_buttons:
            btn.setChecked(btn is botao_ativo)

    def sair(self):
        self.login_window = LoginWindow(self.database)
        self.login_window.show()
        self.close()

    def mostrar_produtos(self):
        self.carregar_produtos()
        self.trocar_pagina(self.page_produtos, self.btnProdutos, "Produtos")

    def abrir_cadastro(self):
        self.trocar_pagina(self.page_cadastro, self.btnProdutos, "Novo Produto")

    def novo_produto(self):
        self.idLineEdit.setText("0")
        self.nomeProdutoLineEdit.clear()
        self.tipoComboBox.setCurrentIndex(0)
        self.valorUnitLineEdit.clear()
        self.qtdInicialLineEdit.clear()
        self.abrir_cadastro()

    def salvar_produto(self):
        name = self.nomeProdutoLineEdit.text().strip()
        category = self.tipoComboBox.currentText()
        price_text = self.valorUnitLineEdit.text().strip().replace(",", ".")
        quantity_text = self.qtdInicialLineEdit.text().strip()
        try:
            price = float(price_text)
            quantity = int(quantity_text)
        except ValueError:
            QMessageBox.warning(self, "Validação", "Informe valor e quantidade numéricos válidos.")
            return
        if not name or category == "Selecione o tipo" or price <= 0 or quantity < 0:
            QMessageBox.warning(self, "Validação", "Preencha todos os campos corretamente.")
            return
        try:
            self.database.save_product(name, category, price, quantity)
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Validação", "Já existe um produto com esse nome.")
            return
        QMessageBox.information(self, "Sucesso", "Produto cadastrado com sucesso.")
        self.carregar_combos_produtos()
        self.mostrar_produtos()

    def carregar_produtos(self):
        products = self.database.list_products(self.buscarProdutoLineEdit.text().strip())
        self.produtosTable.setRowCount(len(products))
        for row_index, product in enumerate(products):
            values = [product["id"], product["name"], product["category"],
                      f'{product["unit_price"]:.2f}', product["quantity"],
                      f'{product["total"]:.2f}', ""]
            for column, value in enumerate(values):
                self.produtosTable.setItem(row_index, column, QTableWidgetItem(str(value)))
        self.totalProdutosLabel.setText(f"Total: {len(products)} produtos")

    def carregar_combos_produtos(self):
        products = self.database.list_products()
        for combo in (self.produtoEntradaComboBox, self.produtoSaidaComboBox):
            combo.clear()
            combo.addItem("Selecione o produto")
            combo.addItems([product["name"] for product in products])

    def registrar_movimento(self, movement_type):
        combo = self.produtoEntradaComboBox if movement_type == "ENTRADA" else self.produtoSaidaComboBox
        quantity_edit = self.qtdEntradaLineEdit if movement_type == "ENTRADA" else self.qtdSaidaLineEdit
        notes_edit = self.obsEntradaTextEdit if movement_type == "ENTRADA" else self.obsSaidaTextEdit
        name = combo.currentText()
        try:
            quantity = int(quantity_edit.text().strip())
        except ValueError:
            QMessageBox.warning(self, "Validação", "Informe uma quantidade inteira válida.")
            return
        if name == "Selecione o produto" or quantity <= 0:
            QMessageBox.warning(self, "Validação", "Selecione um produto e informe uma quantidade maior que zero.")
            return
        product = self.database.product_by_name(name)
        try:
            date_edit = self.dataEntradaDateEdit if movement_type == "ENTRADA" else self.dataSaidaDateEdit
            self.database.register_movement(product["id"], movement_type, quantity,
                                            date_edit.date().toString("yyyy-MM-dd"), notes_edit.toPlainText().strip())
        except ValueError as error:
            QMessageBox.warning(self, "Validação", str(error))
            return
        QMessageBox.information(self, "Sucesso", "Movimentação registrada com sucesso.")
        self.carregar_produtos()
        self.carregar_combos_produtos()
        self.mostrar_produtos()

    def registrar_entrada(self):
        self.registrar_movimento("ENTRADA")

    def registrar_saida(self):
        self.registrar_movimento("SAIDA")

    def gerar_relatorio(self):
        rows = self.database.list_movements(
            self.tipoFiltroComboBox.currentText(),
            self.periodoDeDateEdit.date().toString("yyyy-MM-dd"),
            self.periodoAteDateEdit.date().toString("yyyy-MM-dd"),
        )
        self.relatorioTable.setRowCount(len(rows))
        for row_index, row in enumerate(rows):
            values = [row["movement_date"], row["movement_type"], row["name"], row["category"],
                      f'{row["unit_price"]:.2f}', row["quantity"], f'{row["total"]:.2f}', row["notes"] or ""]
            for column, value in enumerate(values):
                self.relatorioTable.setItem(row_index, column, QTableWidgetItem(str(value)))
        self.totalMovimentacoesLabel.setText(f"Total de Movimentações: {len(rows)}")

    def exportar_relatorio(self):
        self.gerar_relatorio()
        path, _ = QFileDialog.getSaveFileName(self, "Exportar relatório", "relatorio.csv", "CSV (*.csv)")
        if not path:
            return
        with open(path, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=";")
            writer.writerow([self.relatorioTable.horizontalHeaderItem(i).text() for i in range(self.relatorioTable.columnCount())])
            for row in range(self.relatorioTable.rowCount()):
                writer.writerow([self.relatorioTable.item(row, col).text() for col in range(self.relatorioTable.columnCount())])
        QMessageBox.information(self, "Sucesso", "Relatório exportado com sucesso.")

    def salvar_configuracoes(self):
        if not self.nomeSistemaLineEdit.text().strip() or not self.emailAdminLineEdit.text().strip():
            QMessageBox.warning(self, "Validação", "Preencha o nome do sistema e o e-mail do administrador.")
            return
        QMessageBox.information(self, "Sucesso", "Configurações validadas e salvas.")


class LoginWindow(QWidget):
    def __init__(self, database):
        super().__init__()
        self.database = database
        uic.loadUi(os.path.join(UI_DIR, "login.ui"), self)

        # Conecta os botões da tela de login
        self.entrarButton.clicked.connect(self.fazer_login)
        self.toggleSenhaButton.clicked.connect(self.alternar_senha)

    def fazer_login(self):
        usuario = self.usuarioLineEdit.text().strip()
        senha = self.senhaLineEdit.text().strip()

        if not usuario or not senha:
            QMessageBox.warning(self, "Validação", "Informe usuário e senha.")
            return
        if self.database.authenticate(usuario, senha):
            self.main_window = MainWindow(self.database)
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
database = Database()
janela = LoginWindow(database)
janela.show()

sys.exit(app.exec_())
