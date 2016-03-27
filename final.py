import imaplib2
import os
import email
from email.mime.text import MIMEText
import smtplib
import time

import markov
import secrets


EMAIL_NAME = "Secure SMS Transactions"
EMAIL = secrets.EMAIL
PASSWORD = secrets.PASSWORD
CARRIER_GATEWAY = secrets.CARRIER_GATEWAY

smtp = smtplib.SMTP_SSL()
smtp.connect("smtp.mail.yahoo.com", 465)
smtp.login(EMAIL, PASSWORD)

imap = imaplib2.IMAP4_SSL('imap.mail.yahoo.com', 993)
imap.login(EMAIL, PASSWORD)


while True:
	numMsgs = imap.select("inbox")
	print numMsgs
	if numMsgs[0] != '0':

		rv, data = imap.search(None, "(UNSEEN)")

		if rv == 'OK':
			for num in data[0].split():
				rv, data = imap.fetch(num, '(RFC822)')
				msg = email.message_from_string(data[0][1])
				msg = msg.as_string()

				sender = None
				subject = None
				body = None

				msg = msg.split()
				#for j in msg:
				#	print j
				for i in range(len(msg)):
					if msg[i].strip() == 'From:':
						sender = msg[i+1]
						sender = sender[0:len(sender)]
						print 'sender asdf'
						print sender
					if  msg[i].strip() == 'Content-Length:':
						i += 2
						startMsg = i
						try:
							while msg[i+1] != '-----Original':
								i += 1
						except:
							pass
						body = ' '.join(msg[startMsg:i+1])
						print 'body asdf'
						print body
					if msg[i].strip() == 'Subject:':
						startSubject = i+1
						i = startSubject + 1
						subject = ' '.join(msg[startSubject:i+1])
						print 'subject asdf'
						print subject

				anime = subject.split(': ')[0]
				character = subject.split(': ')[1]


				model = markov.Markov(anime)
				model.getCharacters()
				model.getWordsForChar(character)
				print 
				text = model.generate_markov_text(size=len(body))
				print character + ': ' + text

				msg = MIMEText(text)
				msg['Subject'] = subject

				smtp.sendmail(EMAIL, sender, msg.as_string())	

				print 'sent'			


	time.sleep(5)
	print 'running'




