import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, filtfilt
from collections import Counter

# Load the audio file
audio_file = 'My_Song_7.wav'
y, sr = librosa.load(audio_file)

# Highpass filter to remove low-frequency noise
def butter_highpass(cutoff, fs, order=5):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype='high', analog=False)
    return b, a

def highpass_filter(data, cutoff, fs, order=5):
    b, a = butter_highpass(cutoff, fs, order=order)
    y = filtfilt(b, a, data)
    return y

# Apply the highpass filter
y_filtered = highpass_filter(y, cutoff=50, fs=sr)

# Use librosa.pyin for pitch tracking
f0, voiced_flag, voiced_probs = librosa.pyin(
    y_filtered, 
    fmin=librosa.note_to_hz('C3'),  # Lower pitch bound
    fmax=librosa.note_to_hz('C6'),  # Upper pitch bound
    frame_length=1024,  # Smaller frame length for higher precision
    hop_length=256  
)

f0_filtered = f0[~np.isnan(f0)]
f0_smoothed = librosa.decompose.nn_filter(f0_filtered, aggregate=np.median, width=5)
notes = librosa.hz_to_note(f0_smoothed)
amplitude_threshold = 0.02
window_size = 1024
hop_size = 512

# Calculate the short-time RMS energy of the waveform
rms = librosa.feature.rms(y=y_filtered, frame_length=window_size, hop_length=hop_size)[0]

# Detect frames where the RMS energy is below the threshold
silent_frames = rms < amplitude_threshold

# Boundary detection based on both pitch changes and silence
note_boundaries = []
for i in range(1, len(silent_frames)):
    if silent_frames[i - 1] == False and silent_frames[i] == True:
        note_boundaries.append(i * hop_size)
    if silent_frames[i - 1] == True and silent_frames[i] == False:
        note_boundaries.append(i * hop_size)
    if i > 1 and abs(f0_filtered[i] - f0_filtered[i - 1]) > 5:  # Lower pitch change threshold for finer accuracy
        note_boundaries.append(i * hop_size)

# Add a final boundary if the last note segment is not captured
if len(note_boundaries) % 2 != 0:
    note_boundaries.append(len(y))

# Map note names to integers for easier processing
note_mapping = {note: idx for idx, note in enumerate(np.unique(notes))}
reverse_note_mapping = {idx: note for note, idx in note_mapping.items()}

# Detect notes based on boundaries and pitch tracking
detected_notes = []
for i in range(0, len(note_boundaries) - 1, 2):
    start_idx = note_boundaries[i]
    end_idx = note_boundaries[i + 1] if i + 1 < len(note_boundaries) else len(notes)
    note_section = notes[start_idx // hop_size:end_idx // hop_size]

    if len(note_section) > 0:
        note_section_int = [note_mapping[note] for note in note_section]
        most_frequent_note_int = Counter(note_section_int).most_common(1)[0][0]
        most_frequent_note = reverse_note_mapping[most_frequent_note_int]
        detected_notes.append(most_frequent_note)

    print(f"Segment {i // 2 + 1}: Start {start_idx}, End {end_idx}, Notes: {note_section}")

# Plot the waveform with detected note boundaries
plt.figure(figsize=(10, 4))
librosa.display.waveshow(y, sr=sr)
for boundary in note_boundaries:
    plt.axvline(x=boundary / sr, color='r', linestyle='--')
plt.title('Waveform with Detected Note Boundaries')
plt.show()

# Print debug information about note boundaries
for i, note in enumerate(detected_notes):
    print(f"Detected note {i + 1}: {note} at boundary {note_boundaries[i]}")

# Print the simplified detected notes
print("Detected notes:", detected_notes)
