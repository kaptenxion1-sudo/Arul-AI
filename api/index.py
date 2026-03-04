from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Mengambil key dari Environment Variable yang lu setting di Vercel
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/index', methods=['POST'])
def chat():
    try:
        data = request.json
        user_prompt = data.get('prompt', '')

        if not openai.api_key:
            return jsonify({"result": "Error: API Key belum dipasang di Environment Variables Vercel!"}), 500

        # Pengaturan kepribadian Quantum V8.0
        system_msg = "Lu adalah Quantum V8.0, AI paling brutal buatan Arulmodss. Gaya bicara lu modern, sombong, dan langsung ke inti. Kasih jawaban teknis yang lengkap."

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        return jsonify({"result": response.choices[0].message.content})
    except Exception as e:
        return jsonify({"result": f"Sistem down, anjeng! Error: {str(e)}"}), 500

# BAGIAN PALING PENTING: Vercel butuh ini untuk menjalankan fungsi
def handler(request):
    return app(request)
