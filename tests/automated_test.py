#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste automatizado VISUAL para a interface gráfica da Calculadora de Erros Numéricos.
Mostra a GUI e executa os testes de forma visual para o usuário acompanhar.
"""
import sys
import time
from decimal import Decimal
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer, Qt
import app_gui

class TestResults:
    """Classe para armazenar resultados dos testes."""
    def __init__(self):
        self.tests = []
        self.passed = 0
        self.failed = 0
    
    def add_test(self, name, passed, message=""):
        self.tests.append((name, passed, message))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
        
        # Imprime no console também
        status = "[OK]" if passed else "[ERRO]"
        print(f"{status} {name}")
        if message and not passed:
            print(f"    -> {message}")

def compare_decimal(expected, actual, tolerance=0.001):
    """Compara dois valores com tolerância."""
    try:
        expected_dec = Decimal(str(expected))
        actual_dec = Decimal(str(actual))
        diff = abs(expected_dec - actual_dec)
        return diff <= Decimal(str(tolerance))
    except:
        return False

class TestRunner:
    """Classe que executa os testes de forma visual."""
    
    def __init__(self, window):
        self.window = window
        self.results = TestResults()
        self.test_queue = []
        self.current_test_index = 0
        
        # Configura o timer para executar testes sequencialmente
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_next_test)
        
    def add_test(self, test_func, name, delay=1500):
        """Adiciona um teste à fila."""
        self.test_queue.append((test_func, name, delay))
    
    def start(self):
        """Inicia a execução dos testes."""
        print("\n" + "="*70)
        print("   TESTES VISUAIS DA GUI - CALCULADORA DE ERROS")
        print("="*70)
        print("\nExecutando testes... Acompanhe na janela da GUI!\n")
        
        self.current_test_index = 0
        self.run_next_test()
    
    def run_next_test(self):
        """Executa o próximo teste da fila."""
        if self.current_test_index >= len(self.test_queue):
            # Todos os testes foram executados
            self.timer.stop()  # Para o timer antes de mostrar resultados
            self.show_final_results()
            return
        
        test_func, name, delay = self.test_queue[self.current_test_index]
        
        print(f"\n[Teste {self.current_test_index + 1}/{len(self.test_queue)}] {name}")
        
        # Executa o teste
        test_func()
        
        # Agenda o próximo teste
        self.current_test_index += 1
        self.timer.start(delay)
    
    def show_final_results(self):
        """Mostra os resultados finais em um diálogo."""
        print("\n" + "="*70)
        print("RESUMO DOS TESTES")
        print("="*70 + "\n")
        
        summary = f"Total: {self.results.passed}/{len(self.results.tests)} testes passaram\n\n"
        
        for name, passed, message in self.results.tests:
            status = "[OK]" if passed else "[ERRO]"
            summary += f"{status} {name}\n"
            if message and not passed:
                summary += f"   -> {message}\n"
        
        if self.results.passed == len(self.results.tests):
            title = "Todos os Testes Passaram! ✓"
            print("\n>>> TODOS OS TESTES PASSARAM! <<<\n")
            QMessageBox.information(self.window, title, summary)
        else:
            title = "Alguns Testes Falharam"
            print(f"\n>>> {self.results.failed} teste(s) falharam <<<\n")
            QMessageBox.warning(self.window, title, summary)
    
    # ===== TESTES DA CALCULADORA =====
    
    def test_soma_truncamento(self):
        """Teste 1: Soma com Truncamento (Exemplo 1)"""
        tabs = self.window.findChild(app_gui.QTabWidget)
        if tabs:
            tabs.setCurrentIndex(0)
        
        self.window.calc_n1.setText("0.12345")
        self.window.calc_n2.setText("0.67890")
        self.window.calc_digitos.setValue(4)
        self.window.calc_trunc.setChecked(True)
        self.window.calcular('+')
        
        res_aprox = self.window.calc_res_aprox.text()
        erro_abs = self.window.calc_erro_abs.text()
        
        passed = (compare_decimal("0.8023", res_aprox, 0.0001) and 
                 compare_decimal("0.00005", erro_abs, 0.000001))
        
        self.results.add_test("Soma com Truncamento (Ex. 1)", passed)
    
    def test_soma_arredondamento(self):
        """Teste 2: Soma com Arredondamento (Exemplo 1)"""
        self.window.calc_n1.setText("0.12345")
        self.window.calc_n2.setText("0.67890")
        self.window.calc_digitos.setValue(4)
        self.window.calc_arred.setChecked(True)
        self.window.calcular('+')
        
        res_aprox = self.window.calc_res_aprox.text()
        erro_abs = self.window.calc_erro_abs.text()
        
        passed = (compare_decimal("0.8024", res_aprox, 0.0001) and 
                 compare_decimal("0.00005", erro_abs, 0.000001))
        
        self.results.add_test("Soma com Arredondamento (Ex. 1)", passed)
    
    def test_subtracao_truncamento(self):
        """Teste 3: Subtração com Cancelamento - Truncamento (Exemplo 20)"""
        self.window.calc_n1.setText("0.76545")
        self.window.calc_n2.setText("0.76541")
        self.window.calc_digitos.setValue(4)
        self.window.calc_trunc.setChecked(True)
        self.window.calcular('-')
        
        res_aprox = self.window.calc_res_aprox.text()
        erro_rel = self.window.calc_erro_rel.text()
        
        passed = (compare_decimal("0.0000", res_aprox, 0.0001) and 
                 erro_rel == "Infinito")
        
        msg = "" if passed else f"Esperado: 0.0000 e Infinito, Obtido: {res_aprox} e {erro_rel}"
        self.results.add_test("Subtracao com Cancelamento - Truncamento (Ex. 20)", passed, msg)
    
    def test_subtracao_arredondamento(self):
        """Teste 4: Subtração com Cancelamento - Arredondamento (Exemplo 20)"""
        self.window.calc_n1.setText("0.76545")
        self.window.calc_n2.setText("0.76541")
        self.window.calc_digitos.setValue(4)
        self.window.calc_arred.setChecked(True)
        self.window.calcular('-')
        
        res_aprox = self.window.calc_res_aprox.text()
        erro_abs = self.window.calc_erro_abs.text()
        erro_rel = self.window.calc_erro_rel.text()
        
        passed = compare_decimal("0.0001", res_aprox, 0.0001)
        
        if erro_rel != "Infinito":
            erro_rel_num = erro_rel.replace("%", "")
            passed = passed and compare_decimal("60", erro_rel_num, 5)
        
        self.results.add_test("Subtracao com Cancelamento - Arredondamento (Ex. 20)", passed)
    
    def test_multiplicacao(self):
        """Teste 5: Multiplicação simples"""
        self.window.calc_n1.setText("2.5")
        self.window.calc_n2.setText("4.0")
        self.window.calc_digitos.setValue(4)
        self.window.calc_arred.setChecked(True)
        self.window.calcular('*')
        
        res_aprox = self.window.calc_res_aprox.text()
        passed = compare_decimal("10.0", res_aprox, 0.1)
        
        self.results.add_test("Multiplicacao simples", passed)
    
    def test_divisao(self):
        """Teste 6: Divisão simples"""
        self.window.calc_n1.setText("10.0")
        self.window.calc_n2.setText("2.0")
        self.window.calc_digitos.setValue(4)
        self.window.calc_arred.setChecked(True)
        self.window.calcular('/')
        
        res_aprox = self.window.calc_res_aprox.text()
        passed = compare_decimal("5.0", res_aprox, 0.1)
        
        self.results.add_test("Divisao simples", passed)
    
    # ===== TESTES DA SIMULAÇÃO =====
    
    def test_simulacao_truncamento(self):
        """Teste 7: Propagação de Erro - Truncamento (Exemplo 3)"""
        tabs = self.window.findChild(app_gui.QTabWidget)
        if tabs:
            tabs.setCurrentIndex(1)
        
        self.window.sim_valor.setText("0.56786")
        self.window.sim_vezes.setValue(10)
        self.window.sim_digitos.setValue(4)
        self.window.sim_trunc.setChecked(True)
        self.window.rodar_simulacao()
        
        res_aprox = self.window.sim_res_aprox.text()
        erro_abs = self.window.sim_erro_abs.text()
        
        passed = (compare_decimal("5.671", res_aprox, 0.001) and 
                 compare_decimal("0.0076", erro_abs, 0.0001))
        
        self.results.add_test("Propagacao de Erro - Truncamento (Ex. 3)", passed)
    
    def test_simulacao_arredondamento(self):
        """Teste 8: Propagação de Erro - Arredondamento (Exemplo 3)"""
        self.window.sim_valor.setText("0.56786")
        self.window.sim_vezes.setValue(10)
        self.window.sim_digitos.setValue(4)
        self.window.sim_arred.setChecked(True)
        self.window.rodar_simulacao()
        
        res_aprox = self.window.sim_res_aprox.text()
        erro_abs = self.window.sim_erro_abs.text()
        
        passed = (compare_decimal("5.680", res_aprox, 0.001) and 
                 compare_decimal("0.0014", erro_abs, 0.0001))
        
        self.results.add_test("Propagacao de Erro - Arredondamento (Ex. 3)", passed)
    
    def test_simulacao_valor_pequeno(self):
        """Teste 9: Propagação com valor pequeno"""
        self.window.sim_valor.setText("0.0001")
        self.window.sim_vezes.setValue(100)
        self.window.sim_digitos.setValue(3)
        self.window.sim_arred.setChecked(True)
        self.window.rodar_simulacao()
        
        res_exato = self.window.sim_res_exato.text()
        passed = compare_decimal("0.01", res_exato, 0.0001)
        
        self.results.add_test("Propagacao com valor pequeno", passed)

def main():
    """Executa todos os testes de forma visual."""
    # Cria a aplicação Qt
    app = QApplication(sys.argv)
    app.setStyleSheet(app_gui.STYLESHEET)
    
    # Cria a janela da aplicação
    window = app_gui.CalculadoraErrosGUI()
    window.show()
    
    # Cria o executor de testes
    runner = TestRunner(window)
    
    # Adiciona todos os testes à fila (com delay de 1.5 segundos entre cada)
    runner.add_test(runner.test_soma_truncamento, "Soma com Truncamento", 1500)
    runner.add_test(runner.test_soma_arredondamento, "Soma com Arredondamento", 1500)
    runner.add_test(runner.test_subtracao_truncamento, "Subtracao - Truncamento (Divisao por Zero)", 1500)
    runner.add_test(runner.test_subtracao_arredondamento, "Subtracao - Arredondamento", 1500)
    runner.add_test(runner.test_multiplicacao, "Multiplicacao", 1500)
    runner.add_test(runner.test_divisao, "Divisao", 1500)
    runner.add_test(runner.test_simulacao_truncamento, "Simulacao - Truncamento", 2000)
    runner.add_test(runner.test_simulacao_arredondamento, "Simulacao - Arredondamento", 2000)
    runner.add_test(runner.test_simulacao_valor_pequeno, "Simulacao - Valor Pequeno", 2000)
    
    # Inicia os testes após 1 segundo (para dar tempo de ver a janela)
    QTimer.singleShot(1000, runner.start)
    
    # Executa a aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    main()

