from bottle import route, run, request, template, Bottle, static_file
from azure.cognitiveservices.language.textanalytics import TextAnalyticsClient
from msrest.authentication import CognitiveServicesCredentials

subscription_key = "" ###ENTER IN KEY
credentials = CognitiveServicesCredentials(subscription_key)
text_analytics_url = "https://southcentralus.api.cognitive.microsoft.com/"
text_analytics = TextAnalyticsClient(endpoint=text_analytics_url, credentials=credentials)

def getSentiment(message):
    req = [{"id": "1","language": "en","text": message}]
    sentimentVal = text_analytics.sentiment(documents=req)
    response = sentimentVal.documents[0].score
    #for document in response.documents:
    #    print("Document Id: ", document.id, ", Sentiment Score: ",
    #          "{:.2f}".format(document.score))
    return response


def getImage(score):
    if score > 0.8:
        img = "10-8.jpg"
    elif score < 0.8 and score > 0.6:
        img = "6-8.jpg"
    elif score < 0.6 and score > 0.5:
        img = "5-6.jpg"
    elif score < 0.5 and score > 0.4:
        img = "4-5.jpg"
    elif score < 0.4 and score > 0.2:
        img = "2-4.jpg"
    elif score < 0.2:
        img =  "0-2.jpg"
    else:
        img = "6-8.jpg"
    return img

@route('/test')
def hello():
    #template("form.tpl", message="Please enter your name")
    return "Hello World!"

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static')

@route('/')
def index():
    """Home Page"""

    return template("form.tpl", message="Trumpify your message.")

@route('/', method="POST")
def formhandler():
    """Handle the form submission"""
    message = request.forms.get('message')
    #message = request.forms.get('message')
    returnmessage = getSentiment(message)
    trumpimg = getImage(returnmessage)
    fulltrumpimg = "http://13.84.178.85/static/" + trumpimg  ####Change the IP or the hostname to match host name OR add variable for hostname to auto populate
    #message = "message was: " + formInput + "sentiment: " + sentiement
    return template("return.tpl", message=fulltrumpimg)

run(host='0.0.0.0', port=80, debug=False)
