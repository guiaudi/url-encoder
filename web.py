import os
from flask import Flask, render_template, request, redirect, abort, jsonify
from service import criar_url_curta, buscar_url_original
from database import get_connection

app = Flask(__name__)

# ==========================
#       HEALTH CHECK
# ==========================

@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        conn.close()

        return jsonify({
            "status": "ok",
            "service": "url-encoder",
            "database": "ok"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "service": "url-encoder",
            "database": "down"
        }), 500

# =========================
# Configurações via ambiente
# =========================
APP_NAME = os.getenv("APP_NAME", "url-encoder")
APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 5000))
BASE_URL = os.getenv("BASE_URL", "http://localhost")

# =========================
# Rotas
# =========================
@app.route("/", methods=["GET", "POST"])
def index():
    short_url = None

    if request.method == "POST":
        original_url = request.form.get("url")

        if not original_url:
            abort(400, "URL não informada")

        codigo = criar_url_curta(original_url)
        short_url = f"{BASE_URL}/{codigo}"

    return render_template("index.html", short_url=short_url)


@app.route("/<codigo>")
def redirecionar(codigo):
    url_original = buscar_url_original(codigo)

    if not url_original:
        abort(404, "URL não encontrada")

    return redirect(url_original)


# =========================
# Inicialização
# =========================
if __name__ == "__main__":
    print(f" {APP_NAME} iniciado em {APP_HOST}:{APP_PORT}")
    app.run(host=APP_HOST, port=APP_PORT)
