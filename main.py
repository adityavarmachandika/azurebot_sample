from flask import Flask, request, Response
import asyncio
import logging
import os

from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

# ------------------- CONFIG -------------------
# Load App ID and Password from environment variables for security
APP_ID = os.getenv("APP_ID", "bbdadc98-3307-4825-a7ce-05daa9000111")
APP_PASSWORD = "Fpn8Q~35kByG3ogG6c1SwZmhSbO.amhD3ffddamU" # Must be set in environment
PORT = int(os.getenv("PORT", 3978))

if not APP_PASSWORD:
    raise RuntimeError("APP_PASSWORD not set in environment")

# ----------------------------------------------

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)

# Bot Framework Adapter
adapter_settings = BotFrameworkAdapterSettings(APP_ID, APP_PASSWORD)
adapter = BotFrameworkAdapter(adapter_settings)

# ----------------- BOT LOGIC ------------------
async def on_message_activity(turn_context: TurnContext):
    user_text = turn_context.activity.text
    logger.info(f"Received message: {user_text}")
    await turn_context.send_activity(f"You said: {user_text}")

# ---------------- ROUTE ----------------------
@app.route("/api/messages", methods=["POST"])
def messages():
    # ---------------- FIX for 415 ----------------
    # Accept Content-Type: application/json and variants (like charset=utf-8)
    if "application/json" not in request.headers.get("Content-Type", ""):
        logger.warning(f"Unsupported Media Type: {request.headers.get('Content-Type')}")
        return Response(status=415)

    # Deserialize incoming activity
    activity = Activity().deserialize(request.json)

    # Process the activity via the Adapter and Bot logic
    asyncio.run(adapter.process_activity(activity, "", on_message_activity))
    return Response(status=200)

# ----------------- RUN ------------------------
if __name__ == "__main__":
    logger.info(f"Starting Flask Bot on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
