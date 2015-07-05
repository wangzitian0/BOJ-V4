from django.core.mail  import  send_mail

title="This is mail title."
message='Hello! This is a message!'
sender='wangzitian0@bupt.edu.cn'
mail_list=['wangzitian0@bupt.edu.cn',]
send_mail(
    subject=title,  
    message=message,  
    from_email=sender,
    recipient_list=mail_list,  
    fail_silently=False,
) 

