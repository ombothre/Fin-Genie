from flask import Flask,Blueprint, jsonify, request
import os
from langchain.agents import AgentExecutor
from config import utils
from services.ai_agent import AiAgent
from helpers.file_man import File

UPLOAD = 'static/'
state = {'latest': None}

app = Flask(__name__)

@app.route('/',methods=['GET'])
def docs():
    return "API"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # Check if a file was selected
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    # Check if the file has a .csv extension
    if not file.filename.lower().endswith('.csv'):
        return jsonify({"error": "File is not a CSV"}), 400

    # Save the file to the upload folder
    file_path = os.path.join(UPLOAD, file.filename)
    try:
        file.save(file_path)
        state['latest'] = file_path
    except Exception as e:
        print(str(e))

    return jsonify({"message": "File uploaded successfully", "file_path": file_path})

@app.route('/process', methods=['POST'])
def process_query():
    try:
        data = request.get_json()
        query = data['query']
        print("Received query:", query)

        # File Processing
        file = File(state['latest'])
        df = file.data
        metadata = file.meta
        print("File processed successfully.")

        # AI Agent
        agent_model = AiAgent(utils.MODEL_NAME)
        agent: AgentExecutor = agent_model.setup_agent(df, metadata)

        query_input = f"""
        query: {query}
        Your task is to write code to satisfy the query and also execute.
        Use the tools provided to execute the code.
        Output the stdout of the code exectution.
        The output should be formatted so that each row appears on a new line.
        
        Here is the dataset schema:
        {metadata['Schema']}
        """
        print("Query input prepared.")

        result = agent.invoke({"input": query_input, "chat_history": ""})
        print("Agent Result:", result)

        return jsonify({"response": result.get('output', "No output provided")}), 200
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"Error": str(e)}), 400

# if __name__ == "__main__":
#     app.run(debug=True)