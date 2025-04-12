import investpy

api_key = 'D2HKJ58H2UOHYFTS'

# Obter dados de ação
df = investpy.obter_dados_acao('GOOG', api_key)

# Calcular retorno diário
df = investpy.calcular_retorno_diario(df)

# Plotar dados da ação
investpy.plotar_dados_acao(df)
