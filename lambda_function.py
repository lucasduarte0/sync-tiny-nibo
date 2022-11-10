from tiny import Tiny
from nibo import Nibo
import pandas as pd
from datetime import date, time, datetime
import re
import os
from dotenv import load_dotenv

load_dotenv()

NIBO_TOKEN = os.getenv('NIBO_TOKEN')
TINY_TOKEN = os.getenv('TINY_TOKEN')

nb = Nibo(NIBO_TOKEN)
tn = Tiny(TINY_TOKEN)

def run():
    list = []

    contas = tn.getContasTiny()
    niboContas = nb.getAgendamentos()

    for i, conta in contas.iterrows():
        dict = conta.to_dict()

        stakeholderId = nb.srcForn(dict["conta.nome_cliente"])
        description = re.match(r'(?:.*nº )(\w*-\d*)',
                            dict["conta.historico"]).group()
        reference = re.search(r'(?:.*nº )(\w*-\d*)',
                            dict["conta.historico"]).group(1)

        data = {
            "stakeholderId": stakeholderId,
            "description": description,
            "reference": reference,
            "value": dict["conta.valor"],
            "scheduleDate": datetime.strptime(dict["conta.data_emissao"], "%d/%m/%Y"),
            "dueDate": datetime.strptime(dict["conta.data_vencimento"], "%d/%m/%Y"),
            "categoryId": "0ad0720a-0856-4d31-9bfe-d669a67d88e4",
        }

        data["tinyId"] = dict["conta.id"]

        # if int(dict["conta.id"]) in synced["tinyId"].values:
        if reference in niboContas["reference"].values:
            print(reference ,"Repetido")
            pass
        else:            
            res = nb.criarConta(data)
            data["niboId"] = res
            print(reference ,"OK", res)

            list.append(data)

    imported = pd.DataFrame.from_records(list)

    try:
        synced = pd.read_csv("synced.csv")
        pd.concat([synced, imported]).to_csv("synced.csv")
    except:
        imported.to_csv("synced.csv")
    


run()