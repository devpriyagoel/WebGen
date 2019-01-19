from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm,UserUpdateForm,ProfileUpdateForm
from django.contrib.auth.decorators import login_required
def home(request):
	return render(request, 'webgen/home.html')

def register(request):
	if request.method == 'POST':
		form = UserRegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			messages.success(request, f'Account created for {username}!')
			return redirect('login')
	else:
		form = UserRegistrationForm()
	return render(request, 'webgen/register.html', {'form': form})


@login_required
def profile(request):
	if request.method == 'POST':
		u_form=UserUpdateForm(instance=request.POST)
		p_form=ProfileUpdateForm(instance=request.user.profile)
	else:
		u_form=UserUpdateForm(instance=request.user)
		p_form=ProfileUpdateForm(instance=request.user.profile)
	context={
    	'u_form':u_form,
    	'p_form':p_form
	}
	return render(request, 'webgen/profile.html',context)

# Create your views here.
