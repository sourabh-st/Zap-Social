from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.views.generic.base import RedirectView
from django.conf.urls.static import static
from zapsocial import settings


urlpatterns = [
    path('admin/', admin.site.urls),

    path('social/', include('social.urls')),
    path('',RedirectView.as_view(url='social/'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
