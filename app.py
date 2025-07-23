from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import datetime
import threading
import time

app = Flask(__name__)
force_restart = "v1.1.3"  # تحديث يدوي لنسخة Render

# ✅ رابط Google Sheets الخاص بك
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzWJBvR1h8mu0EP8kp4_t8xEBa6fOcVefHHbjpg5sSd92KSN8zgHqjxiEL7NpLeygET/exec'

# ✅ تخزين حالة الطلب
user_state = {}

# ✅ لحفظ البيانات في Google Sheets
def save_to_google_sheet(phone, message):
    data = {
        'phone': phone,
        'message': message
    }
    try:
        requests.post(GOOGLE_SCRIPT_URL, json=data)
    except Exception as e:
        print(f"❌ خطأ في الإرسال إلى Google Sheets: {e}")

# ✅ مسار Ping لإبقاء السيرفر نشط
@app.route('/ping')
def ping():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"✅ Ping received at {now}")
    return f"✅ I'm awake! {now}"

# ✅ المسار الرئيسي للرد على WhatsApp
@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    try:
        incoming_msg = request.values.get('Body', '').strip()
        sender_number = request.values.get('From', '').replace('whatsapp:', '')

        # حفظ الرسالة في Google Sheets
        save_to_google_sheet(sender_number, incoming_msg)

        response = MessagingResponse()
        msg = response.message()

        if user_state.get(sender_number) == 'awaiting_password':
            if incoming_msg == 'bakhsh':
                msg.body("✅ يوجد حالياً 40 براءة اختراع مسجلة في المملكة العربية السعودية.")
            else:
                msg.body("❌ الرقم السري غير صحيح. حاول مرة أخرى.")
            user_state.pop(sender_number, None)
            return str(response)

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

        elif incoming_msg == '6':
            msg.body("🔒 هذا الخيار يتطلب رقم سري.\nيرجى إدخال الرقم السري للمتابعة:")
            user_state[sender_number] = 'awaiting_password'

        else:
            msg.body("مرحباً بك في مساعد مركز الابتكار بجامعة الملك عبد العزيز 👋🏻\n\n"
                     "كيف يمكنني مساعدتك اليوم؟ اختر أحد الخيارات التالية:\n\n"
                     "🧠 1. تقديم فكرة ابتكارية\n"
                     "📞 2. التواصل مع مختص\n"
                     "⚖️ 3. استشارة قانونية\n"
                     "📋 4. متابعة حالة الطلب\n"
                     "🏅 5. أفضل 10 جامعات سعودية\n"
                     "🔒 6. عدد البراءات في السعودية (يتطلب رقم سري)\n\n"
                     "يرجى كتابة رقم الخيار أو نسخه بالكامل.")

        return str(response)

    except Exception as e:
        print(f"❌ خطأ أثناء تنفيذ الكود: {e}")
        return "حدث خطأ في الخادم.", 500

# ✅ Ping تلقائي كل 5 دقائق (فقط لو شغلت محلياً أو على Render)
def keep_alive():
    while True:
        try:
            print("🔁 إرسال Ping للحفاظ على النشاط...")
            requests.get('https://whatsapp-bot-bx3b.onrender.com/ping')
            print("✅ تم إرسال Ping")
        except Exception as e:
            print("❌ حدث خطأ في Ping:", e)
        time.sleep(300)

# ✅ تشغيل الكود
if __name__ == '__main__':
    threading.Thread(target=keep_alive).start()
    app.run()
