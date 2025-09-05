import streamlit as st
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_anthropic import ChatAnthropic
#from langchain_core.cache import BaseCache
import os


class Model:

    @staticmethod
    def load_model(provider, model, document, document_type):
        template = Model.build_template(document, document_type)
        provider['Chat'].model_rebuild()
        chat = provider['Chat'](model=model, api_key=provider['Key'])
        chain = template | chat
        st.session_state["Chain"] = chain

    @staticmethod
    def build_template(document, document_type):
        system_message = '''You are a friendly assistant named Genius.
                                                          You have access to the following information coming from a document {}:

                                                         ####
                                                         {}
                                                         ####

                                                         Use the information provided to base your answers.

                                                         Whenever there is a $ in your output, replace it with S.

                                                         If the document’s information is something like
                                                         “Just a moment… Enable JavaScript and cookies to continue”,
                                                         suggest to the user that they reload Oracle!'''.format(
            document_type, document)

        template = ChatPromptTemplate.from_messages([
            ('system', system_message.replace('{', '{{').replace('}', '}}')),
            ('placeholder', '{chat_history}'),
            ('user', '{input}')
        ])
        return template

    @staticmethod
    def get_providers():
        providers = {
            'OpenAI': {'Models': ['gpt-4.1-mini'],
                       'Key': os.getenv('OPEN_AI_API_KEY'),
                       'Chat': ChatOpenAI},
            'Groq': {'Models': ['groq/compound'],
                     'Key': os.getenv('GROQ_API_KEY'),
                     'Chat': ChatGroq},
            'Anthropic': {'Models': ['claude-3-haiku-20240307', 'claude-sonnet-4-20250514'],
                          'Key': os.getenv('ANTHROPIC_API_KEY'),
                          'Chat': ChatAnthropic},
        }

        return providers
