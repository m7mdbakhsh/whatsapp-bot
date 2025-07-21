from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.form.get("Body", "").strip().lower()
    response = MessagingResponse()
    msg = response.message()

    if "تقديم" in incoming_msg:
        msg.body("لتقديم فكرة براءة اختراع، يرجى تعبئة النموذج عبر الرابط التالي:\nhttps://docs.google.com/forms/d/e/1FAIpQLSe178sNy2ncQOqN4a8-lJFUUIR4hxshBPc7ijQDJs3r_OCKWQ/viewform?usp=header")
    elif "التواصل" in incoming_msg:
        msg.body("للتواصل مع مختص:\nالدكتور / سعود الواصلي\nيمكنك الرد بكلمة 'متابعة' في حال وجود استفسار.")
    elif "قانونية" in incoming_msg:
        msg.body("للاستشارات القانونية:\nالأستاذ / محمد بخش")
    elif "متابعة" in incoming_msg:
        msg.body("شكرًا لتواصلك. سيتم متابعة طلبك قريبًا بإذن الله.")
    else:
        msg.body(
            "مرحبًا بك في مساعد الابتكار بجامعة الملك عبد العزيز 👋\n\n"
            "يرجى اختيار أحد الخيارات التالية:\n"
            "• تقديم فكرة ابتكارية\n"
            "• التواصل مع مختص\n"
            "• استشارة قانونية\n"
            "• متابعة الطلب"
        )

    return str(response)

if __name__ == "__main__":
    app.run(debug=True)


