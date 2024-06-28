import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from variaveis import *
import numpy as np

file_path = CSV_INITIAL_DATA_FILENAME
data = pd.read_csv(file_path)

# Converte timestamp de segundos epoch para datetime
data['timestamp'] = pd.to_datetime(data['timestamp'], unit='s')

# Determina a maior data minima e a menor data maxima entre TODOS os conjuntos
min_dates = data.groupby(['source', 'destination'])['timestamp'].min()
max_dates = data.groupby(['source', 'destination'])['timestamp'].max()

common_min_date = min_dates.max()
common_max_date = max_dates.min()

print(f"Maior data minima comum: {common_min_date}")
print(f"Menor data maxima comum: {common_max_date}")

# Agrega os dados a cada 5 minutos e calcula a taxa maxima de perda de pacotes
def aggregate_data(df):
    df = df.set_index('timestamp')
    df_resampled = df.resample('5min').max().reset_index()
    df_resampled = df_resampled.fillna({'packet_loss_rate_bidir': 0})  # Preenche valores q faltam com zero
    return df_resampled

# Aplica a agregacao para cada combinacao (source, destination) dentro do intervalo
aggregated_data = []

for name, group in data.groupby(['source', 'destination']):
    group = group[(group['timestamp'] >= common_min_date) & (group['timestamp'] <= common_max_date)]
    aggregated_group = aggregate_data(group)
    aggregated_group['source'] = name[0]
    aggregated_group['destination'] = name[1]
    aggregated_data.append(aggregated_group)

result_data = pd.concat(aggregated_data, ignore_index=True)

# Transforma em binario a taxa de perda de pacotes
result_data['packet_loss_rate_bidir'] = np.where(result_data['packet_loss_rate_bidir'] >= 0.1, 1, 0)

# Codifica source e destination como numeros
result_data['source_code'] = result_data['source'].astype('category').cat.codes.astype(float)
result_data['destination_code'] = result_data['destination'].astype('category').cat.codes.astype(float)

# Normaliza os dados
scaler = MinMaxScaler()
result_data[['source_code', 'destination_code']] = scaler.fit_transform(result_data[['source_code', 'destination_code']])

# Salva os mapeamentos de source e destination normalizados (pra usar depois na predicao)
source_mapping = result_data[['source', 'source_code']].drop_duplicates().set_index('source')
destination_mapping = result_data[['destination', 'destination_code']].drop_duplicates().set_index('destination')

source_mapping.to_csv(CSV_SOURCE_MAPPING)
destination_mapping.to_csv(CSV_DESTINATION_MAPPING)

# Reordena as colunas para as features finais e remove a coluna timestamp
result_data_final = result_data[['packet_loss_rate_bidir', 'source_code', 'destination_code']]

result_data_final.to_csv(CSV_PROCESSED_FILENAME, index=False)
print(f"Dados processados salvos em {CSV_PROCESSED_FILENAME}.")
