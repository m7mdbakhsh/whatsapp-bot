from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()
    msg = response.message()

    if incoming_msg in ['1', '١']:
        msg.body("رابط تقديم فكرة براءة اختراع:\nhttps://docs.google.com/forms/d/e/1FAIpQLSe178sNy2ncQOqN4a8-lJFUUIR4hxshBPc7ijQDJs3r_OCKWQ/viewform?usp=header")
    elif incoming_msg in ['2', '٢']:
        msg.body("للتواصل مع مختص:\nالدكتور / سعود الواصلي")
    elif incoming_msg in ['3', '٣']:
        msg.body("للاستفسارات القانونية:\nالأستاذ / محمد بخش")
    elif incoming_msg in ['4', '٤']:
        msg.body("لمتابعة الطلبات، يرجى الرد بكلمة: متابعة")
    elif incoming_msg in ['5', '٥']:
        msg.body("أفضل 10 جامعات سعودية لعام 2024")
        msg.media("https://dl.dropboxusercontent.com/scl/fi/yi66daw7bv0swd2ty0v5h/Photo-21-07-2025-8-05-51-AM.png?rlkey=jts7duicisx5uisq1v0dttfi4&st=snrudf7q")
    else:
        msg.body(
            "أهلًا بك 👋\n"
            "اختر أحد الخيارات التالية:\n\n"
            "1. تقديم فكرة براءة اختراع\n"
            "2. التواصل مع مختص\n"
            "3. استفسار قانوني\n"
            "4. متابعة الطلب\n"
            "5. أفضل 10 جامعات سعودية لعام 2024"
        )

    return str(response)

if __name__ == "__main__":
    app.run()

