
from django.urls import path
from . import views
from myapp.views import UserSignupView,LoginView,HomeView,ProfileView
from  myapp.views import ForgetPasswordView,AddCitizen,VehicleRegistrationView,SeeVehicles,EsewaRequestView,EsewaVerifyView


app_name="myapp"

urlpatterns = [
path("",HomeView.as_view(),name="home"),
path("signup/",UserSignupView.as_view(),name="signup"),
path("accounts/login/",LoginView.as_view(),name="login"),
path("dashboard/",ProfileView.as_view(),name="dashboard"),
path("forgetpw/",ForgetPasswordView.as_view(),name="forgetpw"),
path("changepw/",views.password_change_view,name="changepw"),
path('signout/',views.signout,name="signout"),
path('about/',views.about,name="about"),
path('contact/',views.contact,name="contact"),
path('gallery/',views.gallery,name="gallery"),
path('contact/',views.contact,name="contact"),
path('addcitizen/<int:pk>/',AddCitizen.as_view(),name="addcitizen"),
path('ajax/load-muni/', views.load_muni, name='ajax_load_muni'),
path('vehicle-registration/',VehicleRegistrationView.as_view(),name="vehicleregistration"),
path('vehicle-info/',SeeVehicles.as_view(),name="seevehicle"),
path('esewapayment/<int:vid>/',EsewaRequestView.as_view(),name="esewapayment"),
path('epay-verify',EsewaVerifyView.as_view(),name="epayverify"),
path('fintecherror',views.fintecherror,name="fintecherror"),










]