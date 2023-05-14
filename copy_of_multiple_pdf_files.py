# -*- coding: utf-8 -*-
"""Copy of Multiple_PDF_files.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mIO99-4QWgIKvjgAFj0vvEbQi5xgNCPk

### Installation
"""

#!pip install langchain
#!pip install unstructured
#!pip install openai
#!pip install chromadb
#!pip install Cython
#!pip install tiktoken

"""### Load Required Packages"""

from langchain.document_loaders import UnstructuredPDFLoader
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import GoogleDriveLoader
#OpenAI API Key"""

# Get your API keys from openai, you will need to create an account. 
# Here is the link to get the keys: https://platform.openai.com/account/billing/overview
import os
#os.environ["OPENAI_API_KEY"] = "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"
#Connect Google Drive"""
loader = GoogleDriveLoader(
    folder_id="12vwDZ9GxZOgILsjdF2hIH4gjZ51x1sek",credentials_path="credentials.json",
    # Optional: configure whether to recursively fetch files from subfolders. Defaults to False.
    recursive=False
)
docs=loader.load()
# connect your Google Drive
#from google.colab import drive
#drive.mount('/content/gdrive', force_remount=True)
#root_dir = "/content/gdrive/My Drive/"

#pdf_folder_path = f'{root_dir}/data/'
#os.listdir(pdf_folder_path)


# Load Multiple PDF files"""

# location of the pdf file/files. 
#loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]

#loaders

"""### Vector Store 
Chroma as vectorstore to index and search embeddings


There are three main steps going on after the documents are loaded:

- Splitting documents into chunks

- Creating embeddings for each document

- Storing documents and embeddings in a vectorstore

"""

#!pip install unstructured[local-inference]
index = VectorstoreIndexCreator().from_loaders(docs)
#index = VectorstoreIndexCreator().from_loaders(loaders)
import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from streamlit_extras.add_vertical_space import add_vertical_space
from hugchat import hugchat

st.set_page_config(page_title="HugChat - An LLM-powered Streamlit app")

# Sidebar contents
with st.sidebar:
    st.title('🤗💬 HugChat App')
    st.markdown('''
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [HugChat](https://github.com/Soulter/hugging-chat-api)
    - [OpenAssistant/oasst-sft-6-llama-30b-xor](https://huggingface.co/OpenAssistant/oasst-sft-6-llama-30b-xor) LLM model
    
    💡 Note: No API key required!
    ''')
    add_vertical_space(5)
    st.write('Made with ❤️ by [Data Professor](https://youtube.com/dataprofessor)')

# Generate empty lists for generated and past.
## generated stores AI generated responses
if 'generated' not in st.session_state:
    st.session_state['generated'] = ["I'm HugChat, How may I help you?"]
## past stores User's questions
if 'past' not in st.session_state:
    st.session_state['past'] = ['Hi!']

# Layout of input/response containers
input_container = st.container()
colored_header(label='', description='', color_name='blue-30')
response_container = st.container()

# User input
## Function for taking user provided prompt as input
def get_text():
    input_text = st.text_input("You: ", "", key="input")
    return input_text
## Applying the user input box
with input_container:
    user_input = get_text()

# Response output
## Function for taking user prompt as input followed by producing AI generated responses
def generate_response(prompt):
    chatbot = hugchat.ChatBot()
    response = chatbot.chat(prompt)
    return response

## Conditional display of AI generated responses as a function of user provided prompts
with response_container:
    if user_input:
        response = generate_response(user_input)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(response)
        
    if st.session_state['generated']:
        for i in range(len(st.session_state['generated'])):
            message(st.session_state['past'][i], is_user=True, key=str(i) + '_user')
            message(st.session_state["generated"][i], key=str(i))


#index.query('What was the main topic of the address?')

#index.query('List Holidays of India?')

#index.query_with_sources('What are the different types of tourism? ')

#index.query_with_sources('How many total holidays india have?')



#pdf_folder_path = '/content/gdrive/My Drive/data_2/'
#os.listdir(pdf_folder_path)

# location of the pdf file/files. 
#loaders = [UnstructuredPDFLoader(os.path.join(pdf_folder_path, fn)) for fn in os.listdir(pdf_folder_path)]
#index = VectorstoreIndexCreator().from_loaders(loaders)
#index
