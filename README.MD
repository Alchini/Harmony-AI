# Harmony AI

> Uma IA generativa de músicas instrumentais em MIDI, baseada em prompts, treinada com o Lakh MIDI Dataset usando o Magenta desenvolvida pelos alunos: Gustavo Alchini, Fernando F. Cruz e Davi A. Junkes.

---

## Visão geral

Harmony AI é um projeto para **geração automática de músicas instrumentais em formato MIDI**.  

A ideia central é permitir ao usuário criar músicas completas em diferentes estilos usando **modelos locais do Magenta (MusicVAE)** treinados com dados filtrados do **Lakh MIDI Dataset**.

Executamos nessa aplicação:

- Treinamento local de modelos MusicVAE
- Geração de novos arquivos MIDI usando os modelos treinados
- Frontend simples em HTML/CSS
- Backend em Flask para gerenciar as requisições e geração

---

## Tecnologias

- [Magenta](https://magenta.tensorflow.org/) (MusicVAE)
- [LakahMidi Dataset](https://colinraffel.com/projects/lmd/)
- TensorFlow
- Python 3.x
- Flask
- HTML/CSS (FontAwesome)

---

## Como funciona

1️⃣ **Pré-processamento**  
- Classificação do Lakh MIDI Dataset para separar apenas arquivos de Rock.
- Conversão dos arquivos MIDI em formato TFRecord.

2️⃣ **Treinamento**  
- Fine-tuning dos modelos pré-treinados do Magenta (MusicVAE).
- Modelos utilizados:
  - `cat-mel_2bar_small`
  - `hierdec-trio_16bar`
- Checkpoints salvos localmente.

3️⃣ **Geração**  
- Backend Flask roda comandos do `music_vae_generate` com os checkpoints treinados.
- Gera arquivos MIDI salvos na biblioteca.

4️⃣ **Frontend**  
- `index.html`: formulário para enviar o prompt.
- `results.html`: exibe as músicas geradas com opção de download.

---
##  Dependências

Crie e ative um ambiente virtual:

```bash
python -m venv env
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows
```

Instale as dependências principais:
```bash
pip install magenta flask tensorflow
```
---

## Como treinar um modelo (opcional)

Transforme os arquivos MIDI em TFRecord:

```bash
python -m magenta.scripts.convert_dir_to_note_sequences \
  --input_dir="CAMINHO_PARA_MIDIS" \
  --output_file="CAMINHO_PARA_SAIDA/arquivo.tfrecord"

```

Treine o modelo MusicVAE:

```bash
    music_vae_train \
  --config=hierdec-trio_16bar \
  --run_dir="CAMINHO_PARA_CHECKPOINTS/rock_model" \
  --mode=train \
  --num_steps=2000 \
  --train_examples_path="CAMINHO_PARA_TFRECORD/arquivo.tfrecord"

```
---

##  Como rodar localmente

1️⃣ Clone o repositório


```bash
git clone https://github.com/seuusuario/harmony-ai.git
cd harmony-ai
```
2️⃣ Instale as dependências

```bash
pip install -r requirements.txt
```

3️⃣ Baixe e extraia um modelo pré-treinado caso não queira treinar um

- [cat-mel_2bar_big](https://storage.googleapis.com/magentadata/models/music_vae/checkpoints/cat-mel_2bar_big.tar)

4️⃣ Organize os checkpoints e
garanta a estrutura:

```bash
checkpoints/
    rock_model/
    general_model/
```
5️⃣Aponte o caminho e modelo correto para o checkpoint em app.py:

```bash
checkpoint_file = "C:/tmp/music_vae/train/general/cat-mel_2bar_big.ckpt"
    config = "cat-mel_2bar_big"
```

6️⃣ Rode o servidor Flask
```bash
python app.py
```

7️⃣ Acesse no navegador

```bash
http://localhost:5000
```
---

## Uso

✅ Página inicial (/):

- Digite um prompt descritivo (ex.: "Heavy Metal Tribal Agressivo com Solo de Guitarra").

- Clique em Criar Música.

✅ Página de resultados (/library):

- Veja as músicas geradas.

- Baixe os arquivos MIDI.

⚠️ Observação: no estado atual, o prompt não altera o estilo gerado — ele é apenas usado para nomear o arquivo. A geração real depende do checkpoint selecionado no trecho encontrado no arquivo app.py na linha 40:

```bash
checkpoint_file = "C:/tmp/music_vae/train/general/hierdec-trio_16bar.ckpt"
    config = "hierdec-trio_16bar"
```

---

## Personalização

- Edite o caminho do checkpoint no app.py para trocar o modelo.

- Adicione novos modelos para outros estilos.

- Expanda o frontend para exibir mais metadados.

- Implemente parsing real do prompt para escolha automática de estilo/modelo.
