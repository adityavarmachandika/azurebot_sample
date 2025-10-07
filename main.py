from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/messages", methods=["POST"])
def messages():
    # Parse incoming activity from Azure Bot Service
    activity = request.get_json()

    # Extract message text if available
    user_text = activity.get("text", "")

    # Create response activity (same format)
    response_activity = {
        "type": "message",
        "text": f"You said: {user_text}"
    }

    print(f"Received message: {user_text}")
    print(f"Responding with: {response_activity['text']}")
    # Send the response back (HTTP 200 + JSON)
    return jsonify(response_activity), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3978)
