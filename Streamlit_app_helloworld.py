#import streamlit

import streamlit as st

# create a title Hellow World App
st.title("Hello World App")

# create a text input for the user to enter their name
name = st.text_input("Enter your name")

# create a button to say hello

if st.button("Say hello"):
    st.write(f"Hello {name}!")


