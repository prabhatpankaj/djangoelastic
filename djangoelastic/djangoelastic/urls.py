from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from publisher.views import view_post
from main.views import verify

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r'^(?P<slug>[a-zA-Z0-9\-]+)', view_post, name='view_post'),
    url(r'^verify/(?P<uuid>[a-z0-9\-]+)/', verify, name='verify'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
