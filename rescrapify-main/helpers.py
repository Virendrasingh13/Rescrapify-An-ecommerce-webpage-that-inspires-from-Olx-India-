import uuid
import time
from django.core.mail import send_mail
from rescrapify import settings
from io import BytesIO
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa


def send_email_token(email, slug):
    try:
        # user = User.objects.filter(slug=slug).first()
        # if user.email == email:
        #     message = f"Click on this link to verify your email\nhttp://127.0.0.1:8000/accounts/verify/{slug}"
        # else:
        link = settings.LINK
        message = f"Click on this link to verify your email\n{link}/accounts/verify/{slug}"
        subject = "Verification Token for RESCRAPIFY"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail(subject, message, email_from, recipient_list)
        return True
        
    except Exception as e:
        print(e)
        return False
    
def generate_unique_hash():    
    random_hash = str(uuid.uuid4().int)[:6]    
    timestamp = str(int(time.time()))    
    unique_hash = f"{random_hash}_{timestamp}"
    return unique_hash

        


def send_Contact_mail(name,email,subject,message,phone_no):
    
    try:
        recipient_email = ['rescrapify.demo.login@gmail.com',email] 
        email_message = f'Name: {name}\nEmail: {email}\nPhone: {phone_no}\nMessage: {message}'

        send_mail(
                subject,
                email_message,
                settings.EMAIL_HOST_USER, 
                recipient_email,  
                fail_silently=False,
                
                # reply_to=[email],  # This will set the reply-to address in the email client
            )
        
        return True
    
    except Exception as e:
        print(e)
        return False
    
    
    
def send_password_email(email,forgot_password_token):
    try:
        message = f"To reset password for {email}, Click on this link\nhttp://127.0.0.1:8000/accounts/forgot_password/{forgot_password_token}"
        subject = f"RESCRAPIFY - Reset password for {email}"
        email_from = settings.EMAIL_HOST_USER
        receipent = [email]
        send_mail(subject, message, email_from, receipent)
        return True
        
    except Exception as e:
        print(e)
        return False
    
    
#for invoice 
def save_pdf(params:dict):
    template = get_template('invoice.html')
    html = template.render(params)
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response)
    file_name = uuid.uuid4()
    
    try:
        with open(str(settings.BASE_DIR)+ f"/static/pdfs/{file_name}.pdf", 'wb+') as output:
            pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), output)
            
            if pdf.err:
                return '', False
    

            return file_name, True
            
    except Exception as e:
        print(e)
        
   