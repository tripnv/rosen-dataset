import streamlit as st
import json
import os

AUDIO_FOLDER_PATH = 'audio-checking/audio_folder/'
TEXT_FOLDER_PATH = 'audio-checking/text_folder/'


st.title("Audio selection")


with open("audio-checking/current_idx.txt", 'r') as f:
    current_idx = int(f.read())

audio_path = f'{AUDIO_FOLDER_PATH}{current_idx}.wav'
associated_steno_path = f'{TEXT_FOLDER_PATH}{current_idx}.json'

with open(associated_steno_path, 'r') as f:
        current_text = json.load(f)['text']

st.header("")



st.text(f'idx: {current_idx}')
st.text(associated_steno_path)
st.text_area(
        label = "", value=current_text)
st.text("")
st.text("")
st.text(audio_path)

st.audio(audio_path)
with st.form("Decision", clear_on_submit=True):
    button_bad = st.form_submit_button(label = 'Bad')
    button_good = st.form_submit_button(label = 'Good')

    if button_bad:
        result_ = 'bad'
    elif button_good:
        result_ = 'good'
    else:
        result_ = None

    with open(f'audio-checking/results.json', 'r') as f:
        current_dict = json.load(f)

    current_dict[current_idx] = result_
        
    with open('audio-checking/results.json', 'w') as f:
        current_dict = json.dump(current_dict, f, indent = 4)



    current_idx += 1
    with open("audio-checking/current_idx.txt", 'w') as f:
        f.write(str(current_idx))