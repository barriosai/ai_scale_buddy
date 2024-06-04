import streamlit as st
import openai
import random

# Function to retrieve the API key
def get_api_key():
    return st.secrets["api_key"]

# Initialize OpenAI client
api_key = get_api_key()
openai.api_key = api_key

# Function to get a GPT hint
def get_hint(note):
    completion = openai.chat.completions.create(
      model="gpt-4o",
      messages=[
       {"role": "system", "content": "You are a music teacher, skilled in explaining music theory and programming with a creative flair."},
       {"role": "user", "content": f"Can you give me a hint for identifying the notes in the {note} major triad? Don't give it away just help with a good educational hint. Just give the hint, don't reply with Certainly, just the hint."}
])

    return completion.choices[0].message.content.strip()



# Define all major scales
major_scales = {
    'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
    'C#': ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'],
    'Db': ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'],
    'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
    'D#': ['D#', 'E#', 'Fx', 'G#', 'A#', 'B#', 'Cx'],
    'Eb': ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
    'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
    'F': ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
    'F#': ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'],
    'Gb': ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F'],
    'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
    'G#': ['G#', 'A#', 'B#', 'C#', 'D#', 'E#', 'Fx'],
    'Ab': ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
    'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
    'A#': ['A#', 'B#', 'Cx', 'D#', 'E#', 'Fx', 'Gx'],
    'Bb': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
    'B': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#']
}

def quiz_major_scales_with_hints():
    st.title("Scale Buddy with AI Hints 🤖")
    st.write("You will be asked to enter the notes in various major scales.")
    st.write("Please enter the notes separated by commas and spaces (e.g., C, D, E, F, G, A, B).")

    if 'correct_answers' not in st.session_state:
        st.session_state.correct_answers = 0
    if 'total_questions' not in st.session_state:
        st.session_state.total_questions = 0
    if 'current_key' not in st.session_state:
        st.session_state.current_key = random.choice(list(major_scales.keys()))
    if 'continue_quiz' not in st.session_state:
        st.session_state.continue_quiz = True

    if st.session_state.continue_quiz:
        current_key = st.session_state.current_key
        hint = get_hint(current_key)
        st.write(f"Hint: {hint}")
        
        answer = st.text_input(f"What are the notes in the {current_key} major scale?", key="answer")
        
        if st.button("Submit Answer"):
            answer_list = [note.strip() for note in answer.split(',')]
            correct_notes = major_scales[current_key]
            if answer_list == correct_notes:
                st.write("Correct!")
                st.session_state.correct_answers += 1
            else:
                correct_order = ', '.join(major_scales[current_key])
                st.error(f"Incorrect. The correct notes are {correct_order}")

            st.session_state.total_questions += 1
            st.session_state.current_key = random.choice(list(major_scales.keys()))
            st.experimental_rerun()

        if st.button("End Quiz"):
            st.session_state.continue_quiz = False
            st.write(f"\nYou got {st.session_state.correct_answers} out of {st.session_state.total_questions} correct.")
            st.session_state.correct_answers = 0
            st.session_state.total_questions = 0

# Start the quiz
quiz_major_scales_with_hints()
