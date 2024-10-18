import librosa 
import librosa.display
import matplotlib.pyplot as plt
from scipy.ndimage import median_filter
import numpy as np
from scipy.signal import butter, filtfilt
audio_file = 'My_song_2.wav'
y, sr = librosa.load(audio_file)
def butter_highpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

y_filtered = highpass_filter(y, cutoff=50, fs=sr)
f0, voiced_flag, voiced_probs = librosa.pyin(y_filtered, 
                                             fmin=librosa.note_to_hz('C3'),  # Lower pitch bound
                                             fmax=librosa.note_to_hz('C6'),  # Upper pitch bound
                                             frame_length=2048,  # Frame size for pitch tracking
                                             hop_length=256)
pitches, magnitudes, = librosa.core.piptrack(y=y, sr=sr)
f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'))
f0_filtered = f0[~np.isnan(f0)]
f0_smoothed = median_filter(f0_filtered, size=3)
notes = librosa.hz_to_note(f0_smoothed)
notes = librosa.hz_to_note(f0_filtered)
min_duration = 5  # Minimum consecutive frames for a note to be considered valid
simplified_notes = []
current_note = notes[0]
count = 0
for i, note in enumerate(notes):
    if note == current_note:
        count += 1
    else:
        if count >= min_duration:
            simplified_notes.append(current_note)
        current_note = note
        count = 1  # Reset count


if count >= min_duration:
    simplified_notes.append(current_note)
        
plt.figure(figsize=(10, 4))
librosa.display.waveshow(y, sr=sr)
plt.title('Waveform')
plt.show()
print(simplified_notes)
print(pitches)
