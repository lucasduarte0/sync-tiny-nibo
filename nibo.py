import requests
import pandas as pd
import datetime as dt


class Nibo:
    def __init__(self, token):
        if self.token != None:
            self.token = token
        self.headers = {
            "apitoken": token,
        }

    def getForn(self):

        url = f'https://api.nibo.com.br/empresas/v1/stakeholders'
        response = requests.get(url, headers=self.headers).json()
        res = response["items"]
        df = pd.json_normalize(res)

        return df

    def srcForn(self, name):
        df = self.getForn()
        
        df = df.loc[df["name"] == name]
        id = df["id"].values
        return id[0]

    def criarForn(self, name, cnpj=""):
        url = f'https://api.nibo.com.br/empresas/v1/suppliers'

        data = {
            "name": name,
        }
        if cnpj == "":
            data["document"] = {
                "number": cnpj,
                "type": "Cnpj"
            }

        response = requests.post(url, headers=self.headers, data=data)
        print(response.text)

    def criarConta(self, data):
        url = f'https://api.nibo.com.br/empresas/v1/schedules/debit'

        response = requests.post(url, headers=self.headers, data=data)

        return response.text

    def getAgendamentos(self):
        
        url = f'https://api.nibo.com.br/empresas/v1/schedules'
        response = requests.get(url, headers=self.headers).json()
        res = response["items"]
        df = pd.json_normalize(res)

        return df


# print(nb.criarConta(data))
