# Casos de Teste para Validação do Simulador de Erros Numéricos

## Configuração da Máquina Hipotética
- **Precisão:** t = 4 dígitos significativos
- **Métodos:** Truncamento e Arredondamento

---

## Exemplo 1: Operação Simples (Soma)

### Dados de Entrada
- **Valor 1:** 0.12345 (5 casas decimais)
- **Valor 2:** 0.67890 (5 casas decimais)
- **Dígitos de Precisão:** 4

### Cálculo Exato
```
0.12345 + 0.67890 = 0.80235
```

### Análise com Truncamento (k=4)
1. **Valores Aproximados:**
   - x_aprox = 0.1234 (truncamento)
   - y_aprox = 0.6789 (truncamento)

2. **Operação:**
   - Resultado Aprox = 0.1234 + 0.6789 = 0.8023

3. **Erros:**
   - Erro Absoluto: |0.80235 - 0.8023| = 0.00005
   - Erro Relativo: |0.00005 / 0.80235| = 0.0000623 (0.00623%)

### Análise com Arredondamento (k=4)
1. **Valores Aproximados:**
   - x_aprox = 0.1235 (arredondamento)
   - y_aprox = 0.6789 (arredondamento)

2. **Operação:**
   - Resultado Aprox = 0.1235 + 0.6789 = 0.8024

3. **Erros:**
   - Erro Absoluto: |0.80235 - 0.8024| = 0.00005
   - Erro Relativo: |0.00005 / 0.80235| = 0.0000623 (0.00623%)

### Resultados Esperados
- **Truncamento:** 0.8023, Erro Absoluto: 0.00005, Erro Relativo: 0.00623%
- **Arredondamento:** 0.8024, Erro Absoluto: 0.00005, Erro Relativo: 0.00623%

---

## Exemplo 2: Propagação de Erro e Cancelamento Subtrativo

### Dados de Entrada
- **Valor 1:** 0.76545
- **Valor 2:** 0.76541
- **Operação:** Subtração (x - y)
- **Dígitos de Precisão:** 4

### Cálculo Exato
```
0.76545 - 0.76541 = 0.00004 (4.0 × 10⁻⁵)
```

### Análise com Truncamento (k=4)
1. **Valores Aproximados:**
   - x_aprox = 0.7654 (truncamento)
   - y_aprox = 0.7654 (truncamento)

2. **Operação:**
   - Resultado Aprox = 0.7654 - 0.7654 = 0.0000

3. **Erros:**
   - Erro Absoluto: |0.00004 - 0.0000| = 0.00004
   - Erro Relativo: ∞ (divisão por zero no resultado aproximado)

### Análise com Arredondamento (k=4)
1. **Valores Aproximados:**
   - x_aprox = 0.7655 (arredondamento do 5º dígito)
   - y_aprox = 0.7654 (arredondamento)

2. **Operação:**
   - Resultado Aprox = 0.7655 - 0.7654 = 0.0001

3. **Erros:**
   - Erro Absoluto: |0.00004 - 0.0001| = 0.00006
   - Erro Relativo: |0.00006 / 0.00001| = 0.6 (60%)

### Resultados Esperados
- **Truncamento:** 0.0000, Erro Absoluto: 0.00004, Erro Relativo: ∞
- **Arredondamento:** 0.0001, Erro Absoluto: 0.00006, Erro Relativo: 60%

### Observação
Este exemplo demonstra dramaticamente como a subtração de números muito próximos pode levar à perda total de dígitos significativos, resultando em erro relativo extremamente alto ou mesmo resultado nulo.

---

## Exemplo 3: Propagação de Erro em Sequência de Somas

### Dados de Entrada
- **Valor:** 0.56786
- **Número de Somas:** 10
- **Dígitos de Precisão:** 4

### Cálculo Exato
```
10 × 0.56786 = 5.6786
```

### Análise com Truncamento (k=4)

#### Passo a Passo:
1. **Soma 1:** 0.0000 + 0.56786 = 0.56786 → Truncado: 0.5678
2. **Soma 2:** 0.5678 + 0.56786 = 1.13566 → Truncado: 1.135
3. **Soma 3:** 1.135 + 0.56786 = 1.70286 → Truncado: 1.702
4. **Soma 4:** 1.702 + 0.56786 = 2.26986 → Truncado: 2.269
5. **Soma 5:** 2.269 + 0.56786 = 2.83686 → Truncado: 2.836
6. **Soma 6:** 2.836 + 0.56786 = 3.40386 → Truncado: 3.403
7. **Soma 7:** 3.403 + 0.56786 = 3.97086 → Truncado: 3.970
8. **Soma 8:** 3.970 + 0.56786 = 4.53786 → Truncado: 4.537
9. **Soma 9:** 4.537 + 0.56786 = 5.10486 → Truncado: 5.104
10. **Soma 10:** 5.104 + 0.56786 = 5.67186 → Truncado: 5.671

#### Resultados:
- **Valor Exato:** 5.6786
- **Resultado Aproximado:** 5.671
- **Erro Absoluto:** |5.6786 - 5.671| = 0.0076
- **Erro Relativo:** |0.0076 / 5.6786| = 0.001338 (0.1338%)

### Análise com Arredondamento (k=4)

#### Passo a Passo:
1. **Soma 1:** 0.0000 + 0.56786 = 0.56786 → Arredondado: 0.5679
2. **Soma 2:** 0.5679 + 0.56786 = 1.13576 → Arredondado: 1.136
3. **Soma 3:** 1.136 + 0.56786 = 1.70386 → Arredondado: 1.704
4. **Soma 4:** 1.704 + 0.56786 = 2.27186 → Arredondado: 2.272
5. **Soma 5:** 2.272 + 0.56786 = 2.83986 → Arredondado: 2.840
6. **Soma 6:** 2.840 + 0.56786 = 3.40786 → Arredondado: 3.408
7. **Soma 7:** 3.408 + 0.56786 = 3.97586 → Arredondado: 3.976
8. **Soma 8:** 3.976 + 0.56786 = 4.54386 → Arredondado: 4.544
9. **Soma 9:** 4.544 + 0.56786 = 5.11186 → Arredondado: 5.112
10. **Soma 10:** 5.112 + 0.56786 = 5.67986 → Arredondado: 5.680

#### Resultados:
- **Valor Exato:** 5.6786
- **Resultado Aproximado:** 5.680
- **Erro Absoluto:** |5.6786 - 5.680| = 0.0014
- **Erro Relativo:** |0.0014 / 5.6786| = 0.000246 (0.0246%)

### Resultados Esperados
- **Truncamento:** 5.671, Erro Absoluto: 0.0076, Erro Relativo: 0.1338%
- **Arredondamento:** 5.680, Erro Absoluto: 0.0014, Erro Relativo: 0.0246%

---
