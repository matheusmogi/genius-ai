import streamlit as st
import os
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_community.document_loaders import (WebBaseLoader,
                                                  CSVLoader,
                                                  PyPDFLoader)
import tempfile
from fake_useragent import UserAgent

from abc import ABC, abstractmethod


class AbstractLoader(ABC):
    @abstractmethod
    def load(self, source):
        pass


class WebLoader(AbstractLoader):
    def load(self, source):
        document = ''
        for i in range(5):
            try:
                os.environ["USER_AGENT"] = UserAgent().random
                loader = WebBaseLoader(source)
                document_list = loader.load()
                document = '\n\n'.join([doc.page_content for doc in document_list])
                break
            except:
                print('error on loading web page')
        if document == '':
            st.error('error on loading web page')
            st.stop()
        return document


class YouTubeLoader(AbstractLoader):
    def load(self, source):
        # extract id from url
        video_id = source.split('=')[-1]
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)
        document = ''
        for snippet in fetched_transcript:
            document += snippet.text + ' '
        return document


class CsvLoader(AbstractLoader):
    def load(self, source):
        with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as temp:
            temp.write(source.read())
            temp_path = temp.name
            temp.flush()
        loader = CSVLoader(temp_path)
        document_list = loader.load()
        document = '\n\n'.join([doc.page_content for doc in document_list])
        return document


class PDFLoader(AbstractLoader):
    def load(self, source):
        with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp:
            temp.write(source.read())
            temp_path = temp.name
            temp.flush()
        loader = PyPDFLoader(temp_path)
        document_list = loader.load()
        document = '\n\n'.join([doc.page_content for doc in document_list])
        return document
