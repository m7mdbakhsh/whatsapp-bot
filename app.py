from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import os

app = Flask(__name__)

@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    incoming_msg = request.values.get('Body', '').strip()
    response = MessagingResponse()
    msg = response.message()

    if incoming_msg in ['1', 'تقديم فكرة ابتكارية']:
        msg.body("🔗 لتقديم فكرة ابتكارية، يرجى تعبئة النموذج التالي:\n"
                 "https://docs.google.com/forms/d/e/1FAIpQLSe178sNy2ncQOqN4a8-lJFUUIR4hxshBPc7ijQDJs3r_OCKWQ/viewform?usp=header")

    elif incoming_msg in ['2', 'التواصل مع مختص']:
        msg.body("📞 سيتم تحويلك إلى المختص: د. سعود الواصلي.")

    elif incoming_msg in ['3', 'استشارة قانونية']:
        msg.body("⚖️ سيتم التواصل مع: أ. محمد بخش (مختص الاستشارات القانونية).")

    elif incoming_msg in ['4', 'متابعة حالة الطلب']:
        msg.body("📋 الرجاء تزويدنا برقم الطلب أو الاسم الثلاثي لتحديث حالة الطلب.")

    elif incoming_msg in ['5', 'أفضل 10 جامعات سعودية']:
        msg.body("🏅 أفضل 10 جامعات سعودية لعام 2024:\n")
        msg.media("https://www.dropbox.com/scl/fi/yi66daw7bv0swd2ty0v5h/Photo-21-07-2025-8-05-51-AM.png?rlkey=jts7duicisx5uisq1v0dttfi4&raw=1")

    else:
        msg.body("مرحباً بك في مساعد مركز الابتكار بجامعة الملك عبد العزيز 👋🏻\n\n"
                 "كيف يمكنني مساعدتك اليوم؟ اختر أحد الخيارات التالية:\n\n"
                 "🧠 1. تقديم فكرة ابتكارية\n"
                 "📞 2. التواصل مع مختص\n"
                 "⚖️ 3. استشارة قانونية\n"
                 "📋 4. متابعة حالة الطلب\n"
                 "🏅 5. أفضل 10 جامعات سعودية لعام 2024\n\n"
                 "يرجى كتابة رقم الخيار أو نسخه بالكامل.")

    return str(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
