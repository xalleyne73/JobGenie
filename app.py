from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os  # ✅ THIS LINE!
from docx import Document

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/edit-resume', methods=['POST'])
def edit_resume():
    data = request.json
    resume_text = data.get('resume')
    goal = data.get('goal', 'make it better')
    prompt = f"Improve this resume to be {goal}:\n\n{resume_text}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a resume editing assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    result = response['choices'][0]['message']['content']
    return jsonify({"edited_resume": result})

if __name__ == '__main__':
    app.run(debug=True)
