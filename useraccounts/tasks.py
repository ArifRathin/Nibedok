from celery import shared_task
from .mail_manager import sendSecurityCodeMail
@shared_task
def mailer(email, security_code, subj):
    sendSecurityCodeMail(email=email,security_code=security_code,subj=subj)