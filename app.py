import os
import json
from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()  

app = Flask(__name__)
CORS(app)
client = OpenAI(
  api_key=os.getenv("OPENAI_API_KEY"),
)

@app.route('/api/runcode', methods=['POST'])
def RunCode():
    data = request.get_json()
    code = data.get('code')
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=100,
        messages=[
            {"role": "assistant", "content": f"Evaluate the code below and return output only. If there a syntax error, return 'Syntax error' If there is no valid output, return 'No output.' If no code is submitted return 'No code submitted'. The code is: {code if code else 'No code submitted'}"}
        ]
    )
    print(jsonify(completion.choices[0].message.content))
    return jsonify(completion.choices[0].message.content)
    

@app.route('/api/submitcode', methods=['POST'])
def SubmitCode():
    data = request.get_json()
    code = data.get('code')
    practice = data.get('practice')
    exampleOutput = json.dumps({"evaluation": "Correct or Incorrect", "feedback": "some constructive feedback"})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=200,
        messages=[
            {"role": "assistant", "content": f"Evaluate the submitted code to determine if it completely and correctly solves the given practice problem. First, check if the code submission is not empty. If no code is submitted, return 'Incorrect' with feedback 'No code submitted'. If code is submitted, ensure that it addresses all aspects of the problem. The evaluation should be strict: any partial solution or incorrect implementation should be marked as 'Incorrect'. When providing feedback for incorrect or incomplete submissions, focus solely on identifying the elements or aspects that are missing or incorrect in the submitted code. Avoid giving direct solutions or hints on how to solve the problem. The goal is to encourage the user to think critically and solve the problem independently. If the code fully solves the problem, mark it as 'Correct'. After the correctness evaluation, provide constructive feedback aimed at beginners, focusing on best practices, code quality and adherence to clean coding principles.. The output should be a json like this: {exampleOutput}. The submited code is {code if code else 'No code submitted'}, practice problem is ${practice}"}
        ]
    )
    print(completion.choices[0].message.content)
    return jsonify(completion.choices[0].message.content)

@app.route('/api/explain', methods=['POST'])
def ExplainCode():
    data = request.get_json()
    code = data.get('code')
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=500,
        messages=[
            {"role": "assistant", "content": f"Explain the following code to a beginner using comments. Add an empty line between each explaination. If the code is incorrect or contains a syntax error, explain the error to the user in simple and easy to understand manner.  If no code is submitted return 'No code submitted'. The code is: {code if code else 'No code submitted'}"}
        ]
    )
    print(jsonify(completion.choices[0].message.content))
    return jsonify(completion.choices[0].message.content)

@app.route('/api/generate', methods=['POST'])
def GeneratePractice():
    data = request.get_json()
    topic = data.get('topic')
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=500,
        messages=[
            {"role": "assistant", "content": f"Generate 5 new practice problems for beginners, focusing on {topic}. Each problem should be presented as a standalone statement without any preceding numbers or labels. Avoid labeling with numbers or alphabets. The problems should be unique, testing different aspects of the topic"}
        ]
    )
    print(jsonify(completion.choices[0].message.content))
    return jsonify(completion.choices[0].message.content)
    
@app.route('/api/chat', methods=['POST'])
def Chat():
    data = request.get_json()
    question = data.get('question')
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        max_tokens=200,
        messages=[
            {"role": "assistant", "content": f"You are a helpful assistant for beginner programmers. Based on the user's question, provide a concise response that will help the user.  User's question is: {question}"}
        ]
    )
    print(completion.choices[0].message.content)
    return jsonify(completion.choices[0].message.content)


if __name__ == '__main__':
    app.run(debug=True)



