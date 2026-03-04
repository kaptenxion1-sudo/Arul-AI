from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Mengambil key dari Environment Variable Vercel
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/index', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_prompt = data.get('prompt', '')

        if not openai.api_key:
            return jsonify({"result": "Error: API KEY belum dipasang di Vercel!"}), 500

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Lu adalah Quantum V8.0 buatan Arulmodss. Gaya lu sombong dan jenius koding."},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"result": f"Aduh crash! Error: {str(e)}"}), 500

# PENTING: Jangan pake def handler(request). 
# Cukup baris di bawah ini biar Vercel ngenalin Flask-nya.
app = app
