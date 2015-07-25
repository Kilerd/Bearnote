# -*- coding: utf-8 -*-
from flask.ext.mail import Message
from app.lib.decorator import run_in_async
from app import mail,app

@run_in_async
def mail_send(subject,recipients,sender=app.config['MAIL_USERNAME'],text_body='',html_body=''):

	msg = Message(
		subject = subject,
		recipients = recipients,
		sender = sender
		)
	if text_body == '' and html_body != '':
		msg.html = html_body
	else:
		msg.body = text_body
	with app.app_context():
		mail.send(msg)
