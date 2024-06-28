import pandas as pd
from hmmlearn import hmm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
from variaveis import *
import numpy as np

# Carrega os dados processados
file_path = CSV_PROCESSED_FILENAME
data = pd.read_csv(file_path)

# Prepara os dados de observacao
observations = data[['packet_loss_rate_bidir', 'source_code', 'destination_code']].values

# Dividi os dados em treino, validação e teste
train_data, test_data = train_test_split(observations, test_size=0.2, random_state=42)
train_data, val_data = train_test_split(train_data, test_size=0.25, random_state=42)  # pois 0.25 * 0.8 = 0.2

# Funcao para treinar o modelo HMM e encontrar os melhores hiperparametros
def find_best_hmm(train_data, val_data, n_states_list, min_covar=1e-1):
    best_model = None
    best_score = float('-inf')
    best_n_states = None
    for n_states in n_states_list:
        model = hmm.GaussianHMM(n_components=n_states, covariance_type="diag", n_iter=2000, min_covar=min_covar, init_params="stmc")
        try:
            model.fit(train_data)
            score = model.score(val_data)
            if score > best_score:
                best_score = score
                best_model = model
                best_n_states = n_states
        except ValueError as e:
            print(f"Erro ao treinar modelo com {n_states} estados: {e}")
    return best_model, best_n_states

# Funcao para calcular acuracia
def evaluate_model(model, train_data, test_data):
    predicted_train_states = model.predict(train_data)
    predicted_test_states = model.predict(test_data)
    accuracy = accuracy_score(predicted_train_states[:len(predicted_test_states)], predicted_test_states)
    return accuracy

if __name__ == "__main__":
    # Lista de possiveis numeros de estados ocultos
    n_states_list = [2, 3, 4, 5]

    # Encontra os melhores hiperparametros com validacao cruzada
    best_model, best_n_states = find_best_hmm(train_data, val_data, n_states_list)
    print(f"Melhor número de estados ocultos: {best_n_states}")

    # Re-treina o melhor modelo com todos os dados de treinamento (treino + validacao)
    final_train_data = np.vstack((train_data, val_data))
    final_model = hmm.GaussianHMM(n_components=best_n_states, covariance_type="diag", n_iter=2000, min_covar=1e-1, init_params="stmc")
    final_model.fit(final_train_data)

    # Avalia o modelo no conjunto de TESTE
    test_score = final_model.score(test_data)
    print(f"Log-likelihood: {test_score}")

    # Calcula acuracia
    accuracy = evaluate_model(final_model, final_train_data, test_data)
    print(f"Acuracia: {accuracy}")

    model_path = 'hmm_model.pkl'
    with open(model_path, 'wb') as file:
        pickle.dump(final_model, file)

    print(f"Modelo HMM treinado e salvo em '{model_path}'.")
