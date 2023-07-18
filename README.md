# CleaningAudioFiles


For Spectral Subtraction:

This code sets up a Flask web application with an `/import-audio` route to handle audio file uploads and processing. The uploaded audio file is saved to a specified folder, and then spectral subtraction is applied to reduce noise in the audio.

Specifically, when a POST request is made to the `/import-audio` route, it checks if a file is provided. If no file is provided, it returns an error message. If a file is provided, it saves the file to the upload folder specified in the configuration.

Next, the code uses the `librosa` library to load the audio file and performs spectral subtraction. Spectral subtraction involves computing the magnitude spectrogram of the audio signal, estimating the noise floor, and subtracting the noise floor from the spectrogram.

After applying spectral subtraction, the denoised audio is reconstructed from the modified spectrogram. It is then saved to a specific location in the `save_folder`.

If any errors occur during the audio processing, an error message is returned with a 500 status code. Otherwise, a success message is returned.

The home route `/` renders the `import_audio.html` template, allowing users to upload audio files via the web application.



For Upsampling:
This code sets up a Flask web application with a `/process-audio` route to handle audio file upsampling. The route only accepts POST requests.

When a POST request is made to the `/process-audio` route, it checks if an audio file was uploaded. If no file is provided, an error message is returned.

If a valid audio file is uploaded (with a .wav or .mp3 extension), it saves the file to a temporary location and loads it using the `pydub` library.

The code performs upsampling on the audio file by doubling its sample rate. The upsampled audio is then saved as a new file with a filename prefixed by 'upsampled_'.

After saving the upsampled file, the temporary file is deleted. Finally, a JSON response is returned with a success message and the filename of the upsampled file.

The home route `/process_audio` renders the `process_audio.html` template, allowing users to upload audio files via the web application.

The `if __name__ == '__main__':` block ensures that the web application runs when the script is executed directly, with the `debug=True` argument enabling debug mode for easier development and troubleshooting.

