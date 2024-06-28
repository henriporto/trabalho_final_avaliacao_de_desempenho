import requests
import csv
import os
import urllib3
from variaveis import *

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

csv_filename = CSV_INITIAL_DATA_FILENAME
if not os.path.isfile(csv_filename):
    with open(csv_filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['source', 'destination', 'packet_loss_rate_bidir', 'timestamp'])

prefixos = [
    "ac",
    "al",
    "am",
    "ap",
    "ba",
    "ce",
    "df",
    "es",
    "go",
    "ma",
    "mg",
    "ms",
    "mt",
    "pa",
    "pb",
    "pe",
    "pi",
    "pr",
    "rj",
    "rn",
    "ro",
    "rr",
    "rs",
    "sc",
    "se",
    "sp",
    "to"
]

for prefixo_fonte in prefixos:
    for prefixo_destino in prefixos:
        if prefixo_fonte != prefixo_destino:
                url = f"https://monipe-central.rnp.br/esmond/perfsonar/archive/?event-type=packet-loss-rate-bidir&source=monipe-{prefixo_fonte}-atraso.rnp.br&destination=monipe-{prefixo_destino}-atraso.rnp.br&time-range=86400"
                response = requests.get(url, verify=False)
                if response.status_code == 200:
                    data = response.json()
                    metadata_keys = [item["metadata-key"] for item in data]
                    for metadata_key in metadata_keys:
                        url = f"https://monipe-central.rnp.br/esmond/perfsonar/archive/{metadata_key}/packet-loss-rate-bidir/base?limit=1000000000"
                        response = requests.get(url, verify=False)
                        if response.status_code == 200:
                            packet_loss_rate_bidir_data = response.json()
                            with open(csv_filename, 'a', newline='') as csvfile:
                                csvwriter = csv.writer(csvfile)
                                for entry in packet_loss_rate_bidir_data:
                                    ts = entry.get("ts")
                                    val = entry.get("val")
                                    csvwriter.writerow([prefixo_fonte, prefixo_destino, val, ts])
                            print(f"Dado salvo em {csv_filename} para {prefixo_fonte} -> {prefixo_destino}")
                        else:
                            print(f"Falha ao recuperar packet_loss_rate_bidir para a metadata_key: {metadata_key}. HTTP Status code: {response.status_code}")
                else:
                    print(f"Falha ao recuperar prefixo fonte: {prefixo_fonte}, prefixo destino: {prefixo_destino}. HTTP Status code: {response.status_code}")