import pandas as pd

class Tratamento:
    def __init__(self):
        self.usuarios = pd.read_csv("Dados/users.csv")
        self.precos = pd.read_csv("Dados/prices.csv")
        self.velocidade = pd.read_csv("Dados/avgspeed.csv")

    def unifica_dados(self):
        self.dados_unificados = self.precos.set_index("Name")\
            .join(self.usuarios.set_index("Country or area"))\
            .join(self.velocidade.set_index("Country"))
        return self.dados_unificados

    def tratamento_dados(self):
        self.dados_unificados = self.dados_unificados.dropna(subset=["Population"])
        self.dados_unificados["Internet users"] = self.dados_unificados["Internet users"].str.replace(",","").apply(pd.to_numeric, errors="coerce")
        self.dados_unificados["Population"] = self.dados_unificados["Population"].str.replace(",", "").apply(pd.to_numeric, errors="coerce")
        self.dados_unificados["Average price of 1GB (USD)"] = self.dados_unificados["Average price of 1GB (USD)"].str.replace("$", "", regex=False).apply(pd.to_numeric, errors="coerce")
        self.dados_unificados["Cheapest 1GB for 30 days (USD)"] = self.dados_unificados["Cheapest 1GB for 30 days (USD)"].str.replace("$", "", regex=False).apply(pd.to_numeric,errors="coerce")
        self.dados_unificados["Most expensive 1GB (USD)"] = self.dados_unificados["Most expensive 1GB (USD)"].str.replace("$", "", regex=False).apply(pd.to_numeric, errors="coerce")
        self.dados_unificados["Average price of 1GB (USD  at the start of 2021)"] = self.dados_unificados["Average price of 1GB (USD  at the start of 2021)"].str.replace("$", "", regex=False).apply(pd.to_numeric, errors="coerce")
        self.dados_unificados["Average price of 1GB (USD – at start of 2020)"] = self.dados_unificados["Average price of 1GB (USD – at start of 2020)"].str.replace("$", "", regex=False).apply(pd.to_numeric,errors="coerce")
        self.dados_unificados = self.dados_unificados.dropna(subset=["Average price of 1GB (USD)"])
        self.dados_unificados = self.dados_unificados.dropna(subset=["Cheapest 1GB for 30 days (USD)"])
        self.dados_unificados = self.dados_unificados.dropna(subset=["Most expensive 1GB (USD)"])
        self.dados_unificados = self.dados_unificados.dropna(subset=["Average price of 1GB (USD  at the start of 2021)"])
        self.dados_unificados = self.dados_unificados.dropna(subset=["Average price of 1GB (USD – at start of 2020)"])
            # occur = self.dados_unificados[self.dados_unificados["Avg \n(Mbit/s)Ookla"]].isna()
            # occur2 = occur.groupby(['Region']).size()

        Tratamento.analise_planos(self)
        Tratamento.analise_preco(self)
        Tratamento.plano_preco(self)
        Tratamento.real_dolar(self)
        Tratamento.renomeia(self)

        return self.dados_unificados

    def analise_planos(self):
        mediana = self.dados_unificados["NO. OF Internet Plans "].median()
        self.dados_unificados["AnaliseQuantidadePlanos"] = self.dados_unificados.apply(lambda row: "Muito" if row["NO. OF Internet Plans "] >= mediana else "Pouco", axis=1)
        return self.dados_unificados

    def analise_preco(self):
        mediana = self.dados_unificados["Average price of 1GB (USD)"].median()
        self.dados_unificados["AnalisePrecoMedio"] = self.dados_unificados.apply(
            lambda row: "Caro" if row["Average price of 1GB (USD)"] >= mediana else "Barato", axis=1)
        return self.dados_unificados

    def plano_preco(self):
        self.dados_unificados["PerfilPlanoPreco"] = self.dados_unificados.apply(
            lambda row: row["AnaliseQuantidadePlanos"] + row["AnalisePrecoMedio"], axis=1)
        #occur = self.dados_unificados.groupby('PerfilPlanoPreco').mean()
        return self.dados_unificados

    def real_dolar(self):
        self.dados_unificados[["Average price of 1GB (USD)"]] = self.dados_unificados[
            ["Average price of 1GB (USD)"]].apply(lambda x: round(x * 5, 2))
        self.dados_unificados[["Cheapest 1GB for 30 days (USD)"]] = self.dados_unificados[
            ["Cheapest 1GB for 30 days (USD)"]].apply(lambda x: round(x * 5, 2))
        self.dados_unificados[["Most expensive 1GB (USD)"]] = self.dados_unificados[["Most expensive 1GB (USD)"]].apply(
            lambda x: round(x * 5, 2))
        self.dados_unificados[["Average price of 1GB (USD  at the start of 2021)"]] = self.dados_unificados[
            ["Average price of 1GB (USD  at the start of 2021)"]].apply(lambda x: round(x * 5, 2))
        self.dados_unificados[["Average price of 1GB (USD – at start of 2020)"]] = self.dados_unificados[
            ["Average price of 1GB (USD – at start of 2020)"]].apply(lambda x: round(x * 5, 2))
        return self.dados_unificados

    def renomeia(self):
        self.dados_unificados.columns.values[0] = 'Pais'
        self.dados_unificados = self.dados_unificados.rename(
            columns={
                     'Country code': 'Codigo',
                     'Continental region': 'Regiao Continental',
                     'NO. OF Internet Plans ': 'Numero de Planos',
                     'Average price of 1GB (USD)': 'Preco medio de 1GB',
                     'Cheapest 1GB for 30 days (USD)': '1GB mais barato',
                     'Most expensive 1GB (USD)': '1GB mais caro',
                     'Average price of 1GB (USD  at the start of 2021)': 'Preco medio de 1GB desde 2021',
                     'Average price of 1GB (USD – at start of 2020)': 'Preco medio de 1GB desde 2020',
                     'Subregion': 'Subcontinente',
                     'Region': 'Continente',
                     'Internet users': 'Numero de Usuarios',
                     'Population': 'Populacao',
                     'Avg \n(Mbit/s)Ookla': 'Velocidade media',
                     'AnaliseQuantidadePlanos': 'Numero de Plano Qualitativo',
                     'AnalisePrecoMedio': 'Preco medio de 1GB Qualitativo',
                     'PerfilPlanoPreco': 'Perfil de Plano e Preco'}
        )
        return self.dados_unificados

    def salva(self):
        self.dados_unificados.to_csv('Dados/dadostratados.csv')
        self.dados_unificados.to_pickle('Dados/dados_unificado2.pkl')
        self.dados_unificados.to_pickle('Dados/dados_unificado3.gz')