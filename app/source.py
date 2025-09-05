import streamlit as st

class SourceInput:
    def input(self):
        pass

class WebInput(SourceInput):
    def input(self):
        return st.text_input('Enter the Website URL', placeholder='https://www.yoursite.com/')

class Youtube(SourceInput):
    def input(self):
        return st.text_input('Enter the video URL', placeholder='https://www.youtube.com/watch?v=')

class PDFInput(SourceInput):
    def input(self):
        return st.file_uploader('Upload the PDF', type=['.pdf'])

class CSVInput(SourceInput):
    def input(self):
        return st.file_uploader('Upload the CSV',type=['.csv'])