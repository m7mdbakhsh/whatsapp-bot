from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import requests
import datetime
import threading
import time

app = Flask(__name__)
user_state = {}

@app.route('/ping')
def ping():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"✅ Ping received at {now}")
    return f"✅ I'm awake! {now}"

@app.route('/bakhsh', methods=['POST'])
def whatsapp_reply():
    try:
        incoming_msg = request.values.get('Body', '').strip().lower()
        sender_number = request.values.get('From', '').replace('whatsapp:', '')
        print(f"✅ تم استلام رسالة من واتساب من الرقم {sender_number}: {incoming_msg}")

        response = MessagingResponse()
        msg = response.message()

        state = user_state.get(sender_number, {"step": "start", "otp": None, "verified": False, "admin": False})

        # جملة الرجوع
        back_text = "\n\n🔙 لكتابة 'رجوع' للعودة إلى القائمة السابقة."

        # بداية المحادثة
        if incoming_msg in ['مرحبا', 'السلام عليكم', 'hi', 'hello', 'ابدأ', 'start']:
            user_state[sender_number] = {"step": "main", "otp": None, "verified": False, "admin": False}
            msg.body("مرحباً بك في مساعد مركز الابتكار بجامعة الملك عبد العزيز 👋🏻\nكيف يمكنني مساعدتك اليوم؟\n1. زائر / مخترع\n2. إدارة مركز الابتكار وريادة الأعمال" + back_text)
            return str(response)

        # العودة للقائمة الرئيسية
        if incoming_msg == 'رجوع':
            user_state[sender_number] = {"step": "main", "otp": None, "verified": False, "admin": False}
            msg.body("تمت إعادتك إلى القائمة الرئيسية:\n1. زائر / مخترع\n2. إدارة مركز الابتكار وريادة الأعمال" + back_text)
            return str(response)

        # الخطوة الرئيسية
        if state["step"] == "main":
            if incoming_msg == '1':
                msg.body("يرجى اختيار أحد الخدمات:\n1. إيرادات حقوق الملكية الفكرية" + back_text)
                state["step"] = "visitor_menu"

            elif incoming_msg == '2':
                if sender_number == '+966555582182':
                    msg.body("يرجى إدخال الرقم السري للدخول:" + back_text)
                    state["step"] = "admin_password"
                else:
                    msg.body("❌ هذا الرقم غير مصرح له بالدخول." + back_text)
            else:
                msg.body("❌ يرجى اختيار 1 أو 2 فقط." + back_text)

        elif state["step"] == "visitor_menu":
            if incoming_msg == '1':
                msg.body("🔗 رابط تقديم إيرادات حقوق الملكية الفكرية:\nhttps://docs.google.com/forms/d/e/1FAIpQLSe178sNy2ncQOqN4a8-lJFUUIR4hxshBPc7ijQDJs3r_OCKWQ/viewform?usp=header" + back_text)
            else:
                msg.body("❌ خيار غير صحيح، يرجى اختيار رقم من القائمة." + back_text)

        elif state["step"] == "admin_password":
            if incoming_msg == '5555':
                otp = '1234'
                state["otp"] = otp
                state["step"] = "admin_otp"
                msg.body(f"✅ تم التحقق بنجاح.\nيرجى إدخال رمز التحقق OTP: {otp}" + back_text)
            else:
                msg.body("❌ الرقم السري غير صحيح." + back_text)

        elif state["step"] == "admin_otp":
            if incoming_msg == state["otp"]:
                state["verified"] = True
                state["step"] = "choose_department"
                msg.body("✅ تم التحقق بنجاح.\nيرجى اختيار الإدارة:\n1. إدارة الابتكار\n2. إدارة نقل التقنية\n3. إدارة تتجير المعرفة\n4. إدارة ريادة الأعمال\n5. مدير المركز" + back_text)
            else:
                msg.body("❌ رمز التحقق غير صحيح." + back_text)

        elif state["step"] == "choose_department":
            departments = {
                '1': ("إدارة الابتكار", "1111", "أ. سارة القرني"),
                '2': ("إدارة نقل التقنية", "2222", "م. فهد الثقفي"),
                '3': ("إدارة تتجير المعرفة", "3333", "أ. روان جمال"),
                '4': ("إدارة ريادة الأعمال", "4444", "أ. أحمد الغامدي"),
                '5': ("مدير المركز", "5555", "د. محمد بخش")
            }
            if incoming_msg in departments:
                dep_name, dep_code, dep_head = departments[incoming_msg]
                state["department"] = dep_name
                state["expected_code"] = dep_code
                state["step"] = "department_password"
                msg.body(f"🔐 تم اختيار {dep_name}.\nيرجى إدخال الرقم السري الخاص بهذه الإدارة." + back_text)
            else:
                msg.body("❌ يرجى اختيار رقم إدارة صحيح." + back_text)

        elif state["step"] == "department_password":
            if incoming_msg == state.get("expected_code"):
                dep_name = state.get("department", "الإدارة")
                dep_head = {
                    "إدارة الابتكار": "أ. سارة القرني",
                    "إدارة نقل التقنية": "م. فهد الثقفي",
                    "إدارة تتجير المعرفة": "أ. روان جمال",
                    "إدارة ريادة الأعمال": "أ. أحمد الغامدي",
                    "مدير المركز": "د. محمد بخش"
                }.get(dep_name, "المسؤول غير معروف")
                msg.body(f"✅ تم الدخول إلى {dep_name}.\nاسم المسؤول: {dep_head}" + back_text)
                state["step"] = "main"  # يرجع للخطوة الرئيسية بعد الدخول
            else:
                msg.body("❌ الرقم السري للإدارة غير صحيح." + back_text)

        user_state[sender_number] = state
        return str(response)

    except Exception as e:
        print(f"❌ حدث خطأ: {e}")
        return str(e)

def keep_alive():
    def run():
        while True:
            try:
                requests.get("https://your-deployed-url.com/ping")
            except:
                pass
            time.sleep(300)
    thread = threading.Thread(target=run)
    thread.start()

if __name__ == '__main__':
    keep_alive()
    app.run()
