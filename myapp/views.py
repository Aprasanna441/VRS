from base64 import urlsafe_b64encode
from typing import Any, Dict
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth import login,logout,authenticate
from django.views.generic import CreateView,FormView,TemplateView,UpdateView,View
from .models import CustomUser,Citizen,Municipality,District,RegisteredVehicle,Transactions
from .forms import CitizenRegistrationForm,CitizenLoginForm,ForgetPasswordForm,ResetPasswordForm
from django.contrib.auth.mixins import LoginRequiredMixin
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
    success_url=reverse_lazy('myapp:home')



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
        
    


class ProfileView(LoginRequiredMixin,TemplateView):
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
from django.contrib.auth.forms import PasswordChangeForm  
def password_change_view(request):
    if request.method == 'POST':
        pass_form = PasswordChangeForm(user=request.user, data=request.POST)
        if pass_form.is_valid():
            pass_form.save()
            return redirect('myapp:login')
    else:
        pass_form = PasswordChangeForm(user=request.user)
    return render(request, 'passwordchange.html', {'form': pass_form})

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

class VehicleRegistrationView(LoginRequiredMixin,CreateView):
    model=RegisteredVehicle
    template_name="vehicle_registration.html"
    fields=["vehicle" ,"bluebook","registration_certificate"]
    success_url=reverse_lazy('myapp:home')

    def form_valid(self, form):
        form.instance.owner = self.request.user.citizen
        return super().form_valid(form)


#decorator to check response but is not used as i got other easier logic
class CustomVehicleMixin:
    def dispatch(self, request, *args, **kwargs):
        #  res=RegisteredVehicle.objects.get(owner__user = self.request.user)
         cu=request.user
         res=RegisteredVehicle.objects.filter(owner__user=request.user)
         print(res)
        #  if  res.first():
        #      return super().dispatch(request,*args,**kwargs)
        #  else:
        #      return HttpResponse("No reg")
         return HttpResponse("Hi")



class SeeVehicles(LoginRequiredMixin,TemplateView):
    template_name="vehicleinfo.html"


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        u=self.request.user.id
        c=Citizen.objects.get(user = u)
        
       
        # res=RegisteredVehicle.objects.filter(owner__user = self.request.user)
        res=RegisteredVehicle.objects.filter(owner=c)
     
        
        context["data"]=res
        
       
      
       
        return context


def fintecherror(request):
    return  HttpResponse("Payment error aayo Feri prayas garnuhola")   

class EsewaRequestView(View):
    def get(self,request,*args,**kwargs):
        vid=self.kwargs.get('vid')
        vehicle=RegisteredVehicle.objects.get(id=vid)

        
        context={
            "order":vehicle
        }

        return render(request,"esewapayment.html",context)
import xml.etree.ElementTree as ET
import requests
class EsewaVerifyView(View):
    def get(self,request,*args,**kwargs):
        oid=request.GET.get("oid")
        amt=request.GET.get("amt")
        ref_id=request.GET.get("refId")
        url ="https://uat.esewa.com.np/epay/transrec"
        d = {
        'amt': amt,
        'scd': 'EPAYTEST',
        'rid': ref_id,
        'pid':oid,
        }
        resp = requests.post(url, d)
        inside=ET.fromstring(resp.content)
        status=inside[0].text.strip()  #removes white space from the status code 
        order_id=oid.split("_")[1]   #order_12 ko form ma hunxa ani  12 matra nikalne ho esbata
        order_obj=RegisteredVehicle.objects.get(id=order_id)
        print("yaha sam")
        if status=="Success":
            order_obj.renewed_date=timezone.now()
            order_obj.save()
            temp=RegisteredVehicle.objects.get(id=order_id)
            tr=Transactions(vehicle=temp,amount=float(amt))
            tr.save()
            print("Tr sav")


            return redirect("myapp:home")
        else:
            
            return redirect("/esewapayment/order_id/")
    


