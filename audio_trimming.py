# %%
from pydub import AudioSegment
from IPython.display import Audio

# %%
#%%
def trim_and_export_meeting_audio(timestamps, audio_file_path, destination_folder_path)->None:
    """ 
    Given a pair of timestamps (start and end) in seconds and an audiofile,
    trim the audio, and export the trimmed segments to a given location.
    """

    audio = AudioSegment.from_wav(audio_file_path)

    for idx, (start_time, end_time) in enumerate(timestamps):
        
        # Seconds to milliseconds
        start_time = start_time * 1000
        end_time = end_time * 1000

        trimmed_audio = audio[start_time:end_time]

        trimmed_audio.export(f"{destination_folder_path}/{audio_file_path.replace('.', f'_{idx}.')}")

        


if __name__ == '__main__':
    pass



