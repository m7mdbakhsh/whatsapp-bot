from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import requests
import datetime
import threading
import time

app = Flask(__name__)
user_state = {}
admin_allowed_number = '+966555582182'
admin_password = '5555'
admin_otp = '1234'
admin_codes = {
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
        print(f"✅ رسالة من {sender_number}: {incoming_msg}")

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

        if incoming_msg.lower() == 'الرجوع':
            msg.body("مرحباً بك من جديد 👋🏻\n"
                     "1. زائر / مخترع\n"
                     "2. إدارة مركز الابتكار وريادة الأعمال")
            user_state[sender_number] = 'main_menu'
            return Response(str(response), mimetype="application/xml")

        # القائمة الرئيسية
        if state == 'main_menu':
            if incoming_msg == '1':
                msg.body("🧠 قائمة الزائر / المخترع:\n"
                         "1. تقديم فكرة ابتكارية\n"
                         "2. التواصل مع المختص\n"
                         "3. استشارة قانونية\n"
                         "4. متابعة حالة الطلب\n"
                         "5. فضلاً أرسل سؤالك وسنقوم بمراجعته والرد عليك قريبًا\n"
                         "6. الأسئلة الشائعة\n"
                         "📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
                user_state[sender_number] = 'visitor_menu'
            elif incoming_msg == '2':
                if sender_number != admin_allowed_number:
                    msg.body("🚫 هذا الخيار غير متاح لرقمك.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
                else:
                    msg.body("🔐 الرجاء إدخال كلمة المرور:\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
                    user_state[sender_number] = 'awaiting_password'
            else:
                msg.body("❓ يرجى اختيار 1 أو 2.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            return Response(str(response), mimetype="application/xml")

        if state == 'awaiting_password':
            if incoming_msg == admin_password:
                msg.body("✅ تم التحقق من كلمة المرور.\nيرجى إدخال رمز OTP:\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
                user_state[sender_number] = 'awaiting_otp'
            else:
                msg.body("❌ كلمة المرور غير صحيحة. حاول مرة أخرى.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            return Response(str(response), mimetype="application/xml")

        if state == 'awaiting_otp':
            if incoming_msg == admin_otp:
                msg.body("✅ تم التحقق بنجاح.\nيرجى اختيار الإدارة:\n"
                         "1. مدير المركز\n"
                         "2. نائب مدير المركز للابتكار\n"
                         "3. نائب مدير المركز لنقل التقنية\n"
                         "4. نائب مدير المركز لتتجير المعرفة\n"
                         "5. نائب مدير المركز لريادة الأعمال\n"
                         "📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
                user_state[sender_number] = 'awaiting_admin_selection'
            else:
                msg.body("❌ رمز OTP غير صحيح. حاول مرة أخرى.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            return Response(str(response), mimetype="application/xml")

        if state == 'awaiting_admin_selection':
            if incoming_msg in admin_codes:
                user_state[sender_number] = f'awaiting_admin_pin_{incoming_msg}'
                msg.body("🔐 الرجاء إدخال الرقم السري الخاص بالإدارة:\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            else:
                msg.body("❓ يرجى اختيار رقم من القائمة.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            return Response(str(response), mimetype="application/xml")

        for i in range(1, 6):
            if state == f'awaiting_admin_pin_{i}':
                if incoming_msg == admin_codes[str(i)]:
                    user_state[sender_number] = f'admin_{i}'
                    names = {
                        '1': "د. سعود الواصلي",
                        '2': "د. ليلى أحمد باهمام",
                        '3': "قسم نقل التقنية",
                        '4': "د. رائد إسماعيل فلمبان",
                        '5': "د. حسن علي السقاف"
                    }
                    msg.body(f"👋🏻 أهلاً بك {names[str(i)]}\n\nيرجى اختيار أحد الخيارات التالية:\n1. {get_option_title(i)}\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
                else:
                    msg.body("❌ الرقم السري غير صحيح. حاول مرة أخرى.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
                return Response(str(response), mimetype="application/xml")

        for i in range(1, 6):
            if state == f'admin_{i}':
                if incoming_msg == '1':
                    links = {
                        '1': "📊 رابط إيرادات حقوق الملكية الفكرية:\nhttps://www.notion.so/22b50f86e3428081a375c4df1653ba0e?source=copy_link",
                        '2': "📌 رابط لوحة متابعة المبادرات الابتكارية:\n[يتم إضافته لاحقًا]",
                        '3': "📄 رابط اتفاقيات نقل التقنية:\n[يتم إضافته لاحقًا]",
                        '4': "📈 رابط مؤشرات تتجير المعرفة:\n[يتم إضافته لاحقًا]",
                        '5': "📂 رابط تقارير مشاريع ريادة الأعمال:\n[يتم إضافته لاحقًا]"
                    }
                    msg.body(f"{links[str(i)]}\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
                else:
                    msg.body("❓ يرجى اختيار رقم من القائمة.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
                return Response(str(response), mimetype="application/xml")

        if state == 'visitor_menu':
            if incoming_msg == '1':
                msg.body("🔗 لتقديم فكرة ابتكارية:\nhttps://docs.google.com/forms/d/e/1FAIpQLScPzx7FdVVLezLoUFxz8VWs0NWgMJc_0X6r5zFot9eehtcPLg/viewform?usp=sharing&ouid=111866442441515982808\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            elif incoming_msg == '2':
                msg.body("📞 سيتم تحويلك إلى المختص: د. سعود الواصلي.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            elif incoming_msg == '3':
                msg.body("⚖️ سيتم التواصل مع: أ. محمد بخش (الاستشارات القانونية).\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            elif incoming_msg == '4':
                msg.body("📋 الرجاء تزويدنا برقم الطلب أو الاسم الثلاثي.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            elif incoming_msg == '5':
                msg.body("🔗 يمكنك إرسال سؤالك عبر النموذج التالي:\nhttps://docs.google.com/forms/d/e/1FAIpQLScPzx7FdVVLezLoUFxz8VWs0NWgMJc_0X6r5zFot9eehtcPLg/viewform?usp=header\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            elif incoming_msg == '6':
                msg.body("📚 الأسئلة الشائعة:\n\n- كيف يمكنني حماية فكرتي؟\n- ما الفرق بين براءة الاختراع وحقوق المؤلف؟\n- كيف أتابع حالة طلبي؟\n- متى يمكنني تسويق فكرتي؟\n\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            else:
                msg.body("❓ يرجى اختيار رقم من القائمة.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
            return Response(str(response), mimetype="application/xml")

        msg.body("❓ يرجى اختيار أحد الأرقام من القائمة.\n📩 للانتقال إلى القائمة الرئيسية، اكتب: الرجوع")
        return Response(str(response), mimetype="application/xml")

    except Exception as e:
        print(f"❌ خطأ: {e}")
        return "❌ خطأ في الخادم", 500

def get_option_title(index):
    return {
        1: "إيرادات حقوق الملكية الفكرية",
        2: "لوحة متابعة المبادرات الابتكارية",
        3: "قائمة اتفاقيات نقل التقنية",
        4: "مؤشرات تتجير المعرفة",
        5: "تقارير مشاريع ريادة الأعمال"
    }.get(index, "خيار غير معروف")

def keep_alive():
    while True:
        try:
            print("🔁 Ping...")
            requests.get('https://whatsapp-bot-bx3b.onrender.com/ping')
            print("✅ Ping OK")
        except Exception as e:
            print("❌ Ping Failed:", e)
        time.sleep(300)

if __name__ == '__main__':
    threading.Thread(target=keep_alive).start()
    app.run()
