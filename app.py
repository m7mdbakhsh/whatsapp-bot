from flask import Flask, request, Response
from twilio.twiml.messaging_response import MessagingResponse
import requests
import datetime
import threading
import time
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)
user_state = {}
admin_allowed_numbers = ['+966555582182', '+966540648189']
admin_password = '5555'
admin_otp = '1234'
admin_codes = {
    '1': '1111',
    '2': '2222',
    '3': '3333',
    '4': '4444',
    '5': '5555'
}

# إعداد Google Sheets API
SPREADSHEET_ID = "1615-Km7g7xjDLNHEqgPCoJubNNV6I8rVjaH5n9-GlcA"
RANGE_NAME = "Sheet1!A2:E"  # عدل حسب ورقة العمل ونطاق البيانات

# تحميل بيانات الاعتماد من متغير البيئة
SERVICE_ACCOUNT_INFO = json.loads(os.environ.get('GOOGLE_CREDENTIALS'))
credentials = service_account.Credentials.from_service_account_info(
    SERVICE_ACCOUNT_INFO,
    scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]
)
service = build('sheets', 'v4', credentials=credentials)
sheet = service.spreadsheets()

def clean_number(num):
    # إزالة أي رموز غير الأرقام من رقم الجوال
    return ''.join(filter(str.isdigit, num))

def get_status_by_phone(phone):
    try:
        cleaned_phone = clean_number(phone)
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
        values = result.get('values', [])
        for row in values:
            if len(row) >= 5:
                row_phone_clean = clean_number(row[0])
                if row_phone_clean == cleaned_phone:
                    # صياغة رسالة بجميع بيانات الصف حسب الأعمدة B، C، D، E
                    return (f"📋 بيانات طلبك:\n"
                            f"رقم الطلب: {row[1]}\n"
                            f"اسم المخترع: {row[2]}\n"
                            f"حالة الطلب: {row[3]}\n"
                            f"ملاحظات: {row[4]}")
    except Exception as e:
        print(f"❌ خطأ في جلب بيانات Google Sheets: {e}")
    return None

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

        if incoming_msg == '0':
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
                         "للقائمة الرئيسية، اكتب: 0")
                user_state[sender_number] = 'visitor_menu'
            elif incoming_msg == '2':
                if sender_number not in admin_allowed_numbers:
                    msg.body("🚫 هذا الخيار غير متاح لرقمك.\nللقائمة الرئيسية، اكتب: 0")
                else:
                    if sender_number == '+966555582182':
                        msg.body("مرحباً بك، محمد بخش ✅\n🔐 الرجاء إدخال كلمة المرور:\nللقائمة الرئيسية، اكتب: 0")
                    elif sender_number == '+966540648189':
                        msg.body("مرحباً بك، د.سعود الواصلي ✅\n🔐 الرجاء إدخال كلمة المرور:\nللقائمة الرئيسية، اكتب: 0")
                    else:
                        msg.body("مرحباً بك، تم التعرف على رقمك كمستخدم إداري ✅\n🔐 الرجاء إدخال كلمة المرور:\nللقائمة الرئيسية، اكتب: 0")
                    user_state[sender_number] = 'awaiting_password'
            else:
                msg.body("❓ يرجى اختيار 1 أو 2.\nللقائمة الرئيسية، اكتب: 0")
            return Response(str(response), mimetype="application/xml")

        if state == 'awaiting_password':
            if incoming_msg == admin_password:
                msg.body("✅ تم التحقق من كلمة المرور.\nيرجى إدخال رمز OTP:\nللقائمة الرئيسية، اكتب: 0")
                user_state[sender_number] = 'awaiting_otp'
            else:
                msg.body("❌ كلمة المرور غير صحيحة. حاول مرة أخرى.\nللقائمة الرئيسية، اكتب: 0")
            return Response(str(response), mimetype="application/xml")

        if state == 'awaiting_otp':
            if incoming_msg == admin_otp:
                msg.body("✅ تم التحقق بنجاح.\nيرجى اختيار الإدارة:\n"
                         "1. مدير المركز\n"
                         "2. نائب مدير المركز للابتكار\n"
                         "3. نائب مدير المركز لنقل التقنية\n"
                         "4. نائب مدير المركز لتتجير المعرفة\n"
                         "5. نائب مدير المركز لريادة الأعمال\n"
                         "للقائمة الرئيسية، اكتب: 0")
                user_state[sender_number] = 'awaiting_admin_selection'
            else:
                msg.body("❌ رمز OTP غير صحيح. حاول مرة أخرى.\nللقائمة الرئيسية، اكتب: 0")
            return Response(str(response), mimetype="application/xml")

        if state == 'awaiting_admin_selection':
            if incoming_msg in admin_codes:
                user_state[sender_number] = f'awaiting_admin_pin_{incoming_msg}'
                msg.body("🔐 الرجاء إدخال الرقم السري الخاص بالإدارة:\nللقائمة الرئيسية، اكتب: 0")
            else:
                msg.body("❓ يرجى اختيار رقم من القائمة.\nللقائمة الرئيسية، اكتب: 0")
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
                    msg.body(f"👋🏻 أهلاً بك {names[str(i)]}\n\nيرجى اختيار أحد الخيارات التالية:\n1. {get_option_title(i)}\nللقائمة الرئيسية، اكتب: 0")
                else:
                    msg.body("❌ الرقم السري غير صحيح. حاول مرة أخرى.\nللقائمة الرئيسية، اكتب: 0")
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
                    msg.body(f"{links[str(i)]}\nللقائمة الرئيسية، اكتب: 0")
                else:
                    msg.body("❓ يرجى اختيار رقم من القائمة.\nللقائمة الرئيسية، اكتب: 0")
                return Response(str(response), mimetype="application/xml")

        if state == 'visitor_menu':
            if incoming_msg == '1':
                msg.body("🔗 لتقديم فكرة ابتكارية:\nhttps://docs.google.com/forms/d/e/1FAIpQLScPzx7FdVVLezLoUFxz8VWs0NWgMJc_0X6r5zFot9eehtcPLg/viewform?usp=sharing&ouid=111866442441515982808\nللقائمة الرئيسية، اكتب: 0")
            elif incoming_msg == '2':
                msg.body("📞 سيتم تحويلك إلى المختص: د. سعود الواصلي.\nللقائمة الرئيسية، اكتب: 0")
            elif incoming_msg == '3':
                msg.body("⚖️ سيتم التواصل مع: أ. محمد بخش (الاستشارات القانونية).\nللقائمة الرئيسية، اكتب: 0")
            elif incoming_msg == '4':
                status = get_status_by_phone(sender_number)
                if status:
                    msg.body(f"{status}\nللقائمة الرئيسية، اكتب: 0")
                else:
                    msg.body("❌ عذرًا، لم نعثر على حالة طلب مرتبطة برقم جوالك.\nللقائمة الرئيسية، اكتب: 0")
            elif incoming_msg == '5':
                msg.body("🔗 يمكنك إرسال سؤالك عبر النموذج التالي:\nhttps://docs.google.com/forms/d/e/1FAIpQLScPzx7FdVVLezLoUFxz8VWs0NWgMJc_0X6r5zFot9eehtcPLg/viewform?usp=header\nللقائمة الرئيسية، اكتب: 0")
            elif incoming_msg == '6':
                msg.body("📚 الأسئلة الشائعة:\n\n- كيف يمكنني حماية فكرتي؟\n- ما الفرق بين براءة الاختراع وحقوق المؤلف؟\n- كيف أتابع حالة طلبي؟\n- متى يمكنني تسويق فكرتي؟\n\nللقائمة الرئيسية، اكتب: 0")
            else:
                msg.body("❓ يرجى اختيار رقم من القائمة.\nللقائمة الرئيسية، اكتب: 0")
            return Response(str(response), mimetype="application/xml")

        msg.body("❓ يرجى اختيار أحد الأرقام من القائمة.\nللقائمة الرئيسية، اكتب: 0")
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
