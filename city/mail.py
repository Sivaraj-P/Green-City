from email.message import EmailMessage
import ssl
import smtplib
email_sender='' #enter the email id
email_password='' #enter the app password 


def mail(email_reciever,sub,body):
    em=EmailMessage()
    em['from']=email_sender
    em['to']=email_reciever
    em['subject']=sub
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_reciever,em.as_string())

