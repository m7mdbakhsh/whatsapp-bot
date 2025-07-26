from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsup", methods=["POST"])
def simple_reply():
    response = MessagingResponse()
    response.message("✅ البوت يعمل الآن! أهلاً وسهلاً بك 🌟")
    return str(response)

if __name__ == "__main__":
    app.run()
