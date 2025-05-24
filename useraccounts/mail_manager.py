import random
from django.core.mail import EmailMultiAlternatives

def genSecurityCode():
    digit_list = ['1','2','3','4','5','6','7','8','9']
    chosen_digits_list = random.choices(digit_list,k=6)
    security_code = ''.join(chosen_digits_list)
    return security_code


def sendSecurityCodeMail(email, security_code, subj):
    mail_from = 'ecc.eagle@gmail.com'
    mail_to = email
    mail_body = "<div><h4>Hello,</h4><p>Hope you are having a great time shopping with Nibedok. This is a security code generated for you. Please use it in due purpose to continue.</p><p>Security Code: "+security_code+"</p><p>We are very glad to have you with Nibedok and wish you a very good day.</p><p>Best Regards,</p><span style='font-weight:bold'>Nibedok Team</span></div>"
    mail = EmailMultiAlternatives(subj,mail_body,mail_from,[mail_to])
    mail.content_subtype = 'html'
    mail.send()