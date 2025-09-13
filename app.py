from flask import Flask, request, jsonify
import openai, os

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    niche = data.get("niche", "loja")
    message = data.get("message", "")

    prompt = f"""
    Você é o ShopIA, um assistente de lojas do nicho: {niche}.
    Responda de forma prática e útil para ajudar o dono da loja.
    Mensagem do usuário: {message}
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "Você é um assistente para negócios."},
                      {"role": "user", "content": prompt}]
        )
        reply = response["choices"][0]["message"]["content"].strip()
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "ShopIA está online! Use /chat com POST."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
