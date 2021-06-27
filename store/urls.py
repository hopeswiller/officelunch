from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [

    path('', views.index, name='index'),

    path('registration/register', views.UserFormView.as_view(), name='register'),
    path('registration/loginView',views.loginView, name='loginView'),

    path('dashboard', views.dashboard, name='dashboard'),
    path('dashboard/order', views.AddOrder, name='order'),
    path('dashboard/editorder/', views.EditOrderPage, name="EditOrderPage"),
    path('dashboard/editorder/edit/<int:id>/', views.EditOrder, name="EditOrder"),
    path('dashboard/feedback',views.FeedbackFormView.as_view(), name="feedback"),
    path('dashboard/logout',views.logoutView, name="logoutView"),

    path('registration/AdminLogin', views.AdminLogin,name='AdminLogin'),
    path('adminsite',views.adminsite, name='adminsite'),
    path('adminsite/add',views.addmeal, name='addmeal'),
    path('adminsite/edit/<int:id>/',views.editmeal, name='editmeal'),
    path('adminsite/delete/<int:id>/',views.deletemeal, name='deletemeal'),
    path('adminsite/download-csv/', views.reportDownload, name='reportDownload'),
    path('adminsite/password_change',views.password_change, name="password_change"),
    path('adminsite/viewfeedbacks', views.viewfeedback, name='viewfeedback'),


]

