import streamlit as st
import re
import requests
import time
from multiprocessing.dummy import Pool

pool = Pool(4)

# Adding cache with output mutation for "Continue Generated Story" Feature
@st.cache(allow_output_mutation=True)
def Content():
    return ["", 0]

content = Content()

# Render this content
st.title('Story Generator')
st.subheader('Generate Stories based on genres')
option = st.selectbox("Which genre?", ("Action", "Superhero", "Drama", "sci_fi", "Thriller", "Horror"))
text_input = st.text_input("Enter a Small Starting Prompt")
title_input = st.text_input("Alternatively, Enter a Title")

suggested_prompt = None

suggested_prompt_subtitle = "Alternatively, Select one of these Starting Prompts"
if option == "Horror":
    suggested_prompt = st.selectbox(suggested_prompt_subtitle, ("", "A Demon hunter", "A Ghost", "An apparition", "A monster", "In the mist,","A zombie", "A scary", "A spooky"))
elif option == "Superhero":
    suggested_prompt =  st.selectbox(suggested_prompt_subtitle, ("", "Batman", "Spider-Man", "Superman", "Gotham city is under attack", "Darkseid", "Thanos",
        "The Justice League", "The Avengers"))
elif option == "sci_fi":
    suggested_prompt = st.selectbox(suggested_prompt_subtitle, ("", "Aliens", "In the future, ", "A satellite", "After discovering time travel,"))
elif option == "Thriller":
    suggested_prompt = st.selectbox(suggested_prompt_subtitle, ("", "A detective must investigate the", "In the dark shadows, ", "A serial killer"))
elif option == "Action":
    suggested_prompt = st.selectbox(suggested_prompt_subtitle,  ("", "Special Agent Bart is hunting down", "After a robbery gone wrong,", "A treasure hunter", "An undercover cop poses as a gangster"))

text_input = suggested_prompt if (suggested_prompt and (text_input == "") and (suggested_prompt != 0)) else text_input
text_input = f'"{title_input}" is a film about' if (title_input != "") else text_input
story_length = st.number_input("Enter length of generated text (50 - 100):", min_value=50, max_value=100, key="1")

generate_button = st.button("Generate Story")
generate_more = st.button("Continue Generated Story")


def generate_story(input_prompt, story_length):
    """
    generate_story(input_prompt, story_length) generates a story with story_length number of tokens from an input prompt
    """

    with st.spinner("Story Generating..."):
        my_bar = st.progress(0)
        r = pool.apply_async(requests.post, ["http://127.0.0.1:8000/generate"], {"json": {"prompt": f"<BOS> <{option.lower()}> {input_prompt}", "length": story_length}})

        # Display progress bar while generating
        for percent_complete in range(100):
            time.sleep(0.05)
            my_bar.progress(percent_complete + 1)

    st.success("Story Generated!")
    contents = [text["generated_text"] for text in eval(r.get().content)]

    # Postprocess generated story
    content = contents[0].split(">")[2]
    content = re.sub('\[.*?\]','', content)

    # Write story to frontend
    st.write(content)
    return content, story_length

if generate_button:
    content[0], content[1] = generate_story(text_input, story_length)
if generate_more:
    content[1] += 50
    content[0], content[1] = generate_story(content[0], content[1])
