from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()

    if 'مرحبا' in incoming_msg:
        msg.body("أهلاً وسهلاً بك! كيف أقدر أساعدك اليوم؟ 🤖")
    else:
        msg.body("تم استلام رسالتك! 🚀")

    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
