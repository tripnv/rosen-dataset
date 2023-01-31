import streamlit as st
import json

st.title("Audio selection")


with open("current_idx.txt", 'r') as f:
    current_idx = int(f.read())

audio_path = f'results/audio/{current_idx}'
associated_steno_path = f'results/stenos/{current_idx}'

min_file_index = st.number_input(label = 'Min file index', step = 1, min_value= 0)
max_file_index = st.number_input(label = 'Max file index', step = 1, min_value= 0)

st.header("")



st.header(f'idx: {current_idx}')
st.text(associated_steno_path)
st.text_area(
        label = "", value=f"Lorem ipsum {current_idx}"
    )
st.text("")
st.text("")
st.text(audio_path)

st.audio('audio_seg_1.wav')
with st.form("Decision", clear_on_submit=True):
    button_bad = st.form_submit_button(label = 'Bad')
    button_good = st.form_submit_button(label = 'Good')

    if button_bad:
        result_ = 'bad'
    elif button_good:
        result_ = 'good'
    else:
        result_ = None

    with open('results.json', 'r') as f:
        current_dict = json.load(f)

    current_dict[str(current_idx)] = result_
        
    with open('results.json', 'w') as f:
        current_dict = json.dump(current_dict, f, indent = 4)



    current_idx += 1
    with open("current_idx.txt", 'w') as f:
        f.write(str(current_idx))