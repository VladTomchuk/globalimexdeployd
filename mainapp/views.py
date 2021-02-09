from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib import messages
from django.urls import reverse

from GlobalImex import settings

# Create your views here.


def index(request):
    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message_phone = request.POST['message-phone']
        message_comment = request.POST['message-comment']
        ctx = {
            'message_name': message_name,
            'message_email': message_email,
            'message_phone': message_phone,
            'message_comment': message_comment,
        }
        text_content = get_template('mail/mail.txt').render(ctx)
        html_content = get_template('mail/contact_us_email.html').render(ctx)
        subject = 'Ззапрос на обратную связь'
        from_email = 'etmglobalimex.web@gmail.com'
        to = 'etmglobalimex.web@gmail.com'
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        messages.success(request, 'Thank you for request!')
        return HttpResponseRedirect (reverse('index')+'#Form')
    else:
        return render(request, 'base/base.html')


def change_language(request):
    response = HttpResponseRedirect('/')
    if request.method == 'POST':
        language = request.POST.get('language')
        if language:
            if language != settings.LANGUAGE_CODE and [lang for lang in settings.LANGUAGES if lang[0] == language]:
                redirect_path = f'/{language}/'
            elif language == settings.LANGUAGE_CODE:
                redirect_path = '/'
            else:
                return response
            from django.utils import translation
            translation.activate(language)
            response = HttpResponseRedirect(redirect_path)
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response