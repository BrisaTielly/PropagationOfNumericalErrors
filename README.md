# Calculadora de Erros Numéricos

Uma aplicação GUI em Python para calcular e simular propagação de erros numéricos, desenvolvida com PyQt6.

## 🖼️ Screenshots da Aplicação

### Calculadora Padrão
![Calculadora Padrão](https://github.com/BrisaTielly/PropagationOfNumericalErrors/blob/main/images/Screenshot_120.png)

### Calculadora Sequencial
![Simulação de Propagação de Erros](https://github.com/BrisaTielly/PropagationOfNumericalErrors/blob/main/images/Screenshot_121.png)

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes do Python)

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/BrisaTielly/PropagationOfNumericalErrors.git
cd PropagationOfNumericalErrors
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv .venv
```

3. Ative o ambiente virtual:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
.venv\Scripts\activate.bat
```

**Linux/macOS:**
```bash
source .venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

## ▶️ Como executar

**Opção 1 - Com ambiente virtual ativado:**
```bash
python app_gui.py
```

**Opção 2 - Diretamente com o Python do ambiente virtual:**
```bash
# Windows
.venv\Scripts\python.exe app_gui.py

# Linux/macOS
.venv/bin/python app_gui.py
```

**Opção 3 - Interface de linha de comando (modo texto):**
```bash
python main.py
```

## 🎯 Funcionalidades

### Calculadora Padrão
- Realiza operações básicas (+, -, *, /) com dois números
- Calcula erros absolutos e relativos
- Suporte a truncamento e arredondamento
- Configurável número de dígitos de precisão

### Simulação de Propagação de Erros
- Simula múltiplas somas com precisão limitada
- Mostra como os erros se acumulam ao longo das operações
- Log detalhado dos primeiros 100 passos
- Comparação entre resultado exato e aproximado


## 📁 Estrutura do Projeto

```
├── app_gui.py          # Interface gráfica principal (PyQt6)
├── main.py             # Lógica de cálculo e funções matemáticas
├── requirements.txt    # Dependências do projeto
├── .venv/              # Ambiente virtual (criado automaticamente)
├── images/             # Diretório para ícones e imagens
└── README.md          # Este arquivo
```

## 🔧 Dependências

- **PyQt6**: Framework para interface gráfica
- **decimal**: Biblioteca padrão do Python para cálculos de alta precisão

## 📝 Notas

- O arquivo `main.py` contém toda a lógica de cálculo e é **obrigatório** para o funcionamento da aplicação
- A GUI (`app_gui.py`) é apenas a interface visual que utiliza as funções do `main.py`
- A aplicação funciona melhor em sistemas com fontes modernas instaladas
- **Importante**: Para Python 3.13+, use PyQt6 versão 6.9.1 ou superior para evitar problemas de DLL

## 🐛 Solução de Problemas

### Erro de DLL no Windows
Se você encontrar o erro "DLL load failed while importing QtCore":
1. Certifique-se de estar usando Python 3.8+ (recomendado 3.11+)
2. Reinstale o PyQt6:
```bash
pip uninstall PyQt6 -y
pip install PyQt6 --no-cache-dir
```

### Problemas com ambiente virtual
Se o ambiente virtual não ativar no Windows PowerShell:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```