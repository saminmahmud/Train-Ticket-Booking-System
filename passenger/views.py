
from django.shortcuts import render, redirect
from .forms import UserAccountForm,UserAccountChangeForm
from .models import UserAccount
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import FormView
from django.views.generic import  UpdateView,DetailView
from django.views import View
from .models import UserAccount
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
 

class UserRegistrationView(FormView):
    template_name = 'register.html'
    form_class = UserAccountForm
    # success_url = reverse_lazy('index')
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        # confirm_link = f"http://127.0.0.1:8000/account/active/{uid}/{token}"
        confirm_link = f"https://bangladesh-railway-h8hw.onrender.com/account/active/{uid}/{token}"
        email_subject = "Confirm Your Email"
        email_body = render_to_string('confirm_email.html', {'link': confirm_link})
        email = EmailMultiAlternatives(email_subject, '', to=[user.email])
        email.attach_alternative(email_body, "text/html")
        email.send()

        messages.success(self.request, 'Check your email for Email Verification🎯')
        return super().form_valid(form)

def activate(request, uid64, token):

    try:
        uid = urlsafe_base64_decode(uid64).decode()
        # user = UserAccount.objects.get(pk=uid).user
        user = User._default_manager.get(pk=uid)
    except UserAccount.DoesNotExist:
        user = None 
    print(uid)
    print(user)
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    else:
        print("paise na")
        return redirect('register')

class UserLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('home')

# class UserLogoutView(LogoutView):
#     def get_success_url(self):
#         if self.request.user.is_authenticated:
#             logout(self.request)
#         return reverse_lazy('home')

# class UserLogoutView(LogoutView):
#     def get_success_url(self):
#         return reverse_lazy('home')

def UserLogoutView(request):
    logout(request)
    return redirect('index')


class UserAccountUpdateView(View):
    template_name = 'profile.html'

    def get(self, request):
        form = UserAccountChangeForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = UserAccountChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to the user's profile page
        return render(request, self.template_name, {'form': form})
    
@login_required
def UserProfileView(request):
    return render(request, 'profile.html')


@method_decorator(login_required, name='dispatch')
class edit_profile(UpdateView):
    model = User
    form_class = UserAccountChangeForm
    template_name = 'edit_profile.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')

@login_required
def passChange(request):
    if request.method == 'POST':
        form = SetPasswordForm( request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Password Change Successfully😀')
            return redirect('profile')
    else:
        form = SetPasswordForm(request.user)
    return render(request, 'pass_change.html', {'form' : form})


from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import UserAccount
from .forms import DepositForm

@login_required
def deposit_money(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data.get('amount')
            user = request.user

            account, created = UserAccount.objects.get_or_create(user=user)

            initial_balance = account.balance
            new_balance = initial_balance + amount

            print(f"amount: {amount}")
            print(f"NID: {account.nid}")
            print(f"initial_balance: {initial_balance}")
            print(f"new_balance: {new_balance}")

            account.balance = new_balance
            print(f"new_balance: {account.balance}")
            account.save(update_fields=['balance'])

            messages.success(request, 'Deposit successful😀')
            return redirect('home')
    else:
        form = DepositForm()

    return render(request, 'deposit.html', {'form': form})