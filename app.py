from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').strip().lower()
    response = MessagingResponse()
    msg = response.message()

    if incoming_msg in ["مرحبا", "السلام عليكم", "hi", "hello"]:
        reply = (
            "🎓 مرحبًا بك في مركز الابتكار – جامعة الملك عبدالعزيز.\n\n"
            "يسعدنا دعمك في رحلتك الابتكارية، سواء كنت صاحب فكرة، أو باحث عن حماية، أو مهتم بتحويل ابتكارك إلى منتج.\n\n"
            "🔽 اختر أحد الخيارات التالية للمتابعة:\n"
            "1️⃣ تحليل فكرة\n"
            "2️⃣ تسجيل براءة\n"
            "3️⃣ استشارة قانونية\n"
            "4️⃣ تتجير وتسويق\n"
            "✍️ أو أرسل وصفًا موجزًا لفكرتك."
        )

    elif incoming_msg in ["3", "استشارة قانونية", "استشاره قانونيه", "استشارة", "محامي"]:
        reply = (
            "👨‍⚖️ تم استلام طلبك للاستشارة القانونية.\n"
            "الاسم: محمد بخش\n"
            "رقم الجوال: 0555582182\n"
            "📌 سيتم التواصل معك من الفريق القانوني قريبًا."
        )

    else:
        reply = "✅ شكرًا لرسالتك، سيتم تحويلها للفريق المختص، وسنرد عليك قريبًا."

    msg.body(reply)
    return str(response)

if __name__ == "__main__":
    app.run()
