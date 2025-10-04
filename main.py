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
    parte = string_numero.split('.') #Extraindo numero
    inteiro = parte[0] #Extraindo parte inteira 
    decimal = parte[1] #Extraindo parte decimal
    if(inteiro == '0'):
        for i, items in enumerate(decimal):
            if(items!='0'): #Excluindo zeros a esquerda
                break
        if(int(decimal[i+qtd_digitos]) >= 5):
           valor = int(decimal[i+qtd_digitos]) + 1
           return '0.'+decimal[0:i+qtd_digitos - 1] + str(valor)
        return '0.'+decimal[0:i+qtd_digitos]
    else:
        if(len(inteiro)>qtd_digitos):
            if(int(inteiro[qtd_digitos +1]) >= 5):
                valor = int(inteiro[qtd_digitos - 1]) + 1
                return '0.'+inteiro[0:qtd_digitos-1] + str(valor) + ('0'* (len(inteiro) - qtd_digitos))
            return inteiro[0:qtd_digitos] + ('0'* (len(inteiro) - qtd_digitos))  #Parte inteira + completo com zeros
        else:
            if(int(decimal[qtd_digitos - len(inteiro)])) >= 5:
                valor = int(decimal[qtd_digitos - len(inteiro)]) + 1
                return inteiro+'.'+decimal[0:(qtd_digitos - len(inteiro) - 1)] + str(valor)
            return inteiro+'.'+decimal[0:(qtd_digitos - len(inteiro))] #Concatenação
        
while True: 
    if(acumular.lower() != 's'): 
        n1 = float(input("Informe o primeiro valor de sua operação: "))
        ans_exata = n1
    else:
        n1 = ans_aprox
    n2 = float(input("Informe o segundo valor de sua operação: "))
    op = input("Informe qual operação deseja realizar (+, -, *, /): ")
    dig = int(input("Informe quantos dígitos de precisão deseja obter: "))
    met = int(input("Informe qual método de precisão deseja utilizar (1- trucamento 2-arredondamento): "))

    match(met):
        case 1:
            match(op):
                case '+':
                    valor1= float(truncamento(n1,dig))
                    valor2= float(truncamento(n2,dig))
                    resultado1 = soma(ans_exata,n2)
                    print(f"Primeiro valor truncado: {valor1}")
                    print(f"Primeiro valor truncado: {valor2}")
                    print(f"Resultado exato: {resultado1}")
                    resultado2 = truncamento(soma(valor1,valor2),dig)
                    print(f"Resultado com erro: {resultado2}")
                    print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1))}")
                    ans_exata = float(resultado1)
                    ans_aprox = float(resultado2)
                case '-':
                    valor1= float(truncamento(n1,dig))
                    valor2= float(truncamento(n2,dig))
                    resultado1 = subtracacao(ans_exata,n2)
                    print(f"Primeiro valor truncado: {valor1}")
                    print(f"Primeiro valor truncado: {valor2}")
                    print(f"Resultado exato: {resultado1}")
                    resultado2 = truncamento(subtracacao(valor1,valor2),dig)
                    print(f"Resultado com erro: {resultado2}")
                    print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1))}")
                    ans_exata = float(resultado1)
                    ans_aprox = float(resultado2)
                case '*':
                    valor1= float(truncamento(n1,dig))
                    valor2= float(truncamento(n2,dig))
                    resultado1 = multiplicacao(ans_exata,n2)
                    print(f"Primeiro valor truncado: {valor1}")
                    print(f"Primeiro valor truncado: {valor2}")
                    print(f"Resultado exato: {resultado1}")
                    resultado2 = truncamento(multiplicacao(valor1,valor2),dig)
                    print(f"Resultado com erro: {resultado2}")
                    print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1))}")
                    ans_exata = float(resultado1)
                    ans_aprox = float(resultado2)
                case '/':
                    valor1= float(truncamento(n1,dig))
                    valor2= float(truncamento(n2,dig))
                    resultado1 = divisao(ans_exata,n2)
                    print(f"Primeiro valor truncado: {valor1}")
                    print(f"Primeiro valor truncado: {valor2}")
                    print(f"Resultado exato: {resultado1}")
                    resultado2 = truncamento(divisao(valor1,valor2),dig)
                    print(f"Resultado com erro: {resultado2}")
                    print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1))}")
                    ans_exata = float(resultado1)
                    ans_aprox = float(resultado2)
        case 2:
            match(op):
                case '+':
                    valor1= float(arredondamento(n1,dig))
                    valor2= float(arredondamento(n2,dig))
                    resultado1 = soma(ans_exata,n2)
                    print(f"Primeiro valor arredondado: {valor1}")
                    print(f"Segundo valor arredondado: {valor2}")
                    print(f"Resultado exato: {resultado1}")
                    resultado2 = arredondamento(soma(valor1,valor2),dig)
                    print(f"Resultado com erro: {resultado2}")
                    print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1))}")
                    ans_exata = float(resultado1)
                    ans_aprox = float(resultado2)
                case '-':
                    valor1= float(arredondamento(n1,dig))
                    valor2= float(arredondamento(n2,dig))
                    resultado1 = subtracacao(ans_exata,n2)
                    print(f"Primeiro valor arredondado: {valor1}")
                    print(f"Segundo valor arredondado: {valor2}")
                    print(f"Resultado exato: {resultado1}")
                    resultado2 = arredondamento(subtracacao(valor1,valor2),dig)
                    print(f"Resultado com erro: {resultado2}")
                    print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1))}")
                    ans_exata = float(resultado1)
                    ans_aprox = float(resultado2)
                case '*':
                    valor1= float(arredondamento(n1,dig))
                    valor2= float(arredondamento(n2,dig))
                    resultado1 = multiplicacao(ans_exata,n2)
                    print(f"Primeiro valor arredondado: {valor1}")
                    print(f"Segundo valor arredondado: {valor2}")
                    print(f"Resultado exato: {resultado1}")
                    resultado2 = arredondamento(multiplicacao(valor1,valor2),dig)
                    print(f"Resultado com erro: {resultado2}")
                    print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1))}")
                    ans_exata = float(resultado1)
                    ans_aprox = float(resultado2)
                case '/':
                    valor1= float(arredondamento(n1,dig))
                    valor2= float(arredondamento(n2,dig))
                    resultado1 = divisao(ans_exata,n2)
                    print(f"Primeiro valor arredondado: {valor1}")
                    print(f"Segundo valor arredondado: {valor2}")
                    print(f"Resultado exato: {resultado1}")
                    resultado2 = arredondamento(divisao(valor1,valor2),dig)
                    print(f"Resultado com erro: {resultado2}")
                    print(f"Erro Absoluto: {erroAbs(float(resultado2),float(resultado1))} ; Erro Relativo: {erroRel(float(resultado2),float(resultado1))}")
                    ans_exata = float(resultado1)
                    ans_aprox = float(resultado2)

    continuar = input("Deseja continuar realizando uma nova operação? (s/n)")
    if continuar.lower() != 's':
        break
    acumular = input("Deseja acumular ultimo resultado nesta operação (s/n): ")