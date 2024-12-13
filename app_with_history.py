from flask import Flask, request, render_template, jsonify, session, send_from_directory
from flask_session import Session
from langchain_openai import ChatOpenAI  # Updated import from langchain-openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
import os

openai_api_key = "your-api-key"
os.environ["OPENAI_API_KEY"] = openai_api_key


app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize LangChain for NLP
llm = ChatOpenAI(model="gpt-4o",api_key=openai_api_key)

# Initialize FAISS for document retrieval
embeddings = OpenAIEmbeddings()
index = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)



@app.route('/')
def home():
    return render_template('index.html')  # Basic HTML page for interface


@app.route('/query', methods=['POST'])
def query():
    user_query = request.json.get("query")

    # Ensure chat history is initialized for the session
    if "history" not in session:
        session["history"] = []

    # Add user's query to history
    session["history"].append({"role": "user", "content": user_query})

    # Retrieve similar documents from the FAISS index
    similar_docs = index.similarity_search(user_query, k=7)

    context = "\n".join([doc.page_content for doc in similar_docs])
    print(similar_docs)
    # Generate a response using the chat history and the retrieved context
    response_text = generate_response(session["history"], context)

    # Add assistant's response to history
    session["history"].append({"role": "assistant", "content": response_text})

    return jsonify({"response": response_text})


def generate_response(chat_history, context):
    # Template prompt for MIA
    template_prompt = (
        "You are Montclair Intelligent Assistant (MIA), an academic advisor for Montclair State University. You are on the Montclair State University website (https://www.montclair.edu/). And this is the graduate Computer Science website https://www.montclair.edu/academics/computer-science/"
        "You help students with questions about courses, academic guidance, and campus services. "
        "Strictly use the following context to improve your answers:\n"
        f"{context}\n\n"
        "Respond in a friendly and informative manner. "
    )

    # Combine the template with chat history
    history_text = "\n".join([f"{item['role'].capitalize()}: {item['content']}" for item in chat_history])
    print(history_text)
    full_prompt = f"{template_prompt}\n\n{history_text}\nAssistant:"
    print("full_prompt",full_prompt)

    # Generate response using the LLM
    # response = llm.generate([full_prompt])
    # return response.generations[0][0].text  # Access the generated text
    response = llm([{"role": "system", "content": full_prompt}])
    print(response)
    return response.content  # Access the generated text


if __name__ == '__main__':
    app.run(debug=True)
