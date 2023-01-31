import os
import shutil
from pydub import AudioSegment
from utils import pop_log
import json
import pandas as pd


class SnippetExtractor:

    def __init__(self, pdf_steno, audio_file_path):

        self.steno_path = pdf_steno
        self.df_steno = None

        self.audio_file_path = audio_file_path
        self.audio_file = None

        self.input_folder_path = None
        self.target_folder_path = None
        self.sample_folder_path = None

    def create_output_folder(self):
        """
        Create output folder for speach-to-text dataset.
        The file should be created in the same folder as the project. (filename: "dataset")
        """
        project_folder_path = os.path.dirname(os.path.realpath(__file__))

        dataset_folder_path = os.path.join(project_folder_path, "dataset")
        if not os.path.exists(dataset_folder_path):
            os.makedirs(dataset_folder_path)

        audio_sample_name = os.path.splitext(os.path.basename(self.audio_file_path))[0]
        self.sample_folder_path = os.path.join(dataset_folder_path, audio_sample_name)

        self.input_folder_path = os.path.join(self.sample_folder_path, "input")
        self.target_folder_path = os.path.join(self.sample_folder_path, "target")

        folders_to_create = [self.sample_folder_path, self.input_folder_path, self.target_folder_path]

        for folder_path in folders_to_create:
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            else:
                shutil.rmtree(folder_path)
                os.makedirs(folder_path)

    def extract_timestamps_from_audio(self):
        """

        :return:
        """

        steno_sample = self.df_steno['original_text']
        start_timestamp = self.df_steno['start']
        end_timestamp = self.df_steno['end']

        length = len(steno_sample)

        audio_sample_name = os.path.splitext(os.path.basename(self.audio_file_path))[0]

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

            audio.export(os.path.join(self.input_folder_path, f"{audio_sample_name}_{index}.mp3"), format='mp3')

            with open(os.path.join(self.target_folder_path, f"{audio_sample_name}_{index}.json"), 'w', encoding='utf-8') as f:
                json.dump({'text': current_steno}, f, ensure_ascii=False)

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

    # sa iau denumirea fisierului audio (12.24.2022.wav) ->
