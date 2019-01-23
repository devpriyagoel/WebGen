from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserRegistrationForm, UserUpdateForm, ProfileUpdateForm, AboutUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Course, About,Profile
from django.core.files.storage import FileSystemStorage


def home(request):
	search_term = ''
	abouts = About.objects.all()
	if 'search' in request.GET:
		search_term = request.GET['search']
		abouts = About.objects.filter(name__icontains = search_term)
	context = {'search_term':search_term, 'abouts':abouts}
	return render(request, 'webgen/home.html', context)

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
		u_form=UserUpdateForm(request.POST, instance=request.user)
		p_form=ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
		
		u_form.save()
		p_form.save()
		messages.success(request, f'Account updated!')
		return redirect('profile')
	else:
		u_form=UserUpdateForm(instance=request.user)
		p_form=ProfileUpdateForm(instance=request.user.profile)
	context={
    	'u_form':u_form,
    	'p_form':p_form
	}
	return render(request, 'webgen/profile.html',context)

@login_required
def about(request):
	if request.method == 'POST':
		a_form=AboutUpdateForm(request.POST, request.FILES, instance=request.user.about)
		a_form.save()
		messages.success(request, f'Account updated!')
		return redirect('about')
	else:
		a_form=AboutUpdateForm(instance=request.user.about)
	context={
    	'a_form':a_form
	}
	return render(request, 'webgen/about.html',context)

@login_required
def teaching(request):
	context = {
        'courses': Course.objects.all()
    }
	return render(request, 'webgen/teaching.html', context)

class CourseListView(ListView):
    model = Course
    template_name = 'webgen/teaching.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course


class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    fields = ['course_title', 'content']

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)


class CourseUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Course
    fields = ['course_title', 'content']

    def form_valid(self, form):
        form.instance.teacher = self.request.user
        return super().form_valid(form)

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.teacher:
            return True
        return False


class CourseDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Course
   # success_url = 'teaching/' 

    def test_func(self):
        course = self.get_object()
        if self.request.user == course.teacher:
            return True
        return False
@login_required
def upload(request):
	if request.method=='POST':
		uploaded_file=request.FILES['document']
		fs=FileSystemStorage()
		fs.save(uploaded_file.name, uploaded_file)

	return render(request, 'webgen/upload.html')
# Create your views here.

def prof_page(request, pk=None):
	q = About.objects.get(pk=pk)
	username = q.user.username
	qs = get_object_or_404(Profile, user__username=username)
	cou = Course.objects.filter(teacher__username=username)
	abo = About.objects.filter(user__username=username)

	context ={'q':q, 'qs':qs , 'cou':cou , 'abo':abo}

	return render(request,'webgen/response.html' ,context)
