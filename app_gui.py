import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QRadioButton, QSpinBox, QGroupBox, QFormLayout,
    QMessageBox, QTextEdit
)
from PyQt6.QtGui import QFont, QIcon
from PyQt6.QtCore import Qt
from decimal import Decimal, InvalidOperation

# Importa a lógica de cálculo do outro arquivo
import main as cl  # cl = calculadora


# Estilo da aplicação (CSS para PyQt) com melhor contraste
STYLESHEET = """
QWidget {
    background-color: #F8F7FA;
    color: #2C3E50;
    font-family: 'Inter', 'SF Pro Display', 'Segoe UI Variable', 'Segoe UI', system-ui, -apple-system, sans-serif;
    font-size: 11pt;
    font-weight: 400;
}
QTabWidget::pane {
    border: 1px solid #EAECEE;
    border-radius: 8px;
}
QTabBar::tab {
    background: #F2F3F4;
    color: #5D6D7E;
    padding: 12px 28px;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    border: 1px solid #EAECEE;
    border-bottom: none;
    font-weight: 500;
    font-size: 11pt;
}
QTabBar::tab:selected {
    background: #A569BD; /* Roxo com mais contraste */
    color: #FFFFFF;
}
QGroupBox {
    font-weight: 600;
    color: #8E44AD; /* Título do grupo mais escuro para legibilidade */
    border: 1px solid #D5DBDB;
    border-radius: 8px;
    margin-top: 1ex;
    padding: 10px;
    font-size: 11pt;
}
QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top center;
    padding: 0 10px;
}
QLabel {
    color: #34495E;
    font-weight: 400;
    font-size: 11pt;
}
QLineEdit, QSpinBox, QTextEdit {
    background-color: #FFFFFF;
    border: 1px solid #D5DBDB;
    padding: 10px;
    border-radius: 6px;
    font-weight: 400;
    font-size: 11pt;
}
QLineEdit:focus, QSpinBox:focus, QTextEdit:focus {
    border: 2px solid #A569BD; /* Cor de foco correspondente */
}
QLineEdit[readOnly="true"] {
    background-color: #F2F3F4;
    color: #5D6D7E;
}
QPushButton {
    background-color: #A569BD; /* Roxo com mais contraste */
    color: #FFFFFF;
    border: none;
    padding: 12px 18px;
    border-radius: 6px;
    font-weight: 500;
    font-size: 11pt;
    outline: none;
}
QPushButton:hover {
    background-color: #AF7AC5; /* Tom mais claro para hover */
}
QPushButton:pressed {
    background-color: #8E44AD; /* Tom mais escuro para pressionado */
}
QRadioButton {
    padding: 5px;
    font-weight: 400;
    font-size: 11pt;
}
QRadioButton::indicator {
    width: 18px;
    height: 18px;
}
QRadioButton::indicator:unchecked {
    background-color: #FFFFFF;
    border: 2px solid #BDC3C7;
    border-radius: 9px;
}
QRadioButton::indicator:checked {
    background-color: #A569BD; /* Cor de seleção correspondente */
    border: 2px solid #8E44AD;
    border-radius: 9px;
}
"""

# Classe principal da interface gráfica
# Herda de QWidget (classe base para elementos visuais)
class CalculadoraErrosGUI(QWidget):
    def __init__(self):
        super().__init__()  # Inicializa QWidget (janela básica)
        self.setWindowTitle("Calculadora de Erros Numéricos")
        self.setWindowIcon(QIcon("calculator.png")) 
        self.setGeometry(100, 100, 700, 650)  # Posição e tamanho da janela

        # Layout principal - organiza elementos verticalmente
        main_layout = QVBoxLayout()  # VBox = Vertical Box Layout
        self.setLayout(main_layout)

        # Sistema de abas (como abas do navegador)
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Criar e adicionar as abas
        self.tab_calculadora = QWidget()  # Widget para a primeira aba
        self.tab_simulacao = QWidget()    # Widget para a segunda aba
        tabs.addTab(self.tab_calculadora, "  Calculadora Padrão  ")
        tabs.addTab(self.tab_simulacao, "  Simulação de Propagação de Erros  ")

        # Configurar a interface de cada aba
        self.init_calculadora_ui()  # Cria elementos da calculadora
        self.init_simulacao_ui()    # Cria elementos da simulação

    # Cria a interface da aba "Calculadora Padrão"
    def init_calculadora_ui(self):
        layout = QVBoxLayout(self.tab_calculadora)  # Layout vertical para esta aba

        # Grupo de entradas - caixa com título que agrupa campos relacionados
        input_group = QGroupBox("Entradas")
        input_layout = QFormLayout()  # Layout em pares: rótulo + campo
        
        # Campos de entrada
        self.calc_n1 = QLineEdit("0.1")  # Campo de texto com valor padrão
        self.calc_n2 = QLineEdit("0.2")
        self.calc_digitos = QSpinBox()  # Campo numérico com setas
        self.calc_digitos.setRange(1, 50)  # Define faixa de valores
        self.calc_digitos.setValue(4)     # Valor padrão

        input_layout.addRow(QLabel("Valor 1:"), self.calc_n1)
        input_layout.addRow(QLabel("Valor 2:"), self.calc_n2)
        input_layout.addRow(QLabel("Dígitos de Precisão:"), self.calc_digitos)
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)

        # Grupo de método de precisão
        metodo_group = QGroupBox("Método de Precisão")
        metodo_layout = QHBoxLayout()  # Layout horizontal (lado a lado)
        self.calc_trunc = QRadioButton("Truncamento")  # Botão de rádio (só pode escolher um)
        self.calc_arred = QRadioButton("Arredondamento")
        self.calc_arred.setChecked(True)  # Arredondamento fica selecionado por padrão
        metodo_layout.addWidget(self.calc_trunc)
        metodo_layout.addWidget(self.calc_arred)
        metodo_group.setLayout(metodo_layout)
        layout.addWidget(metodo_group)

        # Grupo de operações - botões para as operações matemáticas
        op_group = QGroupBox("Operação")
        op_layout = QHBoxLayout()  # Botões lado a lado
        ops = ['+', '-', '*', '/']  # Lista das operações
        for op in ops:
            btn = QPushButton(op)  # Cria botão com símbolo da operação
            btn.setFixedWidth(60)  # Largura fixa para todos os botões
            # Conecta o clique ao método calcular (lambda captura o valor de op)
            btn.clicked.connect(lambda checked, o=op: self.calcular(o))
            op_layout.addWidget(btn)
        op_group.setLayout(op_layout)
        layout.addWidget(op_group)

        # Grupo de resultados - campos somente leitura para mostrar resultados
        result_group = QGroupBox("Resultados")
        result_layout = QFormLayout()
        # Campos para mostrar os resultados
        self.calc_valor1_aprox = QLineEdit()  # Primeiro valor com precisão aplicada
        self.calc_valor2_aprox = QLineEdit()  # Segundo valor com precisão aplicada
        self.calc_res_exato = QLineEdit()     # Resultado exato (sem limitação)
        self.calc_res_aprox = QLineEdit()     # Resultado aproximado (com limitação)
        self.calc_erro_abs = QLineEdit()      # Erro absoluto
        self.calc_erro_rel = QLineEdit()      # Erro relativo
        
        # Torna todos os campos de resultado somente leitura
        for field in [self.calc_valor1_aprox, self.calc_valor2_aprox, self.calc_res_exato, self.calc_res_aprox, self.calc_erro_abs, self.calc_erro_rel]:
            field.setReadOnly(True)

        result_layout.addRow(QLabel("Primeiro Valor Ajustado:"), self.calc_valor1_aprox)
        result_layout.addRow(QLabel("Segundo Valor Ajustado:"), self.calc_valor2_aprox)
        result_layout.addRow(QLabel("Resultado Exato:"), self.calc_res_exato)
        result_layout.addRow(QLabel("Resultado Aproximado:"), self.calc_res_aprox)
        result_layout.addRow(QLabel("Erro Absoluto:"), self.calc_erro_abs)
        result_layout.addRow(QLabel("Erro Relativo (%):"), self.calc_erro_rel)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)
        
        layout.addStretch()  # Empurra todos os elementos para o topo

    # Executa o cálculo quando um botão de operação é clicado
    def calcular(self, op_str):
        try:
            # Pega os valores dos campos e converte para Decimal
            n1 = Decimal(self.calc_n1.text())
            n2 = Decimal(self.calc_n2.text())
            dig = self.calc_digitos.value()
            
            # Escolhe a função de precisão baseada no botão selecionado
            met_funcao = cl.truncamento_corrigido if self.calc_trunc.isChecked() else cl.arredondamento_corrigido
            
            # Verifica se a operação é válida
            if op_str not in cl.operacoes:
                QMessageBox.critical(self, "Erro de Operação", f"Operação '{op_str}' não é válida.")
                return
                
            op_funcao = cl.operacoes[op_str]  # Pega a função da operação

            # Aplica precisão limitada aos números de entrada
            valor1_aprox = met_funcao(n1, dig)
            valor2_aprox = met_funcao(n2, dig)
            
            # Calcula resultado exato (sem limitação) e aproximado (com limitação)
            resultado_exato = op_funcao(n1, n2)
            resultado_aprox = op_funcao(valor1_aprox, valor2_aprox)

            # Calcula os erros
            erro_abs = cl.erroAbs(resultado_aprox, resultado_exato)
            erro_rel = cl.erroRel(resultado_aprox, resultado_exato)
            
            # Atualiza os campos de resultado na interface
            self.calc_valor1_aprox.setText(f"{valor1_aprox}")
            self.calc_valor2_aprox.setText(f"{valor2_aprox}")
            self.calc_res_exato.setText(f"{resultado_exato}")
            self.calc_res_aprox.setText(f"{resultado_aprox}")
            self.calc_erro_abs.setText(f"{erro_abs}")
            
            # Formata o erro relativo como porcentagem
            if erro_rel.is_finite():
                # Remove zeros desnecessários da formatação
                erro_rel_formatado = f"{(erro_rel * 100):.10f}".rstrip('0').rstrip('.')
                self.calc_erro_rel.setText(f"{erro_rel_formatado}%")
            else:
                self.calc_erro_rel.setText("Infinito")

        # Tratamento de erros com mensagens amigáveis
        except InvalidOperation:
            QMessageBox.critical(self, "Erro de Entrada", "Por favor, insira valores numéricos válidos.")
        except ValueError:
            QMessageBox.critical(self, "Erro de Entrada", "Por favor, insira valores numéricos válidos.")
        except ZeroDivisionError:
            QMessageBox.critical(self, "Erro de Divisão", "Não é possível dividir por zero.")
        except Exception as e:
            QMessageBox.critical(self, "Erro Inesperado", f"Ocorreu um erro: {e}")

    # Cria a interface da aba "Simulação de Propagação"
    def init_simulacao_ui(self):
        layout = QVBoxLayout(self.tab_simulacao)  # Layout vertical para esta aba

        # Grupo de parâmetros da simulação
        params_group = QGroupBox("Parâmetros da Simulação")
        params_layout = QFormLayout()

        # Campos para configurar a simulação
        self.sim_valor = QLineEdit("0.0001")  # Valor a ser somado repetidamente
        self.sim_vezes = QSpinBox()  # Quantas vezes somar
        self.sim_vezes.setRange(1, 100000)  # De 1 a 100.000 somas
        self.sim_vezes.setValue(100)        # Padrão: 100 somas
        self.sim_digitos = QSpinBox()  # Dígitos de precisão
        self.sim_digitos.setRange(1, 50)
        self.sim_digitos.setValue(3)         # Padrão: 3 dígitos

        params_layout.addRow(QLabel("Valor a ser somado:"), self.sim_valor)
        params_layout.addRow(QLabel("Número de somas:"), self.sim_vezes)
        params_layout.addRow(QLabel("Dígitos de precisão:"), self.sim_digitos)
        params_group.setLayout(params_layout)
        layout.addWidget(params_group)

        # Grupo de método
        metodo_group = QGroupBox("Método de Precisão")
        metodo_layout = QHBoxLayout()
        self.sim_trunc = QRadioButton("Truncamento")
        self.sim_arred = QRadioButton("Arredondamento")
        self.sim_arred.setChecked(True)
        metodo_layout.addWidget(self.sim_trunc)
        metodo_layout.addWidget(self.sim_arred)
        metodo_group.setLayout(metodo_layout)
        layout.addWidget(metodo_group)

        # Botão para iniciar a simulação
        self.sim_run_btn = QPushButton("▶ Iniciar Simulação")
        self.sim_run_btn.clicked.connect(self.rodar_simulacao)  # Conecta ao método de simulação
        layout.addWidget(self.sim_run_btn)
        
        # Grupo de resultados
        result_group = QGroupBox("Resultados Finais")
        result_layout = QFormLayout()
        
        self.sim_res_exato = QLineEdit()
        self.sim_res_aprox = QLineEdit()
        self.sim_erro_abs = QLineEdit()
        self.sim_erro_rel = QLineEdit()

        for field in [self.sim_res_exato, self.sim_res_aprox, self.sim_erro_abs, self.sim_erro_rel]:
            field.setReadOnly(True)

        result_layout.addRow(QLabel("Valor Exato Total:"), self.sim_res_exato)
        result_layout.addRow(QLabel("Resultado Aproximado Final:"), self.sim_res_aprox)
        result_layout.addRow(QLabel("Erro Absoluto Total:"), self.sim_erro_abs)
        result_layout.addRow(QLabel("Erro Relativo Total (%):"), self.sim_erro_rel)
        result_group.setLayout(result_layout)
        layout.addWidget(result_group)

        # Área de log para mostrar o progresso da simulação
        log_group = QGroupBox("Log da Simulação (Primeiros 100 Passos)")
        log_layout = QVBoxLayout()
        self.sim_log = QTextEdit()  # Área de texto grande para o log
        self.sim_log.setReadOnly(True)  # Apenas leitura
        self.sim_log.setFont(QFont("JetBrains Mono", 10))  # Fonte monoespaçada (boa para números)
        log_layout.addWidget(self.sim_log)
        log_group.setLayout(log_layout)
        layout.addWidget(log_group)

    # Executa a simulação de propagação de erros
    def rodar_simulacao(self):
        try:
            # Pega os parâmetros da interface
            numero = Decimal(self.sim_valor.text())
            vezes = self.sim_vezes.value()
            dig = self.sim_digitos.value()
            
            # Escolhe a função de precisão
            met_funcao = cl.truncamento_corrigido if self.sim_trunc.isChecked() else cl.arredondamento_corrigido
            met_nome = "truncamento" if self.sim_trunc.isChecked() else "arredondamento"
            
            self.sim_log.clear()  # Limpa o log anterior

            # Calcula o valor exato (multiplicação é mais eficiente que soma repetida)
            valor_exato_total = numero * Decimal(vezes)
            soma_aproximada_atual = Decimal('0')  # Acumulador com precisão limitada

            # Loop de somas com precisão limitada
            for i in range(1, vezes + 1):
                soma_antes_precisao = soma_aproximada_atual + numero  # Soma sem limitação
                soma_aproximada_atual = met_funcao(soma_antes_precisao, dig)  # Aplica precisão
                
                # Mostra apenas os primeiros 100 passos para não sobrecarregar a interface
                if i <= 100:
                    self.sim_log.append(f"Passo {i: >3}: {soma_antes_precisao} -> ({met_nome}) -> {soma_aproximada_atual}")

            # Informa se houve mais passos além dos 100 mostrados
            if vezes > 100:
                self.sim_log.append("\n...")
                self.sim_log.append(f"(Simulação continuou por mais {vezes-100} passos)")


            # Calcula os erros finais
            erro_abs_final = cl.erroAbs(soma_aproximada_atual, valor_exato_total)
            erro_rel_final = cl.erroRel(soma_aproximada_atual, valor_exato_total)

            # Atualiza os campos de resultado
            self.sim_res_exato.setText(f"{valor_exato_total}")
            self.sim_res_aprox.setText(f"{soma_aproximada_atual}")
            self.sim_erro_abs.setText(f"{erro_abs_final}")
            
            # Formata o erro relativo como porcentagem
            if erro_rel_final.is_finite():
                erro_rel_formatado = f"{(erro_rel_final * 100):.10f}".rstrip('0').rstrip('.')
                self.sim_erro_rel.setText(f"{erro_rel_formatado}%")
            else:
                self.sim_erro_rel.setText("Infinito")

        except InvalidOperation:
            QMessageBox.critical(self, "Erro de Entrada", "Por favor, insira um valor numérico válido para a soma.")
        except Exception as e:
            QMessageBox.critical(self, "Erro Inesperado", f"Ocorreu um erro: {e}")

# Ponto de entrada da aplicação
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Cria a aplicação PyQt
    app.setStyleSheet(STYLESHEET)  # Aplica o estilo CSS
    window = CalculadoraErrosGUI()  # Cria a janela principal
    window.show()  # Mostra a janela
    sys.exit(app.exec())  # Inicia o loop de eventos e aguarda interações

