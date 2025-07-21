from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def reply_whatsapp():
    incoming_msg = request.form.get('Body')
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg == '1':
        msg.body("أهلاً بك! 🌟\nلو عندك فكرة ابتكارية وتبغى تقدمها، اضغط الرابط التالي:\nhttps://docs.google.com/forms/d/e/1FAIpQLSe178sNy2ncQOqN4a8-lJFUUIR4hxshBPc7ijQDJs3r_OCKWQ/viewform?usp=header")
    elif incoming_msg == '2':
        msg.body("للتواصل معنا مباشرة، أرسل لنا استفسارك وسنرد عليك في أقرب وقت 💬")
    elif incoming_msg == '3':
        msg.body("نشكرك على زيارتك لنا، نتمنى لك يومًا جميلًا 🌈")
    elif incoming_msg == '4':
        msg.body("هذه قائمة بالخدمات التي نقدمها:\n- استشارات ابتكارية\n- دعم فني\n- تسجيل براءات\n- تطوير أفكار 💡")
    elif incoming_msg == '5':
        msg.body("أفضل 10 جامعات سعودية لعام 2024 🎓")
        msg.media("https://www.dropbox.com/scl/fi/yi66daw7bv0swd2ty0v5h/Photo-21-07-2025-8-05-51-AM.png?rlkey=jts7duicisx5uisq1v0dttfi4&raw=1")
    else:
        msg.body("مرحباً بك في مساعد الابتكار! ✨\nأرسل رقم الخدمة التي ترغب بها:\n1. تقديم فكرة ابتكارية\n2. التواصل معنا\n3. إنهاء المحادثة\n4. عرض خدماتنا\n5. أفضل 10 جامعات سعودية 2024")

    return str(resp)
