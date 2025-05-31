from flask import Flask, request, send_file, jsonify, Response
from flask_cors import CORS
import os
import csv
import time
import json

from scraper import obter_nome_empresa_e_leads

app = Flask(__name__)
CORS(app)

@app.route("/scrape-link", methods=["POST"])
def scrape_link():
    try:
        data = request.json
        cookie = data.get("cookie")
        empresa_url = data.get("empresa_url")

        if not cookie or not empresa_url:
            return jsonify({"error": "Cookie ou URL da empresa não enviado."}), 400

        nome, nomes = obter_nome_empresa_e_leads(cookie, empresa_url)
        return jsonify({"empresa": nome, "leads": nomes})

    except Exception as e:
        print("[ERRO LINK]:", str(e))
        return jsonify({"error": "Erro ao processar o link."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
