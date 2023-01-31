import os
import shutil
from pydub import AudioSegment
from utils import pop_log
import json
import pandas as pd


class SnippetExtractor:

    def __init__(self, pdf_steno, audio_file_path):

        self.steno_path = pdf_steno
        self.audio_file_path = audio_file_path
        self.audio_file = None
        self.df_steno = None

    @staticmethod
    def create_output_folder():
        """
        Create output folder for speach-to-text dataset.
        The file should be created in the same folder as the project. (filename: "dataset")
        """
        current_folder_path = os.path.dirname(os.path.realpath(__file__))
        folder_wav_output = os.path.join(current_folder_path, "dataset")

        input_folder = os.path.join(folder_wav_output, "input")
        target_folder = os.path.join(folder_wav_output, "target")

        if not os.path.exists(folder_wav_output):
            os.makedirs(folder_wav_output)
        else:
            shutil.rmtree(folder_wav_output)
            os.makedirs(folder_wav_output)

        if not os.path.exists(input_folder):
            os.makedirs(input_folder)
        else:
            shutil.rmtree(input_folder)
            os.makedirs(input_folder)

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        else:
            shutil.rmtree(target_folder)
            os.makedirs(target_folder)

    def extract_timestamps_from_audio(self):
        """

        :return:
        """

        steno_sample = self.df_steno['text']
        start_timestamp = self.df_steno['start']
        end_timestamp = self.df_steno['end']

        current_folder_path = os.path.dirname(os.path.realpath(__file__))
        folder_wav_output = os.path.join(current_folder_path, "dataset")

        input_folder = os.path.join(folder_wav_output, "input")
        output_folder = os.path.join(folder_wav_output, "target")

        length = len(steno_sample)

        for index in range(length):
            print(f"Timestamp {index} / {length + 1}")

            current_steno = steno_sample[index]
            current_start_timestamp, current_end_timestamp = start_timestamp[index], end_timestamp[index]

            if abs(current_start_timestamp - current_end_timestamp) > 500:
                pop_log("Current timestamp was skipped...", "WARNING")
                continue

            current_start_timestamp = current_start_timestamp * 1000  # in ms
            current_end_timestamp = current_end_timestamp * 1000  # in ms

            audio = self.audio_file[current_start_timestamp: current_end_timestamp]

            audio.export(os.path.join(input_folder, f"audio_{index}.mp3"), format='wav')

            with open(os.path.join(output_folder, f"text_{index}.json"), 'w') as f:
                json.dump({'text': current_steno}, f)

    def create_samples(self):

        self.df_steno = pd.read_csv(self.steno_path)

        # create output folder
        self.create_output_folder()

        # read audio file
        self.audio_file = AudioSegment.from_wav(self.audio_file_path)

        # extract timestamps from audio
        self.extract_timestamps_from_audio()


if __name__ == '__main__':

    steno = "/Users/andreibobes/Documents/Projects/NLP2/new_steno_21_decembrie_2022_timestamps.csv"
    audio_file = "/Users/andreibobes/Documents/Projects/NLP2/old/wav_outputs/Ședința Senatului României din data de " \
                 "21 Decembrie 202200001.wav"

    snip_ext = SnippetExtractor(steno, audio_file)
    snip_ext.create_samples()
