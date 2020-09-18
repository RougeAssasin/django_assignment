from django.shortcuts import render
from .forms import LoginForm, SignupForm
import requests
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse 
from .models import Profile
from django.contrib.auth.decorators import login_required
import secrets

def login_view(request):
	form = LoginForm()
	if request.method == 'POST':

		username = Profile.objects.get(email=request.POST['email']).username	
		password = request.POST['password']

		user = authenticate(username = username, password = password)
		if user is not None:
			rsp = requests.post('http://127.0.0.1:8000/api/token/'
				  , data={'username': username, 'password': password}).json()

			token = rsp['access']
			headers = {"Authorization":"Bearer " + token}
			rsp2 = requests.get('http://127.0.0.1:8000/auth/', headers=headers)

			if 'auth' in rsp2.text:
				js = rsp2.json()
				print(js['auth'])	
				login(request, user)
				return redirect(reverse('profile'))
			
			else:
				return render(request, 'login.html', {'form' : form, 'error': 'Something wrong ,try again'})
      	
		else:
			return render(request, 'login.html', {'form' : form, 'error': 'Invalid Credentials'})
		
		# print(token)
	return render(request, 'login.html', { 'form': form })

def signup_view(request):
	form = SignupForm()
	if request.method == 'POST':
		form = SignupForm(data = request.POST)
		if form.is_valid():
			username = request.POST['first_name']
			password = request.POST['password']
			user = User.objects.create(username = username, password=password)
			user.image = request.POST['image']
			user.profile.first_name = request.POST['first_name']
			user.profile.last_name  = request.POST['last_name']
			user.profile.age		= request.POST['age']
			if form['unique_id'] == "":
				user.profile.unique_id	= secrets.token_hex(3)
			else:
				user.profile.unique_id	= request.POST['unique_id']

			user.profile.email		= request.POST['email']
			user.save()
			form = SignupForm()
	return render(request, 'signup.html', {'form': form})

@login_required
def profile_view(request):
	profile = Profile.objects.filter(user=request.user)
	if request.method == 'POST':
		logout(user)
		return redirect(reverse('login'))
	return render(request, 'profile.html', {'profile': profile})