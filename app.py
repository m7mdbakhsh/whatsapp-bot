from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
from datetime import datetime

app = Flask(__name__)

# رابط Google Script لتخزين البيانات في Google Sheets
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbzWJBvR1h8mu0EP8kp4_t8xEBa6fOcVefHHbjpg5sSd92KSN8zgHqjxiEL7NpLeygET/exec'

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    phone = from_number.replace('whatsapp:', '')

    # تحديد نوع الطلب حسب الرسالة
    if incoming_msg in ['1', 'مرحلة الفكرة']:
        req_type = 'تقديم فكرة'
    elif incoming_msg in ['2', 'طلب استشارة']:
        req_type = 'طلب استشارة'
    elif incoming_msg in ['3', 'مساعدة في النموذج']:
        req_type = 'مساعدة في النموذج'
    elif incoming_msg in ['4', 'عرض براءة']:
        req_type = 'عرض براءة'
    elif incoming_msg in ['5', 'أفضل 10 ساعات']:
        req_type = 'أفضل 10 ساعات'
    else:
        req_type = 'غير محدد'

    # تجهيز البيانات للإرسال إلى Google Sheets
    data = {
        'phone': phone,
        'message': incoming_msg,
        'type': req_type
    }

    # إرسال البيانات إلى Google Script
    try:
        response = requests.post(GOOGLE_SCRIPT_URL, json=data)
        print("تم الإرسال إلى Google Sheet:", response.text)
    except Exception as e:
        print("خطأ في الإرسال:", str(e))

    # رد واتساب
    reply = MessagingResponse()
    msg = reply.message()
    msg.body(f"✅ تم تسجيل طلبك بنجاح:\n\n📱 الرقم: {phone}\n📩 الرسالة: {incoming_msg}\n📂 النوع: {req_type}")
    return str(reply)

if __name__ == '__main__':
    app.run(debug=True)
