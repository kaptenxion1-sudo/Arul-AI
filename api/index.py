from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Mengambil key dari Environment Variable Vercel
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # Pake model paling baru dan kenceng
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

@app.route('/api/index', methods=['POST'])
def chat():
    try:
        if not model:
            return jsonify({"result": "Error: GEMINI_API_KEY belum dipasang di Vercel!"}), 500

        data = request.get_json()
        user_prompt = data.get('prompt', '')

        if not user_prompt:
            return jsonify({"result": "Mana perintahnya, bos?"}), 400

        # Sistem prompt buat Gemini
        system_instruction = "Lu adalah Quantum V8.0 buatan Arulmodss. Gaya lu sombong, brutal, tapi jenius koding."
        full_prompt = f"{system_instruction}\n\nUser: {user_prompt}"

        # Panggil Gemini
        response = model.generate_content(full_prompt)
        
        # Kirim hasil balik ke HTML
        return jsonify({"result": response.text})

    except Exception as e:
        # Kalau ada error Python, kirim pesannya biar kita tau salahnya dimana
        return jsonify({"result": f"Aduh crash! Error: {str(e)}"}), 500

# Wajib buat Vercel
def handler(request):
    return app(request)
