from flask import Flask
from flask import render_template, request, jsonify
import smtplib
from email.mime.text import MIMEText
import os
import markov
import secrets

EMAIL_NAME = "Secure SMS Transactions"
EMAIL = secrets.EMAIL
PASSWORD = secrets.PASSWORD
CARRIER_GATEWAY = secrets.CARRIER_GATEWAY

app = Flask(__name__)

smtp = smtplib.SMTP_SSL()
smtp.connect("smtp.mail.yahoo.com", 465)
smtp.login(EMAIL, PASSWORD)

#mail = Mail(app)


@app.route("/")
def index():
    return render_template('index.html')
    '''
    print 'hello'
    number = "8173137559"
    print number+CARRIER_GATEWAY
    msg = Message("Hello", sender=EMAIL, recipients=[number+CARRIER_GATEWAY]) 
    print 'b'
    msg.body = "testing"
    msg.html = '<b>HTML</b>'
    print msg.sender
    print msg.recipients
    print app.config
    mail.send(msg)
    return "Hello World!"
    '''

@app.route("/startConvo", methods=["POST"])
def startConvo():
    number = request.form['number']
    print number
    anime = request.form['anime']
    print anime
    character = request.form['character']
    print character

    model = markov.Markov(anime)
    print 'a'
    model.getCharacters()
    print 'b'
    model.getWordsForChar(character)
    print 'c'
    text = model.generate_markov_text()
    print character + ': ' + text

    msg = MIMEText(text)
    msg['Subject'] = anime + ': ' + character

    print 'd'
    print EMAIL
    print number+CARRIER_GATEWAY
    print msg.as_string()
    try:
        smtp.sendmail(EMAIL, number+CARRIER_GATEWAY, msg.as_string())
    except:
        print 'email did not send'

    print 'sent'            

    return render_template('index.html')

if __name__ == "__main__":
    app.run()
