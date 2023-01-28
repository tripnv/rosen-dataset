#%%
import os
import pdfplumber
import pandas as pd
import json
from tqdm import tqdm
#%%
BASE_DESTINATION_PATH = 'extracted_segments_pdf'
BASE_SOURCE_PATH = 'steno_pdfs'
#%%
class PDFReader:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path
        self.pdf_text = None

    def _get_bold_lines(self, start_page: int = 1):
        """
        :param start_page: extract bold from the starting from a specific page
        :return: [list] - list of all bold lines
        """

        list_bold_text = []
        with pdfplumber.open(self.pdf_path) as pdf:
            all_pages = pdf.pages
            for index in range(start_page, len(all_pages)):
                current_page = all_pages[index]
                bold_text_filter = current_page.filter(
                    lambda obj: obj["object_type"] == "char" and "Bold" in obj["fontname"])
                text = bold_text_filter.extract_text()
                if text != "" or text != " ":
                    different_lines = text.split("\n")
                    different_lines = [line.strip(" ./-'\"[]{}`~_") for line in different_lines if line != "" and line != " "]
                    list_bold_text += different_lines

        return list_bold_text

    def read_pdf(self, start_page: int = 1):
        """
        Extract all text from pdf
        :param start_page(int) - starting the extraction from a specific page
        :return: str - Entire text from pdf
        """
        pdf_text = []
        with pdfplumber.open(self.pdf_path) as pdf:
            all_pages = pdf.pages
            for index in range(start_page, len(all_pages)):
                current_page = all_pages[index]
                text = current_page.extract_text()
                pdf_text.append(text)

        return " ".join(pdf_text)

    def extract_text_between_bolds(self, start_page: int = 1) -> pd.DataFrame:
        """
        Create a dataframe with samples which represents text between two consecutive bold lines.
        :param start_page: page number to start
        :return:
        """
        # Extract the entire pdf
        pdf_text = self.read_pdf(start_page - 1)

        # Extract the bold lines
        bold_text_list = self._get_bold_lines(start_page - 1)

        current_start = 0
        dialog_index = 1

        file_end = len(pdf_text)
        all_samples = {}

        for x, y in zip(bold_text_list[:-1], bold_text_list[1:]):

            # get first bold index, second bold index
            index_start = pdf_text.find(x, current_start, file_end)
            index_end = pdf_text.find(y, current_start, file_end)

            # crop from bold + len index
            slice_start_index = index_start + len(x)
            text = pdf_text[slice_start_index: index_end]

            # create sample info
            sample_info = {
                "start_text": x,
                "start_index": index_start,
                "end_text": y,
                "end_index": index_end,
                "text": text
            }

            # save sample info
            all_samples[f'{dialog_index}'] = sample_info

            # update start point
            current_start = index_end

            # update sample number
            dialog_index += 1

        # save as dataframe for csv
        return pd.DataFrame.from_dict(all_samples).T


def save_extracted_dataframe(dataframe: pd.DataFrame, destination_path: str) -> None:
    # dataframe.to_csv(destination_path)
    data_frame_as_dict = dataframe.to_dict(orient = 'index')
    destination_path += '.json'
    with open(destination_path, 'w',  encoding = 'utf8') as f:
        json.dump(data_frame_as_dict, f, indent = 4, ensure_ascii=False)


def process_folder_content(year: str):
    
    all_pdfs = os.listdir(f"{BASE_SOURCE_PATH}/{year}")

    for pdf_fname in tqdm(all_pdfs):
        pdfreader = PDFReader(f"{BASE_SOURCE_PATH}/{year}/{pdf_fname}")
        extracted_segments = pdfreader.extract_text_between_bolds()
        segments_name = pdf_fname.replace('.pdf', '').replace('steno', 'seg_steno')
        save_extracted_dataframe(extracted_segments, f"{BASE_DESTINATION_PATH}/{year}/{segments_name}")


#%%
for year in [2020,2021,2022]:
    process_folder_content(str(year))
# %%
