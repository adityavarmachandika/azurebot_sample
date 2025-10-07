from flask import Flask, request, jsonify
import logging
app = Flask(__name__)

# Configure logging
logging.basicConfig(
    level=logging.INFO,                      # Log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",  # Format
)
 
logger = logging.getLogger(__name__)  # Create a logger for this module

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
    logger.info(f"Received message: {user_text}")
    
    # Send the response back (HTTP 200 + JSON)
    return jsonify(response_activity), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3978)
