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
   ```bash
   python download_dados.py
   ```

2. **Pré-processamento dos Dados:**
   ```bash
   python preprocessamento.py
   ```

3. **Treinamento do Modelo:**
   ```bash
   python treinamento.py
   ```

4. **Predição de Futuras Taxas de Perda de Pacotes:**
   ```bash
   python predicao.py
   ```