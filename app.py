@app.route("/whatsup", methods=['POST'])
def simple_test():
    from twilio.twiml.messaging_response import MessagingResponse
    response = MessagingResponse()
    response.message("✅ البوت يعمل الآن!")
    return str(response)
