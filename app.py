from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import datetime
import threading
import time

app = Flask(__name__)
user_state = {}
admin_number = '+966555582182'
admin_password = '5555'
admin_otp = '1982'  # OTP ثابت للتجربة

@app.route('/ping')
def ping():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"✅ Ping received at {now}")
    return f"✅ I'm awake! {now}"

@app.route('/bot', methods=['POST'])
def whatsapp_reply():
    try:
        incoming_msg = request.values.get('Body', '').strip()
        sender_number = request.values.get('From', '').replace('whatsapp:', '')
        response = MessagingResponse()
        msg = response.message()

        # الرد التلقائي لأي رسالة جديدة
        if sender_number not in user_state:
            msg.body("مرحباً بك في مساعد مركز الابتكار بجامعة الملك عبد العزيز 👋🏻\n"
                     "كيف يمكنني مساعدتك اليوم؟ اختر أحد الخيارات التالية:\n"
                     "1. زائر / مخترع\n"
                     "2. إدارة مركز الابتكار وريادة الأعمال")
            user_state[sender_number] = 'main_menu'
            return str(response)

        # التحقق من OTP
        if user_state.get(sender_number) == 'awaiting_otp':
            if incoming_msg == admin_otp:
                msg.body("✅ تم التحقق بنجاح، أهلاً بك في لوحة المختص.\n"
                         "يرجى اختيار الإدارة:\n"
                         "1. مدير المركز\n"
                         "2. نائب مدير المركز للابتكار\n"
                         "3. نائب مدير المركز لنقل التقنية\n"
                         "4. نائب مدير المركز لتتجير المعرفة\n"
                         "5. نائب مدير المركز لريادة الأعمال")
                user_state[sender_number] = 'admin_menu'
            else:
                msg.body("❌ رمز التحقق غير صحيح. حاول مرة أخرى.")
            return str(response)

        # التحقق من الرقم السري
        if user_state.get(sender_number) == 'awaiting_password':
            if incoming_msg == admin_password:
                user_state[sender_number] = 'awaiting_otp'
                msg.body("🔐 رمز التحقق (OTP) هو: 1982\nيرجى إدخاله للمتابعة.")
            else:
                msg.body("❌ الرقم السري غير صحيح. حاول مرة أخرى.")
            return str(response)

        # القائمة الرئيسية
        if user_state.get(sender_number) == 'main_menu':
            if incoming_msg == '1':
                msg.body("🧠 قائمة الزائر / المخترع:\n"
                         "1. تقديم فكرة ابتكارية\n"
                         "2. التواصل مع المختص\n"
                         "3. استشارة قانونية\n"
                         "4. متابعة حالة الطلب\n"
                         "5. أسئلة شائعة\n"
                         "6. القائمة الرئيسية")
                user_state[sender_number] = 'visitor_menu'
                return str(response)

            elif incoming_msg == '2':
                if sender_number == admin_number:
                    msg.body("أهلاً يا محمد بخش 👋🏻\nيرجى إدخال الرقم السري للمتابعة.")
                    user_state[sender_number] = 'awaiting_password'
                else:
                    msg.body("🚫 هذا الخيار مخصص للإدارة فقط.")
                return str(response)

        # قائمة الزائر
        if user_state.get(sender_number) == 'visitor_menu':
            if incoming_msg == '1':
                msg.body("🔗 لتقديم فكرة ابتكارية:\n"
                         "https://docs.google.com/forms/d/e/1FAIpQLSe178sNy2ncQOqN4a8-lJFUUIR4hxshBPc7ijQDJs3r_OCKWQ/viewform?usp=header")
            elif incoming_msg == '2':
                msg.body("📞 سيتم تحويلك إلى المختص: د. سعود الواصلي.")
            elif incoming_msg == '3':
                msg.body("⚖️ سيتم التواصل مع: أ. محمد بخش (الاستشارات القانونية).")
            elif incoming_msg == '4':
                msg.body("📋 الرجاء تزويدنا برقم الطلب أو الاسم الثلاثي.")
            elif incoming_msg == '5':
                msg.body("⁉️ الأسئلة الشائعة:\n- ما هي براءة الاختراع؟\n- كيف أبدأ؟\n- هل الفكرة قابلة للتسجيل؟")
            elif incoming_msg == '6':
                msg.body("مرحباً بك من جديد 👋🏻\n"
                         "1. زائر / مخترع\n"
                         "2. إدارة مركز الابتكار وريادة الأعمال")
                user_state[sender_number] = 'main_menu'
            else:
                msg.body("❓ يرجى اختيار رقم من القائمة.")
            return str(response)

        # قائمة الإدارة بعد التحقق
        if user_state.get(sender_number) == 'admin_menu':
            if incoming_msg == '1':
                msg.body("أهلاً بك في إدارة: مدير المركز\nالمسؤول: د. سعود الواصلي")
            elif incoming_msg == '2':
                msg.body("أهلاً بك في إدارة: نائب مدير المركز للابتكار\nالمسؤولة: د. ليلى أحمد باهمام")
            elif incoming_msg == '3':
                msg.body("أهلاً بك في إدارة: نائب مدير المركز لنقل التقنية\n(شاغر حاليًا)")
            elif incoming_msg == '4':
                msg.body("أهلاً بك في إدارة: نائب مدير المركز لتتجير المعرفة\nالمسؤول: د. رائد إسماعيل فلمبان")
            elif incoming_msg == '5':
                msg.body("أهلاً بك في إدارة: نائب مدير المركز لريادة الأعمال\nالمسؤول: د. حسن علي السقاف")
            else:
                msg.body("❓ يرجى اختيار رقم من القائمة.")
            return str(response)

        # رد افتراضي
        msg.body("❓ يرجى اختيار أحد الأرقام من القائمة.")
        return str(response)

    except Exception as e:
        print(f"❌ خطأ أثناء التنفيذ: {e}")
        return "❌ خطأ في الخادم", 500

def keep_alive():
    while True:
        try:
            print("🔁 إرسال Ping للحفاظ على النشاط...")
            requests.get('https://whatsapp-bot-bx3b.onrender.com/ping')
            print("✅ تم إرسال Ping")
        except Exception as e:
            print("❌ خطأ في Ping:", e)
        time.sleep(300)

if __name__ == '__main__':
    threading.Thread(target=keep_alive).start()
    app.run()
