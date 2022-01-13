from django.urls import path

from . import views

app_name = 'myAccount'

urlpatterns = [
    path('profile/edit', views.ProfileEdit.as_view(), name='edit_profile'),
    path('profile/img_upload', views.profile_image_upload, name='image_upload'),
    path('list', views.UserList.as_view(), name='user_list'),
    path('<int:pk>/detail', views.UserDetail.as_view(), name='user_detail'),
    path('<int:pk>/picture_list', views.UserPictureList.as_view(), name='picture_list'),
    path('follow', views.add_or_del_relationship, name='follow'),
    path('activity_watched', views.ajax_activity_watched, name='activity_watched'),
    path('email/', views.MyEmailView.as_view(), name='email_change'),
    path('password/change/', views.MyPasswordChange.as_view(), name='my_password_change'),
    path('password/reset/', views.MyPasswordReset.as_view(), name='my_password_reset'),
    ]