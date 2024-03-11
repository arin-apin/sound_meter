import sounddevice as sd
import numpy as np
import csv
import os
from datetime import datetime

from mediapipe.tasks import python
from mediapipe.tasks.python.components import containers
from mediapipe.tasks.python import audio

# Customize and associate model for Classifier
# Yo can download model with this command:
# wget -O audio_classifier.tflite -q https://storage.googleapis.com/mediapipe-models/audio_classifier/yamnet/float32/1/yamnet.tflite
base_options = python.BaseOptions(model_asset_path='audio_classifier.tflite')
options = audio.AudioClassifierOptions(base_options=base_options, max_results=5)
classifier = audio.AudioClassifier.create_from_options(options)


def record_audio(duration=10, sampling_rate=44100):
    """Record audio from the microphone for a specific duration."""
    print(f"Recording audio for {duration} seconds...")
    audio = sd.rec(int(duration * sampling_rate), samplerate=sampling_rate, channels=2)
    sd.wait()  # Wait until recording is finished
    return audio


def calculate_sound_level(audio, sampling_rate=44100):
    """Calculate the RMS sound level of the audio samples."""
    audio_mono = np.mean(audio, axis=1)  # Convert to mono if necessary
    rms = np.sqrt(np.mean(audio_mono**2))
    return 20 * np.log10(rms)


def save_sound_level_to_csv(sound_level, date_time, sounds):
    filename = f"{date_time.year}-{date_time.month:02d}-{date_time.day:02d}.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Hour', 'Minute', 'Data', 'Sounds'])
        writer.writerow([date_time.hour,
                         date_time.minute,
                         sound_level,
                         sounds
                         ])


def audio_inference(audio, sampling_rate=44100):
    audio_clip = containers.AudioData.create_from_array(
        audio, sampling_rate)
    classification_result_list = classifier.classify(audio_clip)
    sound_list = []
    for classification_result in classification_result_list:
        detected_sound = classification_result.classifications[0].categories[0].category_name
        print(detected_sound)
        sound_list.append(detected_sound)
    return sound_list


def perform_cyclic_measurement(duration=5, sampling_rate=44100):
    """Perform sound measurements cyclically and update the graph."""
    sound_levels = []
    previous_date_time = datetime.now()
    sound_types = []
    while True:
        audio = record_audio(duration, sampling_rate)
        samples = [calculate_sound_level(audio[i:i+sampling_rate]) for i in range(0, len(audio), sampling_rate)]
        for sample in samples:
            sound_levels.append(sample)
        sounds = audio_inference(audio=audio, sampling_rate=sampling_rate)
        for sound in sounds:
            sound_types.append(sound)
        current_date_time = datetime.now()
        if current_date_time.minute != previous_date_time.minute:
            save_sound_level_to_csv(sound_levels, current_date_time, sound_types)
            print('Saved', current_date_time)
            previous_date_time = datetime.now()
            sound_levels = []
            sound_types = []


# Configure these values according to your needs
duration = 4.874  # Recording duration in seconds. 
# Audio classifier chunks sound in .975 seconds chunks, this way we ensure every chunk is big enough
sampling_rate = 44100  # Sampling frequency

perform_cyclic_measurement(duration, sampling_rate)
