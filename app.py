from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=["POST"])
def reply_whatsapp():
    incoming_msg = request.values.get('Body', '').lower()
    print(f"Received message: {incoming_msg}")

    resp = MessagingResponse()
    resp.message("أهلًا بك! تم استلام رسالتك ✅")
    return str(resp)
