from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/api/index', methods=['POST'])
def chat():
    try:
        # Cek apakah ada data JSON yang masuk
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"result": "Mana perintahnya, bos? Isi dulu!"}), 400

        user_prompt = data.get('prompt')

        # Cek API Key
        if not openai.api_key:
            return jsonify({"result": "Error: API KEY belum lu pasang di Vercel!"}), 500

        # Panggil OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Lu adalah Quantum V8.0 buatan Arulmodss. Gaya lu sombong, brutal, tapi jenius koding."},
                {"role": "user", "content": user_prompt}
            ]
        )
        
        # Kirim hasil balik ke HTML
        return jsonify({"result": response.choices[0].message.content})

    except Exception as e:
        # Kalau ada error Python, kirim pesannya biar kita tau salahnya dimana
        return jsonify({"result": f"Aduh, ada yang jebol: {str(e)}"}), 500

# Wajib buat Vercel
def handler(request):
    return app(request)
