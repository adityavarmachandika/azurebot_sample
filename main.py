from flask import Flask, request, Response
import asyncio
import logging
import os
import sys

from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext

# ------------------- CONFIG -------------------
APP_ID = os.getenv("APP_ID", "bbdadc98-3307-4825-a7ce-05daa9000111")
APP_PASSWORD = os.getenv("APP_PASSWORD")  # Must be set in environment
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
    try:
        user_text = turn_context.activity.text
        if not user_text:
            user_text = "<empty message>"
        logger.info(f"Received message: {user_text}")

        # Reply to user
        await turn_context.send_activity(f"You said: {user_text}")
    except Exception as e:
        logger.error(f"Error in bot logic: {e}", exc_info=True)
        # Optionally send a fallback message to user
        await turn_context.send_activity("Sorry, something went wrong.")

# ---------------- ROUTE ----------------------
@app.route("/api/messages", methods=["POST"])
def messages():
    try:
        # Accept JSON (including charset variants)
        content_type = request.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            logger.warning(f"Unsupported Media Type: {content_type}")
            return Response("Unsupported Media Type", status=415)

        auth_header = request.headers.get("Authorization", "")

        # Process activity via adapter
        try:
            asyncio.run(adapter.process_activity(request, auth_header, on_message_activity))
        except RuntimeError as e:
            # Handle nested event loop (rare on Render)
            logger.warning(f"Asyncio RuntimeError: {e}, retrying with new loop")
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(adapter.process_activity(request, auth_header, on_message_activity))
            loop.close()

        return Response(status=200)

    except Exception as e:
        logger.error(f"Error handling request: {e}", exc_info=True)
        return Response("Internal Server Error", status=500)

# ----------------- RUN ------------------------
if __name__ == "__main__":
    logger.info(f"Starting Flask Bot on port {PORT}")
    app.run(host="0.0.0.0", port=PORT)
