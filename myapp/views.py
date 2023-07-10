from base64 import urlsafe_b64encode
from typing import Any, Dict
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import login,logout,authenticate
from django.views.generic import CreateView,FormView,TemplateView,UpdateView
from .models import CustomUser,Citizen,Municipality,District,RegisteredVehicle
from .forms import CitizenRegistrationForm,CitizenLoginForm,ForgetPasswordForm,ChangePasswordForm,ResetPasswordForm
import os
from django.utils import timezone

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.encoding import force_str,force_bytes,DjangoUnicodeDecodeError
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from .utils import Util


class HomeView(TemplateView):
    template_name="home.html"
    image_dir = os.path.join(os.path.dirname(__file__), '/VRS/static/dotm_slideshow')
    images = os.listdir(image_dir)
    image_urls = [os.path.join('static\dotm_slideshow', image) for image in images]
    def get_context_data(self, **kwargs):

        context= super().get_context_data(**kwargs)
        context["slides"]=self.image_urls
        print(self.image_urls)
        return context


class UserSignupView(FormView):
    form_class=CitizenRegistrationForm
    template_name='signup.html'   
    success_url=reverse_lazy('myapp:login')



    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["login"]=self.form_class
        context["purpose"]="Signup"


        


        return context

    def form_valid(self,form):
        email=form.cleaned_data.get("email")
        password=form.cleaned_data.get("password")
        full_name=form.cleaned_data.get("full_name")
        user=CustomUser.objects.create_user(email,password)
        form.instance.user=user
        login(self.request,user)
        citizen=Citizen(user=user,full_name=full_name,joined_on=timezone.now())
        citizen.save()

        
        


        return super().form_valid(form)
    
class LoginView(FormView):
    template_name="signup.html"
    form_class=CitizenLoginForm
    success_url=reverse_lazy('myapp:home')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context["signup"]=self.form_class
        context["purpose"]="Login"


        return context
    
    def form_valid(self,form):
        email=form.cleaned_data.get("email")
        password=form.cleaned_data.get("password")
        user=authenticate(email=email,password=password)
        if user is not None :
            login(self.request,user)
            print("logedin")
        else:
            messages.error(self.request,'Invalid Credentials')
        return redirect('myapp:login')
        
    


class ProfileView(TemplateView):
    template_name ="dashboard.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user=self.request.user
        context["user"]=user
        citizen=Citizen.objects.get(id=user.citizen.id)
        context["citizen"]=citizen
                
        return context


class ForgetPasswordView(FormView):
    template_name="forgetpassword.html"
    form_class=ForgetPasswordForm
    success_url="/forget-password/?sent=yes"


    def form_valid(self,form):
        email=form.cleaned_data.get("email")
        

        user=CustomUser.objects.get(email=email)
       
        
        uid=urlsafe_b64encode(force_bytes(user.id))
        token=PasswordResetTokenGenerator().make_token(user)
        link='http://localhost:8000/resetpassword/'+uid+'/'+token+"/"
        body="Click the link to reset your password"
        data={
                'subject':'Reset your password' ,
                'body' :link,
                'to_email':user.email
                
            }
        Util.send_mail(data)

    


        
        

        return super().form_valid(form)
    

class ResetPasswordView(FormView):
    template_name="passwordreset.html"
    form_class=ResetPasswordForm
    success_url="/login/"

    def form_valid(self, form):
        useridparam=self.kwargs.get("uid") ## getting from link
 ##decoding
        # userid = force_str(urlsafe_base64_decode(useridparam))
        # user=CustomUser.objects.get(id=userid)
        
        token=self.kwargs.get("token")
        
     ###3/////////////////////////////////////////////////
        ##### YAHA BUG XA MALAI FIX GARNA AAYENA

        #////////////////////////////////////////


        # if user is not None: ## and PasswordResetTokenGenerator.check_token(user,token):
        #     password=form.cleaned_data.get("new_password")
        #     user.set_password(password)
        #     user.save()



        return super().form_valid(form)
    
class ChangePasswordView(FormView):
    template_name="passwordchange.html"
    form_class=ChangePasswordForm
    success_url="/login"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)

        return context

def signout(request):
    logout(request)
    return redirect('myapp:home')


from django.shortcuts import render
def about(request):
    return render(request,"about.html")

def contact(request):
    return render(request,"contact.html")

def gallery(request):
    return render(request,"gallery.html")

def contact(request):
    return render(request,"contact.html")


class AddCitizen(UpdateView):
    model=Citizen
    fields=["full_name","nin_no","district","local_body","ward_no","phone","identification","photo"]
    template_name='citizen.html'
    success_url=reverse_lazy('myapp:home')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)        
        user_id = self.kwargs.get('cid')
        return context


def load_muni(request):
    district_id = request.GET.get('district')
    municipality = Municipality.objects.filter(district_id=district_id).order_by('name')
    return render(request, 'municipality_dropdown.html', {'municipalities': municipality})

class VehicleRegistrationView(CreateView):
    model=RegisteredVehicle
    template_name="vehicle_registration.html"
    fields=["vehicle" ,"bluebook","registration_certificate"]
    success_url='myapp:home'

    def form_valid(self, form):
        form.instance.owner = self.request.user 
        return super().form_valid(form)

class SeeVehicles(TemplateView):
    template_name="vehicleinfo.html"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['data']=RegisteredVehicle.objects.get(owner=self.request.user)
        print(context)
        return context
    