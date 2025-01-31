import os
from flask import Flask, jsonify, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route('/detect-phishing', methods=['GET', 'POST'])
def detect_phishing():
    email_text = request.args.get("mail") if request.method == "GET" else request.json.get("mail")

    if not email_text:
        return jsonify({"error": "No email provided"}), 400

    prompt = f"Analyze the following email for phishing indicators and provide a risk assessment:\n\n{email_text}\n\nGive a short verdict and reasoning."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert analyzing emails for phishing threats."},
                {"role": "user", "content": prompt}
            ]
        )

        analysis = response.choices[0].message.content
        return jsonify({"analysis": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/detect-malware', methods=['GET', 'POST'])
def detect_malware():
    code = request.args.get("code") if request.method == "GET" else request.json.get("code")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    prompt = f"Analyze the following code for malware indicators and provide a risk assessment:\n\n{code}\n\nGive a short verdict and reasoning."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity expert analyzing code for malware indicators."},
                {"role": "user", "content": prompt}
            ]
        )

        analysis = response.choices[0].message.content
        return jsonify({"analysis": analysis})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
