#Spectral subtraction
from flask import Flask, request, jsonify, render_template
import os
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/home/niveus/Desktop/flask1'

@app.route('/import-audio', methods=['GET', 'POST'])
def import_audio():
    if request.method == 'POST':
        try:
            # Check if the POST request contains a file
            if 'audio_file' not in request.files:
                return jsonify({'message': 'No file provided.'}), 400

            file = request.files['audio_file']
            if file.filename == '':
                return jsonify({'message': 'No file selected.'}), 400

            # Save the uploaded audio file to the upload folder
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

            # Process the audio file
            audio_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)

            # Load the WAV audio file using librosa
            audio, sr = librosa.load(audio_path)

            # Apply spectral subtraction for noise reduction
            n_fft = 2048  # Number of FFT points
            hop_length = 512  # Hop length for STFT
            noise_threshold = 0.1  # Adjust this threshold as needed

            # Compute the magnitude spectrogram
            stft = librosa.stft(audio, n_fft=n_fft, hop_length=hop_length)
            magnitude_spectrogram = np.abs(stft)

            # Estimate the noise floor as the median across time
            noise_floor = np.median(magnitude_spectrogram, axis=1, keepdims=True)

            # Subtract the noise floor from the magnitude spectrogram
            subtracted_spectrogram = np.maximum(0.0, magnitude_spectrogram - noise_threshold * noise_floor)

            # Reconstruct the audio signal from the modified spectrogram
            denoised_audio = librosa.istft(subtracted_spectrogram, hop_length=hop_length)

            # Save the processed audio to a specific location
            save_folder = '/home/niveus/Desktop/flask1/audio'
            save_path = os.path.join(save_folder, file.filename)
            sf.write(save_path, denoised_audio, sr)

            return jsonify({'message': 'Audio file processed successfully.'})

        except Exception as e:
            return jsonify({'message': 'An error occurred during audio processing.', 'error': str(e)}), 500

    return render_template('import_audio.html')

@app.route('/')
def home():
    return render_template("import_audio.html")


#upsampling

@app.route('/process-audio', methods=['POST'])
def upsample_audio():
    # Check if an audio file was uploaded
    if 'audio_file' not in request.files:
        return jsonify({'error': 'No audio file provided'})

    audio_file = request.files['audio_file']
    
    # Check if the file has a valid extension
    if audio_file.filename.split('.')[-1] not in ['wav', 'mp3']:
        return jsonify({'error': 'Invalid file format. Only WAV and MP3 files are supported.'})
    
    # Save the uploaded file to a temporary location
    temp_filename = 'temp_audio.' + audio_file.filename.split('.')[-1]
    audio_file.save(temp_filename)
    
    # Load the audio file using pydub
    audio = AudioSegment.from_file(temp_filename)
    
    # Perform upsampling
    target_sample_rate = audio.frame_rate * 2  # Upsample to double the sample rate
    upsampled_audio = audio.set_frame_rate(target_sample_rate)
    
    # Save the upsampled audio as a new file
    upsampled_filename = 'upsampled_' + audio_file.filename
    upsampled_audio.export(upsampled_filename, format=audio_file.filename.split('.')[-1])
    
    # Delete the temporary file
    os.remove(temp_filename)
    
    return jsonify({'message': 'Audio file successfully upsampled', 'upsampled_file': upsampled_filename})

@app.route('/process_audio')
def home1():
    return render_template("process_audio.html")

if __name__ == '__main__':
    app.run(debug=True)