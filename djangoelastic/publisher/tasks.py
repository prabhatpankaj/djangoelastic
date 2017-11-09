from django.template import Template, Context
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from djangoelastic.celery import app
from publisher.models import Post
from django.conf import settings

from_email = settings.DEFAULT_EMAIL_USER 
 
REPORT_TEMPLATE = 'postcount.html'
 
 
@app.task
def send_view_count_report():
    for user in get_user_model().objects.all():
        posts = Post.objects.filter(author=user)
        if not posts:
            continue
 
        template = Template(REPORT_TEMPLATE)
 
        send_mail(
            'Your QuickPublisher Activity',
            template.render(context=Context({'posts': posts})),
            from_email,
            [user.email],
            fail_silently=False,
        )