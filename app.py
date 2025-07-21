from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg == "1" or "تقديم" in incoming_msg:
        msg.body("📩 رابط تقديم فكرة براءة اختراع:\nhttps://docs.google.com/forms/d/e/1FAIpQLSe178sNy2ncQOqN4a8-lJFUUIR4hxshBPc7ijQDJs3r_OCKWQ/viewform?usp=header")
    elif incoming_msg == "2" or "التواصل" in incoming_msg:
        msg.body("📞 سيتم تحويلك إلى المختص:\nالدكتور / سعود الواصلي")
    elif incoming_msg == "3" or "قانونية" in incoming_msg:
        msg.body("⚖️ سيتم تحويلك إلى المستشار:\nالأستاذ / محمد بخش")
    elif incoming_msg == "4" or "متابعة" in incoming_msg:
        msg.body("📌 لمتابعة حالة الطلب، يرجى التواصل مع مسؤول المركز.")
    else:
        msg.body("""مرحباً بك في مساعد مركز الابتكار بجامعة الملك عبد العزيز 👋🏻

كيف يمكنني مساعدتك اليوم؟ اختر أحد الخيارات التالية:

1️⃣ تقديم فكرة ابتكارية  
2️⃣ التواصل مع مختص  
3️⃣ استشارة قانونية  
4️⃣ متابعة حالة الطلب

يرجى كتابة رقم الخيار أو نسخه بالكامل.""")

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
