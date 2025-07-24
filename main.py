import os
from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/digikey", methods=["GET"])
def get_digikey_info():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing URL"}), 400

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Extragem câmpurile de interes
        mpn = soup.find("span", {"data-testid": "manufacturer-part-number"})
        stock = soup.find("span", {"data-testid": "availability-msg"})
        price = soup.find("span", {"data-testid": "pricing"})
        delivery = soup.find("div", string=lambda t: t and "lead time" in t.lower())

        return jsonify({
            "mpn": mpn.text.strip() if mpn else "N/A",
            "stock": stock.text.strip() if stock else "N/A",
            "price": price.text.strip() if price else "N/A",
            "delivery": delivery.text.strip() if delivery else "N/A",
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
