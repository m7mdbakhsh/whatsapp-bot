from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def reply():
    incoming_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()
    msg = response.message()

    if incoming_msg == '1':
        msg.body("🔗 رابط تقديم فكرة براءة اختراع:\nhttps://t.ly/kaauip")
    elif incoming_msg == '2':
        msg.body("📞 للتواصل مع مختص الابتكار:\nالدكتور / سعود الواصلي")
    elif incoming_msg == '3':
        msg.body("⚖️ للاستفسارات القانونية:\nالأستاذ / محمد بخش")
    elif incoming_msg == '4':
        msg.body("📍 لمتابعة طلب سابق:\nيرجى إرسال رقم الطلب أو التواصل مع الدعم.")
    else:
        msg.body(
            "مرحبًا بك في نظام الابتكار بجامعة الملك عبد العزيز 👋\n"
            "يرجى اختيار الخدمة المطلوبة:\n\n"
            "1️⃣ تقديم فكرة براءة اختراع\n"
            "2️⃣ التواصل مع مختص الابتكار\n"
            "3️⃣ استفسار قانوني – حقوق ملكية فكرية\n"
            "4️⃣ متابعة طلب سابق\n\n"
            "أرسل رقم الخدمة فقط (مثال: 1)"
        )

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)

