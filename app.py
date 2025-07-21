from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "مساعد مركز الابتكار يعمل بنجاح ✅"

@app.route("/whatsapp", methods=["POST"])
def reply_whatsapp():
    incoming_msg = request.form.get('Body', '').strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    if incoming_msg in ['مرحبا', 'السلام عليكم', 'ابدأ', 'start']:
        msg.body(
            "مرحبًا بك في *مساعد مركز الابتكار بجامعة الملك عبد العزيز* 👋🏼\n\n"
            "كيف يمكنني مساعدتك اليوم؟ اختر أحد الخيارات التالية:\n\n"
            "1️⃣ استشارة قانونية\n"
            "2️⃣ تسجيل فكرة ابتكارية\n"
            "3️⃣ متابعة حالة الطلب\n"
            "4️⃣ التواصل مع مختص\n\n"
            "يرجى كتابة رقم الخيار أو نسخه بالكامل."
        )

    elif incoming_msg == '1' or 'استشارة قانونية' in incoming_msg:
        msg.body("تم تحويل طلبك إلى المستشار القانوني.\nالاسم: محمد بخش\nالجوال: 0555582182")

    else:
        msg.body("عذرًا، لم أفهم طلبك.\nمن فضلك اختر رقم من القائمة أو اكتب *ابدأ* لعرض الخيارات.")

    return str(resp)

if __name__ == "__main__":
    app.run()
