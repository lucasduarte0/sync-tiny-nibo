import requests
import pandas as pd
# import nibo as nb

class Tiny:
    def __init__(self, token):
        self.token = token   
        self.params={
            "formato": "json",
            "token": token,
        }   

    def getContasTiny(self, situacao="aberto"):

        url = "https://api.tiny.com.br/api2/contas.pagar.pesquisa.php"

        params = self.params
        params["situacao"] = situacao

        res = requests.request("GET", url, params=params).json()
        res = res["retorno"]["contas"]
        df = pd.json_normalize(res)

        return df

