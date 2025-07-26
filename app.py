from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import datetime

app = Flask(__name__)

user_states = {}
admin_phone_number = "+966555582182"
admin_password = "5555"
otp_code = "1234"

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').strip()
    sender = request.values.get('From', '')
    response = MessagingResponse()
    msg = response.message()
    current_state = user_states.get(sender, {})

    def reset_state():
        user_states[sender] = {}

    if not current_state:
        msg.body("مرحباً بك في مساعد مركز الابتكار بجامعة الملك عبد العزيز 👋🏻\n"
                 "كيف يمكنني مساعدتك اليوم؟ اختر أحد الخيارات التالية:\n"
                 "1. زائر / مخترع\n"
                 "2. إدارة مركز الابتكار وريادة الأعمال")
        user_states[sender] = {'stage': 'main_menu'}
        return str(response)

    if current_state['stage'] == 'main_menu':
        if incoming_msg == '1':
            msg.body("مرحباً بك! يرجى اختيار أحد الخيارات:\n"
                     "1. تقديم فكرة ابتكارية\n"
                     "2. تتبع حالة الطلب\n"
                     "3. التواصل مع مختص")
            user_states[sender]['stage'] = 'inventor_menu'
        elif incoming_msg == '2':
            if sender == f"whatsapp:{admin_phone_number}":
                msg.body("يرجى إدخال الرقم السري:")
                user_states[sender]['stage'] = 'enter_password'
            else:
                msg.body("هذا الخيار مخصص لإدارة المركز فقط.")
                reset_state()
        else:
            msg.body("يرجى اختيار رقم صحيح (1 أو 2).")
        return str(response)

    if current_state['stage'] == 'enter_password':
        if incoming_msg == admin_password:
            msg.body("يرجى إدخال رمز التحقق (OTP):")
            user_states[sender]['stage'] = 'verify_otp'
        else:
            msg.body("❌ الرقم السري غير صحيح. حاول مرة أخرى.")
        return str(response)

    if current_state['stage'] == 'verify_otp':
        if incoming_msg == otp_code:
            msg.body("✅ تم التحقق بنجاح.\nيرجى اختيار الإدارة:\n"
                     "1. مدير المركز\n"
                     "2. نائب مدير المركز للابتكار\n"
                     "3. نائب مدير المركز لنقل التقنية\n"
                     "4. نائب مدير المركز لتتجير المعرفة\n"
                     "5. نائب مدير المركز لريادة الأعمال")
            user_states[sender]['stage'] = 'select_department'
        else:
            msg.body("❌ رمز التحقق غير صحيح.")
        return str(response)

    if current_state['stage'] == 'select_department':
        department_names = {
            '1': 'مدير المركز',
            '2': 'نائب مدير المركز للابتكار',
            '3': 'نائب مدير المركز لنقل التقنية',
            '4': 'نائب مدير المركز لتتجير المعرفة',
            '5': 'نائب مدير المركز لريادة الأعمال'
        }

        department_managers = {
            '1': 'د. سعود الواصلي',
            '2': 'د. ليلى أحمد باهمام',
            '3': 'شاغر حالياً',
            '4': 'د. رائد إسماعيل فلمبان',
            '5': 'د. حسن علي السقاف'
        }

        if incoming_msg in department_names:
            dep = department_names[incoming_msg]
            manager = department_managers[incoming_msg]
            msg.body(f"مرحباً بك في إدارة {dep} 👋🏻\n"
                     f"المسؤول: {manager}")
            reset_state()
        else:
            msg.body("❌ يرجى اختيار رقم من 1 إلى 5.")
        return str(response)

    if current_state['stage'] == 'inventor_menu':
        if incoming_msg == '1':
            msg.body("📝 يرجى تعبئة نموذج تقديم فكرة عبر الرابط التالي:\n"
                     "https://docs.google.com/forms/d/e/1FAIpQLSe178sNy2ncQOqN4a8-lJFUUIR4hxshBPc7ijQDJs3r_OCKWQ/viewform?usp=header")
            reset_state()
        elif incoming_msg == '2':
            msg.body("🔍 يرجى تزويدنا برقم الطلب لتتبع حالته.")
            reset_state()
        elif incoming_msg == '3':
            msg.body("📞 سيتم تحويلك إلى أحد المختصين قريباً.")
            reset_state()
        else:
            msg.body("❌ يرجى اختيار رقم صحيح من 1 إلى 3.")
        return str(response)

    msg.body("❌ لم أتمكن من فهم الطلب. يرجى إعادة المحاولة.")
    reset_state()
    return str(response)

if __name__ == '__main__':
    app.run(debug=True)
