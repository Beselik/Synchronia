import librosa 
import librosa.display
import matplotlib.pyplot as plt
audio_file = 'in_the_end.wav'
y, sr = librosa.load(audio_file)
pitches, magnitudes, = librosa.core.piptrack(y=y, sr=sr)
plt.figure(figsize=(10, 4))
librosa.display.waveshow(y, sr=sr)
plt.title('Waveform')
plt.show()
print(pitches)
