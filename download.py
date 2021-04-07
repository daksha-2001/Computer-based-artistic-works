import streamlit as st
from PIL import Image
import style
import base64
from io import BytesIO


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)



local_css("style.css")

button_clicked = st.button("OK")
user=st.text_input("Hello")

