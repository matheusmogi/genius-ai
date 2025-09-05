import yaml
import streamlit as st
from streamlit_supabase_auth import logout_button
from authenticator import sign_in
from source_strategy import get_source
from model import Model
from langchain.memory import ConversationBufferMemory

# load env keys
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Genius", page_icon="🧞")
MEMORY = ConversationBufferMemory()

def chat():
    st.html('<h1><center>Welcome to Genius 🧞</center></h1>')
    chain = st.session_state.get("Chain")
    if chain is None:
        st.error('load the Model')
        st.stop()

    stored_messages = st.session_state.get("messages", MEMORY)
    for message in stored_messages.buffer_as_messages:
        conversation = st.chat_message(message.type)
        conversation.markdown(message.content)

    user_input = st.chat_input('What is your question?')
    if user_input:
        conversation = st.chat_message('human')
        conversation.markdown(user_input)

        conversation = st.chat_message('ai')
        response = conversation.write_stream(chain.stream(
            {'input':user_input,
             'chat_history': stored_messages.buffer_as_messages
             }))

        stored_messages.chat_memory.add_user_message(user_input)
        stored_messages.chat_memory.add_ai_message(response)
        st.session_state["messages"] = stored_messages

def sidebar():
    tabs = st.tabs(['File Upload', 'Model Selection'])
    with tabs[0]:
        sources = get_source()
        source_type = st.selectbox('Select the source', sources.keys())
        source = sources[source_type]["Source"].input()

    with tabs[1]:
        providers = Model.get_providers()
        provider = st.selectbox('Select the model provider', providers.keys())
        model = st.selectbox('Select the model', providers[provider]['Models'])

    if source:
        if st.button('Load Model'):
            document = sources[source_type]["Loader"].load(source)
            Model.load_model(providers[provider], model, document, source_type)

    if st.button('Clean History'):
        st.session_state["messages"]=MEMORY

    logout_button()


def main():
    if sign_in():
        with st.sidebar:
           sidebar()
        chat()



if __name__ == '__main__':
    main()
