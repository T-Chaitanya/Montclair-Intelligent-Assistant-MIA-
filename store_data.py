from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import os

# Set your OpenAI API key if using OpenAI embeddings
os.environ["OPENAI_API_KEY"] = "your-api-key"

# Example documents
with open('scraped_data.txt', 'r', encoding='utf-8') as file:
    text = file.read()

# Split text into manageable chunks
from langchain.text_splitter import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = splitter.split_text(text)

# Generate embeddings
embeddings = OpenAIEmbeddings()

# Create a FAISS vectorstore
vectorstore = FAISS.from_texts(texts, embeddings)

# Save the FAISS vectorstore to disk
vectorstore.save_local("faiss_index")


