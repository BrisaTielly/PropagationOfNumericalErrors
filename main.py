import math
# Usando o módulo decimal para evitar problemas de precisão com floats
from decimal import Decimal, getcontext, ROUND_HALF_UP, ROUND_DOWN

# Configurando uma precisão bem alta para os cálculos
getcontext().prec = 50 

# Funções para calcular diferentes tipos de erro
def erroAbs(resultado_aproximado, resultado_exato):
    """Calcula o erro absoluto - diferença simples entre os valores."""
    return abs(resultado_exato - resultado_aproximado)

def erroRel(resultado_aproximado, resultado_exato):
    """Calcula o erro relativo - erro em relação ao valor exato."""
    if resultado_exato == 0:
        return Decimal('Infinity') if resultado_aproximado != 0 else Decimal('0')
    return (abs(resultado_exato - resultado_aproximado) / resultado_aproximado)

# Operações básicas que funcionam diretamente com Decimal
def soma(n1, n2): return n1 + n2
def subtracacao(n1, n2): return n1 - n2
def multiplicacao(n1, n2): return n1 * n2
def divisao(n1, n2): return n1 / n2 if n2 != 0 else Decimal('NaN')

# Funções para controlar a precisão dos números
def truncamento_corrigido(numero, digitos):
    """Corta o número para manter apenas uma certa quantidade de dígitos significativos."""
    if numero == 0:
        return Decimal('0')
    
    # Calcula quantas casas decimais precisamos para manter os dígitos significativos
    ordem = math.floor(numero.log10())
    casas_decimais = digitos - ordem - 1
    
    # Se casas_decimais for negativo, significa que precisamos arredondar para múltiplos de 10
    if casas_decimais < 0:
        # Para 1 dígito significativo em números como 12.2, queremos 10
        # Para 1 dígito significativo em números como 123.4, queremos 100
        quantizer = Decimal('1e' + str(-casas_decimais))
    else:
        quantizer = Decimal('1e-' + str(casas_decimais))
    
    # Aplica o truncamento (sempre para baixo)
    return numero.quantize(quantizer, rounding=ROUND_DOWN)

def arredondamento_corrigido(numero, digitos):
    """Arredonda o número para manter uma certa quantidade de dígitos significativos."""
    if numero == 0:
        return Decimal('0')
    
    # Mesma lógica do truncamento, mas com arredondamento
    ordem = math.floor(numero.log10())
    casas_decimais = digitos - ordem - 1
    
    # Se casas_decimais for negativo, significa que precisamos arredondar para múltiplos de 10
    if casas_decimais < 0:
        # Para 1 dígito significativo em números como 12.2, queremos 10
        # Para 1 dígito significativo em números como 123.4, queremos 100
        quantizer = Decimal('1e' + str(-casas_decimais))
    else:
        quantizer = Decimal('1e-' + str(casas_decimais))
    
    # Aplica o arredondamento (meio para cima)
    return numero.quantize(quantizer, rounding=ROUND_HALF_UP)

# Mapeamento dos símbolos para as funções de operação
operacoes = {
    '+': soma,
    '-': subtracacao,
    '*': multiplicacao,
    '/': divisao
}

# Simulação de como o erro se acumula em múltiplas somas
def propagacao_erro_soma():
    """Mostra como pequenos erros de precisão vão se acumulando em operações repetidas."""
    try:
        # Pede os dados do usuário
        numero_str = input("Informe o valor a ser somado repetidamente: ")
        numero = Decimal(numero_str)
        
        vezes = int(input("Quantas vezes o valor deve ser somado? "))
        dig = int(input("Informe quantos dígitos de precisão deseja utilizar: "))
        met = int(input("Informe qual método de precisão deseja utilizar (1- truncamento 2-arredondamento): "))

        # Valida as entradas
        if vezes <= 0 or dig <= 0 or met not in [1, 2]:
            print("Valores inválidos. O número de somas e dígitos deve ser positivo, e o método deve ser 1 ou 2.")
            return

        # Escolhe qual função de precisão usar
        met_funcao = truncamento_corrigido if met == 1 else arredondamento_corrigido
        met_nome = "truncamento" if met == 1 else "arredondamento"

        # Calcula o resultado exato (sem erro de precisão)
        valor_exato_total = numero * Decimal(vezes)
        
        # Vai somando com erro de precisão
        soma_aproximada_atual = Decimal('0')

        print("\n--- Iniciando Simulação ---")
        for i in range(1, vezes + 1):
            # Soma sem aplicar precisão ainda
            soma_antes_precisao = soma_aproximada_atual + numero
            # Aplica a precisão escolhida
            soma_aproximada_atual = met_funcao(soma_antes_precisao, dig)
            
            print(f"Soma {i}: {soma_antes_precisao}. Após {met_nome}: {soma_aproximada_atual}")
        
        # Calcula os erros finais
        erro_abs_final = erroAbs(soma_aproximada_atual, valor_exato_total)
        erro_rel_final = erroRel(soma_aproximada_atual, valor_exato_total)
        erro_rel_percent = f"{(erro_rel_final * 100):.10f}%" if erro_rel_final.is_finite() else "inf%"

        # Mostra os resultados
        print("\n--- Resultados Finais da Simulação ---")
        print(f"Valor Exato Esperado: {valor_exato_total}")
        print(f"Resultado Aproximado Final: {soma_aproximada_atual}")
        print("-" * 30)
        print(f"Erro Absoluto Total: {erro_abs_final}")
        print(f"Erro Relativo Total: {erro_rel_final} (ou {erro_rel_percent})")
        print("-" * 30)

    except Exception as e:
        print(f"Ocorreu um erro: {e}. Por favor, verifique os valores informados.")

# Calculadora principal que compara resultados exatos vs aproximados
def calculadora_padrao():
    """Calculadora que mostra como a precisão afeta os resultados das operações."""
    ans_exata_acumulada = Decimal('0')
    ans_aprox_acumulada = Decimal('0')
    acumular = 'n'

    while True:
        try:
            # Pega o primeiro valor (ou usa o acumulado)
            if acumular.lower() != 's':
                n1 = Decimal(input("Informe o primeiro valor de sua operação: "))
            else:
                n1 = ans_aprox_acumulada
                print(f"Usando o valor acumulado aproximado como primeiro valor: {n1}")

            # Pede os outros dados
            n2 = Decimal(input("Informe o segundo valor de sua operação: "))
            op_str = input("Informe qual operação deseja realizar (+, -, *, /): ")
            dig = int(input("Informe quantos dígitos de precisão deseja obter: "))
            met = int(input("Informe qual método de precisão deseja utilizar (1- trucamento 2-arredondamento): "))

            # Configura as funções baseado na escolha do usuário
            met_funcao = truncamento_corrigido if met == 1 else arredondamento_corrigido
            op_funcao = operacoes.get(op_str)

            if not op_funcao:
                print("Operação inválida!")
                continue

            # Aplica a precisão aos números antes de fazer a operação
            valor1_aprox = met_funcao(n1, dig)
            valor2_aprox = met_funcao(n2, dig)
            
            # Calcula o resultado exato (sem aplicar precisão)
            primeiro_valor_exato = ans_exata_acumulada if acumular.lower() == 's' else n1
            resultado_exato = op_funcao(primeiro_valor_exato, n2)
            
            # Calcula o resultado aproximado (usando os valores com precisão limitada)
            resultado_aprox = op_funcao(valor1_aprox, valor2_aprox)

            # Mostra os resultados
            met_nome = "truncado" if met == 1 else "arredondado"
            print("-" * 30)
            print(f"Primeiro valor {met_nome}: {valor1_aprox}")
            print(f"Segundo valor {met_nome}: {valor2_aprox}")
            print(f"Resultado exato: {resultado_exato}")
            print(f"Resultado com erro (aproximado): {resultado_aprox}")
            
            # Calcula e mostra os erros
            erro_abs = erroAbs(resultado_aprox, resultado_exato)
            erro_rel = erroRel(resultado_aprox, resultado_exato)
            
            erro_rel_percent = f"{(erro_rel * 100):.2f}%" if erro_rel.is_finite() else "inf%"
            print(f"Erro Absoluto: {erro_abs}")
            print(f"Erro Relativo: {erro_rel} (ou {erro_rel_percent})")
            print("-" * 30)

            # Salva os resultados para possível acumulação
            ans_exata_acumulada = resultado_exato
            ans_aprox_acumulada = resultado_aprox
            
            # Pergunta se quer continuar
            continuar_op = input("Deseja realizar outra operação dentro da calculadora? (s/n): ")
            if continuar_op.lower() != 's':
                break
            
            acumular = input("Deseja acumular o último resultado nesta operação (s/n): ")

        except Exception as e:
            print(f"Ocorreu um erro: {e}. Por favor, verifique os valores informados.")
            break

# Menu principal do programa
def main():
    """Função principal que mostra o menu e chama as outras funções."""
    while True:
        print("\n===== CALCULADORA DE ERROS NUMÉRICOS =====")
        print("1. Calculadora de Operação Padrão")
        print("2. Simular Propagação de Erro em Somas")
        print("3. Sair")
        
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            calculadora_padrao()
        elif escolha == '2':
            propagacao_erro_soma()
        elif escolha == '3':
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida! Por favor, escolha 1, 2 ou 3.")

# Inicia o programa quando executado diretamente
if __name__ == "__main__":
    main()