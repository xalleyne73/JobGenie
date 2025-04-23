from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from docx import Document

app = Flask(__name__)
CORS(app)  # 👈 needed for Bubble to connect without CORS issues

# Use environment variable (don't hardcode your key)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/edit-resume', methods=['POST'])
def edit_resume():
    try:
        data = request.json
        resume_text = data.get('resume')
        goal = data.get('goal', 'make it better')

        prompt = f"Improve this resume to be {goal}:\n\n{resume_text}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a resume editing assistant."},
                {"role": "user", "content": prompt}
            ],
            timeout=15
        )

        result = response['choices'][0]['message']['content']
        return jsonify({"edited_resume": result})

    except Exception as e:
        # 👇 This will send the error as JSON so Bubble can read it
        return jsonify({"error": str(e)}), 500

# Note: Render will use gunicorn, so this is safe to leave
if __name__ == '__main__':
    app.run(debug=True)
