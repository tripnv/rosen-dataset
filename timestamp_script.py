# %%
import os
import pandas as pd
import json
import re
import numpy as np
import multiprocessing
# %%
from unidecode import unidecode
from num2words import num2words 
from thefuzz import fuzz

SOURCE_TRANSCRIPTS = 'transcriptions_2/'
SOURCE_STENOS = 'extracted_segments_pdf/2022/'
DESTINATION_FOLDER = 'extracted_csvs/'


def text_cleaning(text):
    
    # Remove PAUZĂ
    text = re.sub("PAUZĂ", '', text)
    
    text = text.lower()
    text = text.replace("art.", "art ")
    
    # Remove diacritics
    text = unidecode(text)

    # Replace spaces
    text = re.sub("\s\s+", ' ', text)

    # Remove parenthesis
    text = re.sub("\(.+?\)", ' ', text)

    # Remove page number
    text = re.sub("-\s[0-9]+\s-", '', text)

    # Remove special characters
    text = re.sub("[^\w\s]", ' ', text)
    
    # Replace spaces
    text = re.sub("\s\s+", ' ', text)
    
    # Convert digits to text
    text = text.split(" ")
    text = [num2words(word, lang = 'ro') if word.isnumeric() else word for word in text]
    
    text = " ".join(text)
    
    # Second decoding step
    text = unidecode(text)

    return text

def fuzzy_search2(phrase, corpus):
    #phrase = text_cleaning(phrase)
    value = fuzz.token_set_ratio(corpus, phrase)
    if value >= 80:
        return True
    
    return False

def get_timestamp_for_steno(steno, df_transcript):
    
    # Todo: daca cubul are ca maxim valori negative atunci ignori
    
    #print("sample")
    
    # get is in corpus
    df_transcript['in_corpus'] = df_transcript['text'].map(lambda x: fuzzy_search2(x, steno))
    
    # count consecutive True values
    g = df_transcript['in_corpus'].ne(df_transcript['in_corpus'].shift()).cumsum()
    df_transcript['Count'] = df_transcript.groupby(g)['in_corpus'].transform('size') * np.where(df_transcript['in_corpus'], 1, -1)
    
    # get max of consecutive True values
    max_consecutive = df_transcript['Count'].max()
    
    # filter the cube
    # Todo: take first max_consecutive
    df_cube = df_transcript[df_transcript['Count'] == max_consecutive]
    
    # return start timestamp, end timestamp
    return (df_cube['start'].min(), df_cube['start'].max())

def get_timestamp_for_steno_2(steno, df_transcript):
    
    # get is in corpus
    transcript_text = df_transcript['text'].to_numpy()
    in_corpus = [fuzzy_search2(transcript, steno) for transcript in transcript_text]
    #df_transcript['in_corpus'] = df_transcript['text'].map(lambda x: fuzzy_search2(x, steno))
    df_transcript['in_corpus'] = in_corpus
    
    # count consecutive True values
    g = df_transcript['in_corpus'].ne(df_transcript['in_corpus'].shift()).cumsum()
    df_transcript['Count'] = df_transcript.groupby(g)['in_corpus'].transform('size') * np.where(df_transcript['in_corpus'], 1, -1)
    
    # get max of consecutive True values
    max_consecutive = df_transcript['Count'].max()
    
    # filter the cube
    df_cube = df_transcript[df_transcript['Count'] == max_consecutive]
    
    # asta e pentru fisier
    return (df_cube['start'].min(), df_cube['start'].max())
    
    # asta e pentru vizualizare cub
    # return (df_cube['start'].min(), df_cube['end'].max(), df_cube)

def assign_timestamps_to_steno(steno_fpath, transcript_fpath):
    
    # Get fname
    fname = transcript_fpath.split('/')[-1].replace('.json', '')
    
    # Collect the resources
    try:
        df_steno = get_stenogram_extracted_json(steno_fpath)
        df_transcript = get_transcript_json(transcript_fpath)

        # Clean the stenos and transcripts
        df_steno['text'] = df_steno['text'].map(text_cleaning)
        df_transcript['text'] = df_transcript['text'].map(text_cleaning)

        text = df_steno['text'].to_numpy()

        # Generate timestamps
        timestamp = [get_timestamp_for_steno_2(steno, df_transcript) for steno in text]

        # Assign generated timestamps to the steno dataframe
        df_steno['timestamp'] = timestamp

        df_steno[['start', 'end']] = pd.DataFrame(df_steno['timestamp'].tolist(), index=df_steno.index)

        save_dataframe(df_steno, fname)
    except:
        print(f"{fname}")


def save_dataframe(df: pd.DataFrame, fname: str):
    """ Export dataframe to the target folder """
    export_path = DESTINATION_FOLDER + fname + '.csv'
    df.to_csv(export_path)



# %%
def get_stenogram_extracted_json(fpath: str):
    # Get steno
    df_steno = pd.read_json(fpath)
    df_steno = df_steno.T

    return df_steno

# %%

def get_transcript_json(fpath: str):
    # get transcript
    with open(fpath, 'r') as file:
        data = json.load(file)
    
    df_transcript = pd.DataFrame.from_dict(data['segments'])

    return df_transcript

def get_fpaths(fname:str):
    """ Given a transcript fname, return the associated stenogram and transcript full paths """
    steno_full_path = SOURCE_STENOS + fname
    transcript_full_path = SOURCE_TRANSCRIPTS + fname
    return steno_full_path, transcript_full_path

def task(transcript_fname):
    steno_fpath, transcript_fpath = get_fpaths(transcript_fname)
    assign_timestamps_to_steno(steno_fpath, transcript_fpath)


if __name__ == '__main__':
    print(f""" The following files have been ommited: """)
    all_transcripts = os.listdir(SOURCE_TRANSCRIPTS)
    with multiprocessing.Pool() as pool:
        pool.map(task, all_transcripts)


        
