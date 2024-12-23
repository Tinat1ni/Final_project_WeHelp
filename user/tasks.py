from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_post_choice_email(subject, message, recipient_email):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])

@shared_task
def send_welcome_email(user_email, username):
    subject='Welcome To WeHelp!'
    message = (
        f'მოგესალმებით {username}!\nთქვენ უკვე შეგიძლიათ განათავსოთ და აირჩიოთ პოსტები.\n\nპროფილის გვერდზე გამოგიჩნდებათ თქვენი ინფორმაცია,'
        f' თქვენი პოსტები და ასევე პოსტები რომლებიც აირჩიეთ.\n\nპროფილის გვერდზევე გაქვთ თქვენი პოსტების წაშლის და რედაქტირების საშუალება.\n\nიმ შემთხვევაში, თუ თქვენი საჭიროება დაკმაყოფილდა,'
        f' მონიშნეთ პოსტი როგორც დასრულებული.\n\nდასრულებული და დედლაინის ვადას გადაცილებული პოსტები გარკვეული დროის შემდეგ ავტომატურად წაიშლება\n\n'
        f'\nთუ თქვენ აირჩევთ პოსტს, რეგისტრაციისას '
        f'თქვენს მიერ მითითებულ მეილზე მიიღებთ პოსტის ავტორის სახელს და ტელეფონის ნომერს,\n'
        f'რის შემდეგაც თავად დაუკავშირდებით და გაარკვევთ დეტალებს.\n\n'
        f'\nთქვენი განთავსებული პოსტის მოხალისის მიერ არჩევის შემთხვევაში მეილზე მიიღებთ შეტყობინებას.'

    )
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user_email]
    )

