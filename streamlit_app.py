import streamlit as st
import random
import time
import re
#import requests
import time
from transformers import pipeline


# Adding cache with output mutation for "Continue Generated Story" Feature
@st.cache(allow_output_mutation=True)
def Content():
    return ["", 0]

content = Content()

# Render this content
st.title('Story Generator')
st.subheader('Generate Stories based on genres')
option = st.selectbox("Which genre?", ("Superhero", "sci_fi",  "Horror", "Thriller", "Action", "Drama"))

suggested_prompt = None

suggested_prompt_subtitle = "Select one of these Starting Prompts"
if option == "Horror":
    suggested_prompt = st.selectbox(suggested_prompt_subtitle, ("", "A Demon hunter", "A Ghost", "Luigi enters a haunted resort", "An apparition", "A monster", "In the mist,","A zombie", "A scary", "A spooky",))
elif option == "Superhero":
    suggested_prompt =  st.selectbox(suggested_prompt_subtitle, ("", "Batman", "Spider-Man", "Superman", "Gotham city is under attack", "Darkseid", "Thanos",
        "The Justice League", "The Avengers"))
elif option == "sci_fi":
    suggested_prompt = st.selectbox(suggested_prompt_subtitle, ("", "Aliens", "In the future, ", "A satellite", "After discovering time travel,"))
elif option == "Thriller":
    suggested_prompt = st.selectbox(suggested_prompt_subtitle, ("", "A detective must investigate the", "In the dark shadows, ", "A serial killer"))
elif option == "Action":
    suggested_prompt = st.selectbox(suggested_prompt_subtitle,  ("", "Special Agent Bart is hunting down", "After a robbery gone wrong,", "A treasure hunter", "An undercover cop poses as a gangster"))


title_input = st.text_input("Alternatively, Enter a Title")
text_input = st.text_input("Enter a Small Starting Prompt")

text_input = suggested_prompt if (suggested_prompt and (text_input == "") and (suggested_prompt != 0)) else text_input
text_input = f'"{title_input}" is a(n) {option.lower()} film about' if (title_input != "") else text_input
story_length = st.number_input("Enter length of generated text (50 - 100):", min_value=50, max_value=100, key="1")

generate_button = st.button("Generate Story")
generate_more = st.button("Continue Generated Story")
model_name = "pranavpsv/gpt2-genre-story-generator"

@st.cache(allow_output_mutation=True)
def get_model():
    story_generator = pipeline("text-generation", model_name)
    return story_generator


story_generator = get_model()
def generate_story(input_prompt, story_length):
    """
    generate_story(input_prompt, story_length) generates a story with story_length number of tokens from an input prompt
    """
    global story
    i = 1
    with st.spinner("Story Generating..."):
        contents = story_generator(f"<BOS> <{option.lower()}> {input_prompt}", max_length=story_length)[0]["generated_text"]
        print(contents)

    st.success("Story Generated!")

    # Postprocess generated story
    content = contents.split(">")[2]
    story = re.sub('\[.*?\]','', content)
    st.write("Generated Story:")
    st.write(story)

    # Write story to frontend
    return story, story_length

if generate_button:
    content[0], content[1] = generate_story(text_input, story_length)
if generate_more:
    content[1] += 50
    content[0], content[1] = generate_story(content[0], content[1])
