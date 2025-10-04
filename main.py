from decimal import Decimal, getcontext

# Configurar precisão alta para cálculos exatos
getcontext().prec = 50

ans_exata = 0
ans_aprox = 0
acumular = 'n'

def erroAbs(resultado_aproximado,resultado_exato):
    return abs(resultado_exato - resultado_aproximado)

def erroRel(resultado_aproximado,resultado_exato):
    return abs( (resultado_exato - resultado_aproximado) / resultado_aproximado)

def soma(n1,n2):
    return n1+n2

def subtracacao(n1,n2):
    return n1-n2

def multiplicacao(n1,n2):
    return n1*n2

def divisao(n1,n2):
    return n1/n2


def truncamento(numero,qtd_digitos): 
    string_numero = str(numero)
    parte = string_numero.split('.') #Extraindo numero
    inteiro = parte[0] #Extraindo parte inteira 
    decimal = parte[1] #Extraindo parte decimal
    if(inteiro == '0'):
        for i, items in enumerate(decimal):
            if(items!='0'): #Excluindo zeros a esquerda
                break
        return '0.'+decimal[0:i+qtd_digitos]
    else:
        if(len(inteiro)>qtd_digitos):
            return inteiro[0:qtd_digitos] + ('0'* (len(inteiro) - qtd_digitos))  #Parte inteira + completo com zeros
        else:
            return inteiro+'.'+decimal[0:(qtd_digitos - len(inteiro))] #Concatenação
        
def arredondamento(numero,qtd_digitos):
    string_numero = str(numero)
    # Expandir notação científica se necessário
    if 'e' in string_numero.lower():
        numero = float(string_numero)
        string_numero = f"{numero:.15f}".rstrip('0')
    
    if '.' not in string_numero:
        string_numero += '.0'
    
    parte = string_numero.split('.') #Extraindo numero
    inteiro = parte[0] #Extraindo parte inteira 
    decimal = parte[1] if len(parte) > 1 else '0' #Extraindo parte decimal
    
    if(inteiro == '0' or inteiro == '-0'):
        for i, items in enumerate(decimal):
            if(items!='0'): #Excluindo zeros a esquerda
                break
        else:
            # Todos são zeros
            return '0.' + '0' * qtd_digitos
        
        # Verificar se temos dígitos suficientes
        if i+qtd_digitos > len(decimal):
            # Adicionar zeros se necessário
            decimal = decimal + '0' * (i + qtd_digitos + 1 - len(decimal))
        
        # Verificar se deve arredondar para cima
        if int(decimal[i+qtd_digitos]) >= 5:
            # Pegar os dígitos significativos e incrementar
            digitos = decimal[i:i+qtd_digitos]
            numero_int = int(digitos) + 1
            digitos_str = str(numero_int)
            
            # Verificar se houve carry (ex: 9999 + 1 = 10000)
            if len(digitos_str) > qtd_digitos:
                # Ajustar zeros à esquerda e dígitos
                return '0.' + '0' * (i-1) + digitos_str
            else:
                return '0.' + '0' * i + digitos_str.zfill(qtd_digitos)
        return '0.' + '0' * i + decimal[i:i+qtd_digitos]
    else:
        if(len(inteiro)>qtd_digitos):
            if qtd_digitos < len(inteiro) and int(inteiro[qtd_digitos]) >= 5:
                numero_int = int(inteiro[0:qtd_digitos]) + 1
                digitos_arredondados = str(numero_int).zfill(qtd_digitos)
                return digitos_arredondados + ('0'* (len(inteiro) - qtd_digitos))
            return inteiro[0:qtd_digitos] + ('0'* (len(inteiro) - qtd_digitos))
        else:
            decimais_necessarios = qtd_digitos - len(inteiro)
            if decimais_necessarios > len(decimal):
                decimal = decimal + '0' * (decimais_necessarios + 1 - len(decimal))
            
            if int(decimal[decimais_necessarios]) >= 5:
                numero_completo = inteiro + decimal[0:decimais_necessarios]
                numero_int = int(numero_completo) + 1
                resultado = str(numero_int)
                if len(resultado) > len(inteiro):
                    return resultado[0:len(inteiro)] + '.' + resultado[len(inteiro):]
                else:
                    return resultado + '.' + '0' * decimais_necessarios
            return inteiro+'.'+decimal[0:decimais_necessarios]

if __name__ == "__main__":
    while True: 
        if(acumular.lower() != 's'): 
            n1_input = input("Informe o primeiro valor de sua operação: ")
            n1 = float(n1_input)
            n1_exato = Decimal(n1_input)
            ans_exata = n1_exato
        else:
            n1 = ans_aprox
            n1_exato = Decimal(str(ans_aprox))
        n2_input = input("Informe o segundo valor de sua operação: ")
        n2 = float(n2_input)
        n2_exato = Decimal(n2_input)
        op = input("Informe qual operação deseja realizar (+, -, *, /): ")
        dig = int(input("Informe quantos dígitos de precisão deseja obter: "))
        met = int(input("Informe qual método de precisão deseja utilizar (1- trucamento 2-arredondamento): "))

        match(met):
            case 1:
                match(op):
                    case '+':
                        valor1= float(truncamento(n1,dig))
                        valor2= float(truncamento(n2,dig))
                        resultado1_exato = ans_exata + n2_exato
                        resultado1 = float(resultado1_exato)
                        print(f"Primeiro valor truncado: {valor1}")
                        print(f"Segundo valor truncado: {valor2}")
                        print(f"Resultado exato: {resultado1_exato}")
                        resultado2 = truncamento(soma(valor1,valor2),dig)
                        print(f"Resultado com erro: {resultado2}")
                        print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1_exato))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1_exato))}")
                        ans_exata = resultado1_exato
                        ans_aprox = float(resultado2)
                    case '-':
                        valor1= float(truncamento(n1,dig))
                        valor2= float(truncamento(n2,dig))
                        resultado1_exato = ans_exata - n2_exato
                        resultado1 = float(resultado1_exato)
                        print(f"Primeiro valor truncado: {valor1}")
                        print(f"Segundo valor truncado: {valor2}")
                        print(f"Resultado exato: {resultado1_exato}")
                        resultado2 = truncamento(subtracacao(valor1,valor2),dig)
                        print(f"Resultado com erro: {resultado2}")
                        print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1_exato))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1_exato))}")
                        ans_exata = resultado1_exato
                        ans_aprox = float(resultado2)
                    case '*':
                        valor1= float(truncamento(n1,dig))
                        valor2= float(truncamento(n2,dig))
                        resultado1_exato = ans_exata * n2_exato
                        resultado1 = float(resultado1_exato)
                        print(f"Primeiro valor truncado: {valor1}")
                        print(f"Segundo valor truncado: {valor2}")
                        print(f"Resultado exato: {resultado1_exato}")
                        resultado2 = truncamento(multiplicacao(valor1,valor2),dig)
                        print(f"Resultado com erro: {resultado2}")
                        print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1_exato))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1_exato))}")
                        ans_exata = resultado1_exato
                        ans_aprox = float(resultado2)
                    case '/':
                        valor1= float(truncamento(n1,dig))
                        valor2= float(truncamento(n2,dig))
                        resultado1_exato = ans_exata / n2_exato
                        resultado1 = float(resultado1_exato)
                        print(f"Primeiro valor truncado: {valor1}")
                        print(f"Segundo valor truncado: {valor2}")
                        print(f"Resultado exato: {resultado1_exato}")
                        resultado2 = truncamento(divisao(valor1,valor2),dig)
                        print(f"Resultado com erro: {resultado2}")
                        print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1_exato))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1_exato))}")
                        ans_exata = resultado1_exato
                        ans_aprox = float(resultado2)
            case 2:
                match(op):
                    case '+':
                        valor1= float(arredondamento(n1,dig))
                        valor2= float(arredondamento(n2,dig))
                        resultado1_exato = ans_exata + n2_exato
                        resultado1 = float(resultado1_exato)
                        print(f"Primeiro valor arredondado: {valor1}")
                        print(f"Segundo valor arredondado: {valor2}")
                        print(f"Resultado exato: {resultado1_exato}")
                        resultado2 = arredondamento(soma(valor1,valor2),dig)
                        print(f"Resultado com erro: {resultado2}")
                        print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1_exato))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1_exato))}")
                        ans_exata = resultado1_exato
                        ans_aprox = float(resultado2)
                    case '-':
                        valor1= float(arredondamento(n1,dig))
                        valor2= float(arredondamento(n2,dig))
                        resultado1_exato = ans_exata - n2_exato
                        resultado1 = float(resultado1_exato)
                        print(f"Primeiro valor arredondado: {valor1}")
                        print(f"Segundo valor arredondado: {valor2}")
                        print(f"Resultado exato: {resultado1_exato}")
                        resultado2 = arredondamento(subtracacao(valor1,valor2),dig)
                        print(f"Resultado com erro: {resultado2}")
                        print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1_exato))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1_exato))}")
                        ans_exata = resultado1_exato
                        ans_aprox = float(resultado2)
                    case '*':
                        valor1= float(arredondamento(n1,dig))
                        valor2= float(arredondamento(n2,dig))
                        resultado1_exato = ans_exata * n2_exato
                        resultado1 = float(resultado1_exato)
                        print(f"Primeiro valor arredondado: {valor1}")
                        print(f"Segundo valor arredondado: {valor2}")
                        print(f"Resultado exato: {resultado1_exato}")
                        resultado2 = arredondamento(multiplicacao(valor1,valor2),dig)
                        print(f"Resultado com erro: {resultado2}")
                        print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1_exato))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1_exato))}")
                        ans_exata = resultado1_exato
                        ans_aprox = float(resultado2)
                    case '/':
                        valor1= float(arredondamento(n1,dig))
                        valor2= float(arredondamento(n2,dig))
                        resultado1_exato = ans_exata / n2_exato
                        resultado1 = float(resultado1_exato)
                        print(f"Primeiro valor arredondado: {valor1}")
                        print(f"Segundo valor arredondado: {valor2}")
                        print(f"Resultado exato: {resultado1_exato}")
                        resultado2 = arredondamento(divisao(valor1,valor2),dig)
                        print(f"Resultado com erro: {resultado2}")
                        print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1_exato))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1_exato))}")
                        ans_exata = resultado1_exato
                        ans_aprox = float(resultado2)

        continuar = input("Deseja continuar realizando uma nova operação? (s/n)")
        if continuar.lower() != 's':
            break
        acumular = input("Deseja acumular ultimo resultado nesta operação (s/n): ")
