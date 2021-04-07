import streamlit as st
from multiapp import MultiApp
import main
import test # import your app modules here


app = MultiApp()
        # Add all your application here
app.add_app("Model", main.main)
app.add_app("Model", main.mainapp)


        # The main app
app.run()
