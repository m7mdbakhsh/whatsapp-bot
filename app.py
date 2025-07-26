from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsup", methods=["POST"])
def simple_reply():
    print("📩 تم استلام رسالة من واتساب!")  # هذا فقط للتجربة
    response = MessagingResponse()
    response.message("🌞 البوت يعمل الآن! أهلاً وسهلاً بك")
    return str(response)
