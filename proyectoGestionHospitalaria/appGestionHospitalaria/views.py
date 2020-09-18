from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import patient, doctor, estudio
from django.views import generic
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from .forms import SignUpForm



# Create your views here.
@login_required
def index(request):

    """
        Función vista para la página inicio del sitio.
    """
    num_medicos = doctor.objects.all().count()
    num_pacientes = patient.objects.all().count()
    num_estudios = estudio.objects.all().count()

    return render(request, 'index.html', context ={'num_medicos':num_medicos, 'num_pacientes':num_pacientes, 'num_estudios':num_estudios})



def usuarios(request):
    #latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #context = {'latest_question_list': latest_question_list}
    #return render(request, 'appGestionHospitalaria/index.html', context)

    # return render(request, 'appGestionHospitalaria/index.html')
    return HttpResponse("Hello, world. You're at the users index.")


class patientsListView(generic.ListView):
    model = patient
    paginate_by = 10

class patientDetailView(generic.DetailView):
    model = patient


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('Inicio')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


