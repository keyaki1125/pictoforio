from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from .views import AboutSite, TermsOfService, PrivacyPolicy, ContactFormView, ContactResultView

urlpatterns = [
    path('admin/', admin.site.urls),
    # 同じURLでviewをORしてるのでmyAccountを上にする
    path('account/', include('myAccount.urls')),
    path('account/', include('allauth.urls')),
    path('board/', include('board.urls')),
    path('about_site', AboutSite.as_view(), name='about_site'),
    path('terms_of_service', TermsOfService.as_view(), name='terms_of_service'),
    path('privacy_policy', PrivacyPolicy.as_view(), name='privacy_policy'),

    path('contact', ContactFormView.as_view(), name='contact_form'),
    path('contact/result', ContactResultView.as_view(), name='contact_result'),

]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]