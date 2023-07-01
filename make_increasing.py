import os
from scipy.io.wavfile import read as read_wav
from scipy.io.wavfile import write as write_wav
import numpy as np
from function_shape import start_time_seconds, time_till_full_power


def alter_audio_array(rate, audio_array):
    # make ringtone 10 minuets long (via looping it several times)
    total_time = len(audio_array) / rate
    num_loops = int(np.ceil(10 * 60 / total_time))
    audio_array = np.concatenate([audio_array for i in range(num_loops)])

    # buffer with empty start
    audio_array = np.concatenate([np.zeros((int(start_time_seconds * rate), 2)), audio_array])

    # make audio linearly increasing, from 0.1 at the beginning until it reaches twice the original volume after 3 minutes, then stay at that level
    time_of_stop_increasing = time_till_full_power + start_time_seconds
    time_array = np.arange(0, len(audio_array)) * 1 / rate
    index_of_stop_increasing = int(len(time_array) * (time_of_stop_increasing / (time_array[-1])))
    index_of_start_increasing = int(len(time_array) * (start_time_seconds / (time_array[-1])))
    increasing_part_of_mask = np.linspace(0, 1, index_of_stop_increasing - index_of_start_increasing)
    mask = np.ones(audio_array.shape, float)
    mask[index_of_start_increasing:index_of_stop_increasing, 0] = increasing_part_of_mask
    mask[index_of_start_increasing:index_of_stop_increasing, 1] = increasing_part_of_mask
    audio_array *= mask
    audio_array = audio_array.astype(np.int16)

    return audio_array


try:
    import efipy
    input_file = os.path.split(efipy.inquire_input_path())[1]
except:
    print("select input file")
    input_file = input()

wav_file_name = "ringtone.wav"
output_file_name = "ringtone.mp3"
os.system(f"ffmpeg -y -i \"{input_file}\"  {wav_file_name}")
rate, audio_array = read_wav(wav_file_name)
audio_array = alter_audio_array(rate, audio_array)
write_wav(wav_file_name, rate, audio_array)
os.system(f"ffmpeg -y -i \"{wav_file_name}\"  {output_file_name}")
