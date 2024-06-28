# Predição de Perda de Pacotes utilizando Modelos Ocultos de Markov (Hidden Markov Model - HMM)

## Setup do Ambiente

1. **Criar e Ativar o Ambiente Virtual:**
   ```bash
   python -m venv myenv
   myenv\Scripts\Activate
   ```

2. **Instalar as Dependências:**
   ```bash
   python -m pip install -r .\requirements.txt
   ```

## Ordem de Execução dos Scripts

1. **Download dos Dados:**
   Executa o script para coletar dados da API Esmond.
   ```bash
   python download_dados.py
   ```

2. **Pré-processamento dos Dados:**
   Executa o script para processar os dados brutos.
   ```bash
   python preprocessamento.py
   ```

3. **Treinamento do Modelo:**
   Executa o script para treinar o modelo de Cadeia de Markov Oculta (HMM).
   ```bash
   python treinamento.py
   ```

4. **Predição de Futuras Taxas de Perda de Pacotes:**
   Executa o script para fazer previsões usando o modelo treinado.
   ```bash
   python predicao.py
   ```