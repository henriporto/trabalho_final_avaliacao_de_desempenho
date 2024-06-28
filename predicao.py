import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import MinMaxScaler
from variaveis import *

def predict_future_loss(model, observations, n_predictions=10):
    hidden_states = model.predict(observations)

    # Prevendo o proximo estado com base na matriz de transicao c:
    last_state = hidden_states[-1]
    predicted_states = []
    for _ in range(n_predictions):
        next_state = np.argmax(model.transmat_[last_state])
        predicted_states.append(next_state)
        last_state = next_state

    # Converte os estados previstos pra taxas de perda de pacotes usando a matriz de emissao
    predicted_loss_rates = model.means_[predicted_states]
    return predicted_loss_rates

if __name__ == "__main__":
    file_path = CSV_PROCESSED_FILENAME
    data = pd.read_csv(file_path)

    # Carrega os mapeamentos de source e destination feitos no preprocessamento
    source_mapping = pd.read_csv(CSV_SOURCE_MAPPING, index_col='source')
    destination_mapping = pd.read_csv(CSV_DESTINATION_MAPPING, index_col='destination')

    source = input("Digite o source: ")
    destination = input("Digite o destination: ")

    # Converte source e destination para codigos numericos
    source_code = source_mapping.loc[source, 'source_code']
    destination_code = destination_mapping.loc[destination, 'destination_code']

    # Aplica normalizacao p/ source_code e destination_code
    scaler = MinMaxScaler()
    scaler.fit(data[['source_code', 'destination_code']])
    input_data = pd.DataFrame([[source_code, destination_code]], columns=['source_code', 'destination_code'])
    normalized_input = scaler.transform(input_data)
    source_code_norm = normalized_input[0][0]
    destination_code_norm = normalized_input[0][1]
    filtered_data = data[(data['source_code'] == source_code_norm) & (data['destination_code'] == destination_code_norm)]

    if filtered_data.empty:
        raise ValueError(f"Nenhum dado encontrado para a combinacao {source} -> {destination}")

    # Prepara os dados de observação
    observations = filtered_data[['packet_loss_rate_bidir', 'source_code', 'destination_code']].values

    # Carrega o modelo treinado
    with open(MODEL_FILENAME, 'rb') as file:
        model = pickle.load(file)

    # Prediz as proximas n observacoes
    n_steps_ahead = int(input("Insira o numero de intervalos de 5 minutos para prever: "))
    predicted_loss_rates = predict_future_loss(model, observations, n_predictions=n_steps_ahead)
    print(predicted_loss_rates)
