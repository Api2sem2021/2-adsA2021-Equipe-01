import json

from psycopg2 import connect
from psycopg2.extras import Json

# Abrindo o arquivo.
trello_json_file = open(file='trello.json')

# Lendo o arquivo como Json.
trello_data = json.load(trello_json_file)

# Fechando o arquivo, visto que ele não é mais necessário.
trello_json_file.close()

# CONVERTENDO

trello_list = []

for item in trello_data:
    trello_details = {"id": None, "status": None, "usuario_id": None, "usuario_avatar": None, "usuario_first_name": None, "usuario_last_name": None, "usuario_email": None,
                      "amounthours": None, "startedat": None, "finished": None, "project": None, "carddescription": None, "gitmetadata_branch": None, "gitmetadata_hash": None}
    trello_details["id"] = item["_id"]
    trello_details["status"] = item["status"]
    trello_details["usuario_id"] = item["user"]["_id"]
    trello_details["usuario_avatar"] = item["user"]["avatar"]
    trello_details["usuario_first_name"] = item["user"]["userName"]
    trello_details["usuario_last_name"] = item["user"]["userLastName"]
    trello_details["usuario_email"] = item["user"]["userEmail"]
    trello_details["amounthours"] = item["hours"]
    if item["hours"] == None:
        trello_details["amounthours"] = 0
    trello_details["startedat"] = item["startedAt"]
    trello_details["finished"] = item["isFinished"]
    trello_details["project"] = item["project"]
    trello_details["carddescription"] = item["cardDescription"]
    trello_details["gitmetadata_branch"] = item["gitMetadata"]["branch"]
    trello_details["gitmetadata_hash"] = item["gitMetadata"]["hash"]
    trello_list.append(trello_details)

# Criando arquivo do trello
with open('trello_formatted.json', 'w') as f:
    json.dump(trello_list, f, ensure_ascii=False)


# Verificando quantidades

status_tags = ['DONE', 'FOR_TEST', 'IN_PROGRESS', 'RELEASE_TO_PROD', 'PROD_DEPLOYING', 'QA_DEPLOYING', 'QA_TESTING']
ks = 0
ttl = len(status_tags)
i = 0
trello_status_quant = []
tot = len(trello_list)
while ks < ttl:
  k = 0
  q = 0
  while k < tot:

    palavras_procuradas = {status_tags[ks]}
    texto = [trello_list[k]["status"]]


    dicionario = {}
    for palavra in texto:
        if palavra in palavras_procuradas:
            count = 1
            if palavra in dicionario:
              count = int(dicionario[palavra].split(' ')[-1]) + 1;
            dicionario[palavra] = palavra + " " + str(count)
          

    for palavra in palavras_procuradas:
      if palavra not in texto:
        dicionario[palavra] = palavra + " " + str(0)

    for chave in dicionario:
        if(dicionario[palavra] == palavra + " " + str(1)):
          q = q + 1
    k = k + 1
  ks = ks + 1

  trello_q = {chave: None}
  trello_q [chave] = q
  trello_status_quant.append(trello_q)


# Criando arquivo com quantidades
with open('trello_q.json', 'w') as f:
    json.dump(trello_status_quant, f, ensure_ascii=False)
