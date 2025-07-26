from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# بيانات الدخول للمختص
admin_phone = "+966555582182"
admin_password = "5555"

# حالة كل مستخدم
user_states = {}

# واجهة البوت الأساسية
@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").strip()
    from_number = request.values.get("From", "").strip()

    resp = MessagingResponse()
    msg = resp.message()

    state = user_states.get(from_number, {"step": "start"})

    if state["step"] == "start":
        user_states[from_number] = {"step": "awaiting_choice"}
        msg.body("مرحباً بك في مساعد مركز الابتكار بجامعة الملك عبد العزيز 👋🏻\n"
                 "كيف يمكنني مساعدتك اليوم؟\n"
                 "اختر أحد الخيارات التالية:\n"
                 "1. زائر / مخترع\n"
                 "2. إدارة مركز الابتكار وريادة الأعمال")
        return str(resp)

    # خيار الزائر
    if state["step"] == "awaiting_choice" and incoming_msg == "1":
        msg.body("رائع! كيف يمكننا خدمتك؟\n"
                 "1. تقديم فكرة ابتكارية\n"
                 "2. متابعة طلب سابق\n"
                 "3. التواصل مع الدعم")
        user_states[from_number]["step"] = "visitor_options"
        return str(resp)

    # رابط تقديم فكرة
    if state["step"] == "visitor_options" and incoming_msg == "1":
        msg.body("يمكنك تقديم فكرتك عبر النموذج التالي:\n"
                 "https://docs.google.com/forms/d/e/1FAIpQLSe178sNy2ncQOqN4a8-lJFUUIR4hxshBPc7ijQDJs3r_OCKWQ/viewform?usp=header")
        user_states[from_number]["step"] = "done"
        return str(resp)

    # خيار المختص
    if state["step"] == "awaiting_choice" and incoming_msg == "2":
        if from_number != admin_phone:
            msg.body("⚠️ هذا الخيار مخصص لإدارة مركز الابتكار فقط.")
            return str(resp)
        else:
            msg.body("الرجاء إدخال الرقم السري:")
            user_states[from_number] = {"step": "awaiting_password"}
            return str(resp)

    # التحقق من الرقم السري
    if state["step"] == "awaiting_password":
        if incoming_msg == admin_password:
            msg.body("✅ تم التحقق بنجاح.\nالرجاء إدخال رمز التحقق (OTP):")
            user_states[from_number] = {"step": "awaiting_otp"}
        else:
            msg.body("❌ الرقم السري غير صحيح. حاول مرة أخرى.")
        return str(resp)

    # التحقق من OTP
    if state["step"] == "awaiting_otp":
        if incoming_msg == "0000":  # مؤقتاً نستخدم OTP ثابت للتجربة
            msg.body("أهلاً بك، يرجى اختيار الإدارة:\n"
                     "1. إدارة الابتكار\n"
                     "2. إدارة نقل التقنية\n"
                     "3. إدارة تتجير المعرفة\n"
                     "4. إدارة ريادة الأعمال\n"
                     "5. إدارة الخدمات المساندة")
            user_states[from_number] = {"step": "admin_menu"}
        else:
            msg.body("❌ رمز التحقق غير صحيح.")
        return str(resp)

    if state["step"] == "admin_menu":
        departments = {
            "1": "م. محمد - مدير إدارة الابتكار",
            "2": "م. أحمد - مدير إدارة نقل التقنية",
            "3": "أ. نورة - مديرة إدارة تتجير المعرفة",
            "4": "د. عبدالله - مدير إدارة ريادة الأعمال",
            "5": "أ. سارة - مديرة إدارة الخدمات المساندة"
        }
        if incoming_msg in departments:
            msg.body(f"✅ تم اختيار الإدارة:\n{departments[incoming_msg]}")
            user_states[from_number]["step"] = "done"
        else:
            msg.body("❌ خيار غير صحيح. الرجاء اختيار رقم من 1 إلى 5.")
        return str(resp)

    msg.body("يرجى إرسال 'مرحبا' للبدء من جديد.")
    user_states[from_number] = {"step": "start"}
    return str(resp)

# مسار ping لفحص عمل البوت
@app.route("/ping", methods=["GET"])
def ping():
    return "Bot is alive", 200

if __name__ == "__main__":
    app.run()
