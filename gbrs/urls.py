
from django.contrib import admin
from django.urls import path,include
from system.views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index,name='index'),
    path('search/',search,name='search'),
    path('login/',login_page,name='login_page'),
    path('signup/',signup_page,name='signup_page'),
    path('tickets/',tickets,name='tickets'),
    path('logout/',logout_page,name='logout_page'),
    path('booking/<id>',booking,name='booking'),
    path('account/<id>',account,name='account'),
    path('delete_account/<id>',delete_account,name='delete_account'),
    path('booking/confirm/<id>/',confirm,name='confirm'),
    path('booking/confirmed/<id>',render_pdf_view,name='render_pdf_view'),
    path('reset_password/',auth_views.PasswordResetView.as_view(template_name = "resetpassword.html"),name='reset_password'),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = "resetpasswordsent.html"),name='password_reset_done'),    
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name = "resetpasswordform.html"),name='password_reset_confirm'),
    path('reset_password_success/',auth_views.PasswordResetCompleteView.as_view(template_name = "resetpasswordcomplete.html"),name='password_reset_complete'),     
]
