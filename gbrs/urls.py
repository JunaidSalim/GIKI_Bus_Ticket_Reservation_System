
from django.contrib import admin
from django.urls import path,include
from system.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('',home,name='home'),
    path('',index,name='index'),
    path('temp/',temp,name='temp'),
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
]
