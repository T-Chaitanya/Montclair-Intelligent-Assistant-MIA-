from langchain.vectorstores import FAISS
import os
from langchain.embeddings.openai import OpenAIEmbeddings
os.environ["OPENAI_API_KEY"] = "your-api-key"


embeddings = OpenAIEmbeddings()
# Load it back
loaded_vectorstore = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)

# Perform a similarity search
query = "test"
results = loaded_vectorstore.similarity_search(query, k=2)
for result in results:
    print(result.page_content)