import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
import io

def home(request):
    # Definir os símbolos das ações
    simbolos = ['^BVSP', 'PETR4.SA', 'VALE3.SA', 'ITUB4.SA']

    # Definir o intervalo de tempo dos dados históricos
    data_inicio = '2016-01-01'
    data_fim = '2023-04-18'

    # Obter os dados históricos de preços de ações da B3
    precos = yf.download(simbolos, start=data_inicio, end=data_fim)['Adj Close']

    # Definir o saldo inicial e as proporções de cada ação na carteira
    saldo_inicial = 4000
    proporcoes = {'^BVSP': 0.25, 'PETR4.SA': 0.25, 'VALE3.SA': 0.25, 'ITUB4.SA': 0.25}

    # Calcular o número de ações que cada proporção representa no saldo inicial
    precos_atual = {'^BVSP': precos.iloc[-1]['^BVSP'], 'PETR4.SA': precos.iloc[-1]['PETR4.SA'], 'VALE3.SA': precos.iloc[-1]['VALE3.SA'], 'ITUB4.SA': precos.iloc[-1]['ITUB4.SA']}
    num_acoes = {}
    for simbolo, proporcao in proporcoes.items():
        num_acoes[simbolo] = int((saldo_inicial * proporcao) / precos_atual[simbolo])

    # Simular o crescimento da carteira até 2023
    anos = range(2016, 2024)
    saldo = [saldo_inicial]
    for ano in anos[1:]:
        # Calcular o valor atual da carteira
        valor_atual = 0
        for simbolo, num in num_acoes.items():
            valor_atual += num * precos_atual[simbolo]
        saldo.append(valor_atual)

        # Calcular o novo número de ações de cada ação na carteira
        for simbolo, proporcao in proporcoes.items():
            num_acoes[simbolo] = int((valor_atual * proporcao) / precos_atual[simbolo])

    # Plotar o gráfico do crescimento da carteira
    plt.plot(anos, saldo)
    plt.xlabel('Ano')
    plt.ylabel('Saldo (em reais)')
    plt.title('Crescimento da carteira de 2016 a 2023')

    # Salvar o gráfico em um buffer de memória
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Converter o buffer de memória em um objeto de imagem do Django
    string = buf.getvalue()

    return render(request, 'home.html', {'imagem': string})
