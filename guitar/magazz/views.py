from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import RegisterUserForm, LoginUserForm
from django.urls import reverse_lazy
from .utils import*
import smtplib
from email.mime.text import MIMEText
# Create your views here.


def index(request):
    return render(request, "magazz/index.html")

def about(request):
    return render(request, "magazz/about us.html")

def contact(request):
    if request.user.is_authenticated:
        if request.POST.get("textarea"):
            print("Massage push")
            msg_get(request.user.email, request.POST.get("textarea"), request.user.username)

    return render(request, "magazz/contact.html")


def msg_get(user_email, string_user, user_name):
    email_sender = user_email
    password = "6xmHvFWL2s8F0dwhcY5e"
    email_getter = "skrudji02@mail.ru"

    smtp_server = smtplib.SMTP("smtp.mail.ru", 587)
    smtp_server.starttls()

    msg = MIMEText(str(string_user))
    msg["Subject"] = str(user_name)
    smtp_server.login(email_sender, password)
    smtp_server.sendmail(email_sender, email_getter, msg.as_string())


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'magazz/register.html'
    success_url = reverse_lazy('login')


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class LoginUser(DataMixin, LoginView):
    #form_class = LoginUserForm
    template_name = 'magazz/login.html'
    #success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('index')

def logout_user(request):
    logout(request)
    return redirect('index')