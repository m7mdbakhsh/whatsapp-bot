from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import requests
import datetime
import threading
import time

app = Flask(__name__)
user_state = {}
admin_auth = {}

ALLOWED_ADMIN_NUMBER = '+966555582182'
ADMIN_PASSWORD = '5555'
ADMIN_OTP = '1234'
DEPARTMENT_PASSWORDS = {
    '1': '1111',
    '2': '2222',
    '3': '3333',
    '4': '4444',
    '5': '5555'
}

@app.route('/ping')
def ping():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"✅ Ping received at {now}")
    return f"✅ I'm awake! {now}"

@app.route('/bakhsh', methods=['POST'])
def whatsapp_reply():
    try:
        incoming_msg = request.values.get('Body', '').strip()
        sender_number = request.values.get('From', '').replace('whatsapp:', '')

        print(f"✅ تم استلام رسالة من واتساب من الرقم {sender_number}: {incoming_msg}")

        response = MessagingResponse()
        msg = response.message()

        if sender_number not in user_state:
            msg.body("مرحباً بك في مساعد مركز الابتكار بجامعة الملك عبد العزيز 👋🏻\n"
                     "كيف يمكنني مساعدتك اليوم؟ اختر أحد الخيارات التالية:\n"
                     "1. زائر / مخترع\n"
                     "2. إدارة مركز الابتكار وريادة الأعمال")
            user_state[sender_number] = 'main_menu'
            return Response(str(response), mimetype="application/xml")

        state = user_state.get(sender_number)

        if state == 'main_menu':
            if incoming_msg == '1':
                msg.body("🧠 قائمة الزائر / المخترع:\n"
                         "1. تقديم فكرة ابتكارية\n"
                         "2. التواصل مع المختص\n"
                         "3. استشارة قانونية\n"
                         "4. متابعة حالة الطلب\n"
                         "5. أسئلة شائعة\n"
                         "6. القائمة الرئيسية")
                user_state[sender_number] = 'visitor_menu'
            elif incoming_msg == '2':
                if sender_number != ALLOWED_ADMIN_NUMBER:
                    msg.body("❌ هذا الخيار مخصص لإدارة المركز فقط.")
                else:
                    msg.body("🔒 يرجى إدخال كلمة المرور الخاصة بالإدارة:")
                    user_state[sender_number] = 'admin_password'
            else:
                msg.body("❓ يرجى اختيار رقم من القائمة.")
            return Response(str(response), mimetype="application/xml")

        if state == 'admin_password':
            if incoming_msg == ADMIN_PASSWORD:
                msg.body("✅ كلمة المرور صحيحة.\n📩 الآن، أدخل رمز التحقق OTP:")
                user_state[sender_number] = 'admin_otp'
            else:
                msg.body("❌ كلمة المرور غير صحيحة. حاول مرة أخرى.")
            return Response(str(response), mimetype="application/xml")

        if state == 'admin_otp':
            if incoming_msg == ADMIN_OTP:
                msg.body("✅ تم التحقق بنجاح.\nيرجى اختيار الإدارة:\n"
                         "1. مدير المركز\n"
                         "2. نائب مدير المركز للابتكار\n"
                         "3. نائب مدير المركز لنقل التقنية\n"
                         "4. نائب مدير المركز لتتجير المعرفة\n"
                         "5. نائب مدير المركز لريادة الأعمال")
                user_state[sender_number] = 'admin_menu'
            else:
                msg.body("❌ رمز التحقق غير صحيح. حاول مرة أخرى.")
            return Response(str(response), mimetype="application/xml")

        if state == 'visitor_menu':
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
            return Response(str(response), mimetype="application/xml")

        if state == 'admin_menu':
            if incoming_msg in ['1', '2', '3', '4', '5']:
                admin_auth[sender_number] = incoming_msg
                msg.body("🔐 يرجى إدخال الرقم السري الخاص بهذه الإدارة:")
                user_state[sender_number] = 'department_auth'
            else:
                msg.body("❓ يرجى اختيار رقم من القائمة.")
            return Response(str(response), mimetype="application/xml")

        if state == 'department_auth':
            dept_choice = admin_auth.get(sender_number)
            correct_password = DEPARTMENT_PASSWORDS.get(dept_choice)
            if incoming_msg == correct_password:
                if dept_choice == '1':
                    msg.body("✅ إدارة: مدير المركز\nالمسؤول: د. سعود الواصلي")
                elif dept_choice == '2':
                    msg.body("✅ إدارة: نائب مدير المركز للابتكار\nالمسؤولة: د. ليلى أحمد باهمام")
                elif dept_choice == '3':
                    msg.body("✅ إدارة: نائب مدير المركز لنقل التقنية\n(شاغر حاليًا)")
                elif dept_choice == '4':
                    msg.body("✅ إدارة: نائب مدير المركز لتتجير المعرفة\nالمسؤول: د. رائد إسماعيل فلمبان")
                elif dept_choice == '5':
                    msg.body("✅ إدارة: نائب مدير المركز لريادة الأعمال\nالمسؤول: د. حسن علي السقاف")
                user_state[sender_number] = 'admin_menu'
            else:
                msg.body("❌ الرقم السري غير صحيح. حاول مرة أخرى.")
            return Response(str(response), mimetype="application/xml")

        msg.body("❓ يرجى اختيار أحد الأرقام من القائمة.")
        return Response(str(response), mimetype="application/xml")

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
