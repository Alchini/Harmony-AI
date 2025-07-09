import os
import subprocess
import glob
from flask import Flask, request, render_template, send_from_directory
from datetime import datetime

app = Flask(__name__, static_folder='static')

GENERATED_FOLDER = os.path.join(app.static_folder, 'generated')
os.makedirs(GENERATED_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/library')
def library():
    all_midi_paths = glob.glob(os.path.join(GENERATED_FOLDER, '*.mid'))
    
    all_midi_paths.sort(key=os.path.getmtime, reverse=True)

    results = []
    for file_path in all_midi_paths:
        file_name = os.path.basename(file_path)
        readable_name = "Música " + file_name.replace('_', ' ').replace('.mid', '')
        results.append({
            'name': readable_name,
            'url': f'/static/generated/{file_name}'
        })

    return render_template('results.html', results=results, prompt="Sua Biblioteca")


@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form.get('prompt-input')
    if not prompt:
        return "Erro: O prompt não pode ser vazio.", 400

    checkpoint_file = "C:/tmp/music_vae/train/general/hierdec-trio_16bar.ckpt"
    config = "hierdec-trio_16bar"
    num_outputs = 1 # Quantidade de musicas a gerar

    print(f"Gerando {num_outputs} músicas para o prompt: '{prompt}'...")

    try:
        temp_output_dir = os.path.join(GENERATED_FOLDER, 'temp_generation')
        os.makedirs(temp_output_dir, exist_ok=True)
        
        # Limpa
        for f in glob.glob(os.path.join(temp_output_dir, '*.mid')):
            os.remove(f)

        command = [
            'music_vae_generate', f'--config={config}', f'--checkpoint_file={checkpoint_file}',
            '--mode=sample', f'--num_outputs={num_outputs}', f'--output_dir={temp_output_dir}'
        ]
        subprocess.run(command, check=True, shell=True)
        
        # ATUALIZAÇÃO: Renomeia os arquivos gerados para garantir que sejam únicos
        generated_files = glob.glob(os.path.join(temp_output_dir, '*.mid'))
        timestamp_prefix = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        final_results = []
        for i, file_path in enumerate(generated_files):
            new_file_name = f"{timestamp_prefix}_{i}.mid"
            new_file_path = os.path.join(GENERATED_FOLDER, new_file_name)
            os.rename(file_path, new_file_path)

            # ATUALIZAÇÃO: O título da música agora é o prompt
            final_results.append({
                'name': f"{prompt} #{i + 1}",
                'url': f'/static/generated/{new_file_name}'
            })

        # Remove a pasta temporária
        os.rmdir(temp_output_dir)

        print("Músicas geradas e salvas na biblioteca com sucesso.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return "Ocorreu um erro interno ao tentar gerar a música.", 500

    # Mostra a página de resultados apenas com as músicas que acabaram de ser criadas
    return render_template('results.html', results=final_results, prompt=prompt)


if __name__ == '__main__':
    app.run(debug=True, port=5000)