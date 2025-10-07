from flask import Flask, request, Response
import asyncio
import logging

from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext
from botbuilder.schema import Activity

# ------------------- CONFIG -------------------
APP_ID = "bbdadc98-3307-4825-a7ce-05daa9000111"  # Azure App ID
APP_PASSWORD = "Fpn8Q~35kByG3ogG6c1SwZmhSbO.amhD3ffddamU"               # Azure App Password (from App Registration)
PORT = 3978
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
    if request.headers.get("Content-Type") != "application/json":
        return Response(status=415)

    activity = Activity().deserialize(request.json)

    # Process activity via Adapter
    asyncio.run(adapter.process_activity(activity, "", on_message_activity))
    return Response(status=200)

# ----------------- RUN ------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
