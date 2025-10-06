from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/messages", methods=["POST"])
def messages():
    # Get the incoming JSON payload
    data = request.json
    print("Incoming activity from Bot Service:")
    print(data)

    # Respond with 200 OK
    # (Bot Service expects a 200 response, even if you do nothing)
    return jsonify({"status": "received"}), 200

if __name__ == "__main__":
    # Run on port 3978 (common for Bot Framework testing)
    app.run(host="0.0.0.0", port=3978)
