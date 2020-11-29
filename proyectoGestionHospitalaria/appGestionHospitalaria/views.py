from django.http import HttpResponse
from .models import *
from django.shortcuts import render, redirect
from django.http import Http404
from .forms import SignUpFormMedico, SignUpFormPaciente, CreateFormTurno, EspecialidadForm, DoctorMatriculaForm, TurnoDateForm, DNIForm
from django.contrib.auth.models import Group, User
from .filters import DoctorFilter, PatientFilter, EstudioFilter, TurnoFilter



# funcion que valida los permisos de una vista en base a los grupos a los que pertenece el usuario
# y los grupos que permite la vista
def is_user_auth(user, valid_groups):
    # staff siempre tiene permiso
    if user.is_staff:
        return True
    
    # probé de otras formas que en teoría serian mas optimas pero no me dejó
    # valiar que hay al menos 1 grupo de los cuales el usuario pertenece y es valido
    for group in valid_groups:
        if user.groups.filter(name=group).exists():
            return True
    return False

def error_acceso(request):
    # se podría tirar algo aca, el proble es que al desloguear te habría que redirigirlo, 
    # sino deslogueo y quedo en una vista que necesita permisos y automaticamente despues
    #  de desloguear se activaria esta vista
    return redirect('index')
    # return HttpResponse('usted no tiene permiso para solicitar esta pagina - bajo construcción')    

def timefields_to_min(timefield):
    lista_num_str = str(timefield).split(':')
    lista_num_int = []
    
    for i in lista_num_str:
        numero = int(i)
        lista_num_int.append(numero)
    
    minutos = (lista_num_int[0]*60) + lista_num_int[1] + (lista_num_int[2]/60) # horas *60 y seg /60 y dejo todo en min
    
    return minutos

def operate_timefields(tf_inicial, tf_final, operation): 
    minutos_numero_inicial = timefields_to_min(tf_inicial)
    minutos_numero_final = timefields_to_min(tf_final)

    if (operation == 'suma'):
        return minutos_numero_final + minutos_numero_inicial 
    else:
        return minutos_numero_final - minutos_numero_inicial 


def index(request):
    # chequeo si el user pertenece a un grupo y en base a eso defino si esta autorizado o no
    # lo mando al template para chequear que pueve ver ahi también
    # exist se aplica a una colección por eso uso filter, con get no funciona.
    """
        Función vista para la página inicio del sitio.
    """
    num_medicos = Doctor.objects.all().count()
    num_pacientes = Paciente.objects.all().count()
    num_estudios = Estudio.objects.all().count()

    context = {
        'num_medicos': num_medicos,
        'num_pacientes': num_pacientes, 
        'num_estudios': num_estudios,
    }

    return render(request, 'index.html', context)

# <int:paciente_id>/ es mandado como parametro
# si no lo agrego en la funcion de abajo genera error
def paciente(request, paciente_id):
    if not is_user_auth(request.user, ('secretarios', 'medicos', 'sarasa')):
        return redirect('error_acceso')
   
    try:
        paciente = Paciente.objects.get(pk=paciente_id)
    except Paciente.DoesNotExist:
        raise Http404("El paciente no existe")
    
    return render(request, 'paciente_detail.html', {'paciente': paciente})

def pacientes(request):
    if not is_user_auth(request.user, ('secretarios', 'medicos', 'sarasa')):
        return redirect('error_acceso')
    
    paciente_list = Paciente.objects.order_by('dni')

    myFilter = PatientFilter(request.GET, queryset=paciente_list)
    paciente_list = myFilter.qs

    context = {
        'paciente_list': paciente_list,
        'myFilter': myFilter
    }
    return render(request, 'paciente_list.html', context)

def medico(request, doctor_id):
    if not is_user_auth(request.user, ('secretarios', 'medicos', 'sarasa')):
        return redirect('error_acceso')

    try:
        doctor = Doctor.objects.get(pk=doctor_id)
        especialidades = doctor.especialidad.all()
        context = {
        'doctor': doctor,
        'especialidades': especialidades
        }
    
    except Doctor.DoesNotExist:
        raise Http404("El paciente no existe")
    return render(request, 'medico_detail.html', context)


# @login_required en vez de usar esto chequeamos si el user pertenece a un grupo y mandamos
# el si o no por el context - mas facil asi parece
def medicos(request):
    if not is_user_auth(request.user, ('secretarios', 'sarasa')):
        return redirect('error_acceso')
      
    doctores = Doctor.objects.order_by('matricula')

    myFilter = DoctorFilter(request.GET, queryset=doctores)
    doctores = myFilter.qs

    context = {
        'doctores': doctores,
        'myFilter': myFilter
    }
    return render(request, 'medico_list.html', context)

def turnos(request):
    if not is_user_auth(request.user, ('secretarios', 'sarasa')):
        return redirect('error_acceso')
      
    turnos = Turno.objects.all()

    myFilter = TurnoFilter(request.GET, queryset=turnos)
    turnos = myFilter.qs

    #for i in turnos:
       # print(i.estudio.doctor.user.first_name)
        #print(i.estudio.paciente.user.first_name)

    context = {
        'turnos': turnos,
        'myFilter': myFilter
    }
    return render(request, 'turno_list.html', context)


def historiasMedicas(request):
    if not is_user_auth(request.user, ('secretarios', 'medicos', 'sarasa')):
        return redirect('error_acceso')

    estudios = Estudio.objects.filter(confirmed=True)

    myFilter = EstudioFilter(request.GET, queryset=estudios)
    estudios = myFilter.qs

    context = {
        'estudios': estudios,
        'myFilter': myFilter
    }
    return render(request, 'historia_list.html', context)

def historia(request, estudio_id):
    if not is_user_auth(request.user, ('secretarios', 'medicos', 'sarasa')):
       return redirect('error_acceso')

    try:
        estudioAux = Estudio.objects.get(pk=estudio_id)
        files = EstudioFile.objects.filter(estudio = estudioAux)

        context = {
            'estudio': estudioAux,
            'files': files
        }

    except Estudio.DoesNotExist:
        raise Http404("El estudio no existe")
    return render(request, 'historia_detail.html', context)

dict_especialidades = {
    'traumatologia': 'Traumatología',
    'clinica_medica': 'Clínica médica',
    'cardiologia': 'Cardiología',
    'dermatologia': 'Dermatología',
    'oftalmologia': 'Oftalmologia',
    'endocrinologia': 'Endocrinología',
    'ginecologia': 'Ginecología',
    'obstetricia': 'Obstetricia',
    'psicologia': 'Psicología',
    'diagnostico_por_imagenes': 'Diagnóstico por Imágenes',
    'nutricion': 'Nutrición',
    'pediatria': 'Pediatría',
    'psiquiatria': 'Psiquiatría',
    'neumonologia': 'Neumonología'
}

lista_especialidades_nombres = [
    'traumatologia',
    'clinica_medica',
    'cardiologia',
    'dermatologia',
    'oftalmologia',
    'endocrinologia',
    'ginecologia',
    'obstetricia',
    'psicologia',
    'diagnostico_por_imagenes',
    'nutricion', 
    'pediatria',
    'psiquiatria',
    'neumonologia',
]

def signup_medico(request):
    # le damos a is_auth los grupos permitidos en la vista
    # is auth devuelve true si el usuario tiene permisos en la vista
    if not is_user_auth(request.user, ('secretarios', 'sarasa')):
        return redirect('error_acceso')

    # si el usuario esta autorizado a ver la vista sigue
    if request.method == 'POST':
        # Create a form instance from POST data.
        form = SignUpFormMedico(request.POST)
        if form.is_valid(): # sino el cleaned data get no funca - dependiendo del tipo de form chequea que las instancais no sea repetidas en la bd también
            print(request.POST) # para ver la post data
            # Save a new User object from the form's data.
            new_user = form.save()
            grupo = Group.objects.get(name='medicos')
            new_user.groups.add(grupo)
            # new_user.refresh_from_db()  # load the profile instance created by the signal - 
            # no estoy seguro que sea necesario, estoy probando sin esto y por ahora va bien
            
            matricula_form = form.cleaned_data.get('matricula') # agarra por el name del input, no mira el id 
          
            # new_user.save() # verificar si hace falta guardar de nuevo
            new_doctor = Doctor(matricula=matricula_form, user=new_user)
            new_doctor.save()

            # añadiendo las especialidades al doctor
            index = 0
            for i in lista_especialidades_nombres:
                # si el checkbox no se marco directamente no se manda y da falso aca
                if form.cleaned_data.get(i):
                    nombre = dict_especialidades[i]
                    especialidad = Especialidad.objects.get(name=nombre) 
                    new_doctor.especialidad.add(especialidad)
                    print('especialidad seleccionada:', especialidad.name)
                index = index + 1
            

            new_user.save() 
            new_doctor.save()
            # me paso que necesitaba guardar antes de agregar especialidades, anda pero verificar
            # si es necesario el codigo restante, talvez no lo sea
            # doctor.refresh_from_db()
            # doctor.especialidad.add(especialidad) 
            # new_user.save() # no hace falta guardar devuelta el usuario al final de todo x ahora aparentemente
            return redirect('index')
        else:
            # falta agregar error por si el form es invalid
            print('form fail')
            print(form.errors)
            return redirect('index')
            
    else:
        # envio las especialidades al front para mostrarlas en el desplegable del alta
        context = { 
            'especialidades': Especialidad.objects.order_by('name')
        }       
        return render(request, 'signup_medico.html', context)

# todos los comentarios de signup_medico aplican aca
def signup_paciente(request):
    # por ahora saco el permiso para registrar pacientes al sistema, que se registre cualquiera
    # if not is_user_auth(request.user, ('pacientes')):
    #     return redirect('error_acceso')

    if request.method == 'POST':
        form = SignUpFormPaciente(request.POST)
        print(form.errors)
        if form.is_valid():
            new_user = form.save() 
            numero_telefono_form = form.cleaned_data.get('phone_number') 
            dni_form = form.cleaned_data.get('dni')
            date_of_birth_form = form.cleaned_data.get('date_of_birth')
            obra_social_form = form.cleaned_data.get('obra_social')
            grupo = Group.objects.get(name='pacientes')
            new_user.groups.add(grupo)
            new_user.save()
            paciente = Paciente(dni=dni_form, date_of_birth=date_of_birth_form, phone_number=numero_telefono_form, user=new_user)
            paciente.obra_social = Obra_social.objects.get(name=obra_social_form)
            paciente.save()
            return redirect('index')  
        else:
            # invalid form
            pass
    else:
        context = {
            'obras_sociales': Obra_social.objects.order_by('name'),
        }
        return render(request, 'signup_paciente.html', context)

def create_turno_1(request):
    if not is_user_auth(request.user, ('secretarios', 'pacientes')):
        return redirect('/accounts/login')
    
    # El post directamente lo hace en /2 - esta seteado desde el front
    if request.method == 'GET':
        context = {
            'especialidades': Especialidad.objects.all()
        }
        return render(request, 'create_turno_1.html', context)
    else:
        return redirect('error_acceso')

def create_turno_2(request):
    if not is_user_auth(request.user, ('secretarios', 'pacientes')):
        return redirect('error_acceso')

    if request.method == 'GET':
        form = EspecialidadForm(request.GET)
        if form.is_valid(): 
            especialidad_name = form.cleaned_data.get('name')
            especialidad = Especialidad.objects.get(name=especialidad_name)
            doctores = Doctor.objects.filter(especialidad=especialidad)
            # tipoEstudios = TipoEstudio.objects.filter(especialidad=especialidad)
            context = {
                'doctores': doctores,
                'especialidad': especialidad,
                # 'tipoEstudios': tipoEstudios,
                # 'lista_pacientes': Paciente.objects.all()

            }
            return render(request, 'create_turno_2.html', context)
        else:
            return redirect('error_acceso')
    else:
        return redirect('error_acceso')

def create_turno_3(request):
    if not is_user_auth(request.user, ('secretarios', 'pacientes')):
        return redirect('error_acceso')
    
    if request.method == 'GET':
        form = DoctorMatriculaForm(request.GET) # Me quedo con la matricula por el value dentro del select
        if form.is_valid():
            especialidad_name = form.cleaned_data.get('especialidad') 
            especialidad = Especialidad.objects.get(name=especialidad_name)
            matricula = form.cleaned_data.get('matricula')
            doctor = Doctor.objects.get(matricula=matricula)

            context = {
                # 'tipo_estudios': TipoEstudio.objects.all(),
                'lista_pacientes': Paciente.objects.all(),
                'especialidad': especialidad,
                'doctor': doctor 
            }
        
            return render(request, 'create_turno_3.html', context)

dict_dias = {
    '0': 'Lunes',
    '1': 'Martes',
    '2': 'Miércoles',
    '3': 'Jueves',
    '4': 'Viernes',
    '5': 'Sábado',
    '6': 'Domingo'
}

def create_turno_4(request):
    if not is_user_auth(request.user, ('secretarios', 'pacientes')):
        return redirect('error_acceso')     

    if request.method == 'GET':
        doctorForm = DoctorMatriculaForm(request.GET)
        turnoForm = TurnoDateForm(request.GET)
        if turnoForm.is_valid() and doctorForm.is_valid():
            mpt = 15 # mintuos por turno usado mas adelante
            date = turnoForm.cleaned_data.get('date') 
            dia = dict_dias[str(date.weekday())]  # date.weekday() traduce date a dias -> 0 es lunes y 7 domingo 
            matricula = doctorForm.cleaned_data.get('matricula')
            doctor = Doctor.objects.get(matricula=matricula)
            turnos_de_jornadas = TurnoJornada.objects.filter(doctor=doctor)

            atiende_ese_dia = False
            turnos_jornada = []
            for i in turnos_de_jornadas:
                if i.dia.nombre == dia:
                    atiende_ese_dia = True
                    turnos_jornada.append(i)
            
            cantidad_de_turnos = []
            for i in turnos_jornada:
                a = operate_timefields(i.horario_inicio, i.horario_fin, 'resta')
                a = int(a//mpt) # 15 minutos por turno, esto lo podriamos cambiar
                cantidad_de_turnos.append(a) # total de min de turnos / m por turno

            turnos_disponibles = []
            index_i = 0
            for i in cantidad_de_turnos:
                base = timefields_to_min(turnos_jornada[index_i].horario_inicio)
                index_i = index_i + 1
                for x in range(i):
                    horario = base + x*mpt
                    horario = int(horario)
                    turnos_disponibles.append(horario)

            # esta forma hace 12:00pm = noon y es re molesto   
            # index_i = 0
            # for i in turnos_disponibles:
            #     horas = i/60
            #     minutos = int(horas % 1 * 60)
            #     horas = int(horas)
            #     turno = datetime.time(horas, minutos, 0)
            #     turnos_disponibles[index_i] = turno
            #     print(turno)
            #     index_i = index_i + 1

            index_i = 0
            lista_turnos = []
            for i in turnos_disponibles:
                horas = i/60
                minutos = int(horas % 1 * 60)
                if minutos == 0:
                    minutos = '00'
                else:
                    minutos = round(minutos,2)
                horas = int(horas)
                if horas >= 12:
                   lista_turnos.append(str(horas) + ':' + str(minutos) + 'pm')
                else:
                    lista_turnos.append(str(horas) + ':' + str(minutos) + 'am')
                index_i = index_i + 1
            print(lista_turnos)

            # Turno.objects.filter(date=date).exists() 
            context = {
                'turnos_disponibles': lista_turnos
            }
            return render(request, 'create_turno_4.html', context) 
        else:
            print('-------------------------------')
            print('errores del form de doctor')
            print(doctorForm.errors)
            print('errores del form de turno')
            print(turnoForm.errors)
            print('-------------------------------')
            


# viejo crear turno
def create_turno_3_old(request):
    if not is_user_auth(request.user, ('secretarios', 'pacientes')):
        return redirect('error_acceso')

    if request.method == 'POST':
        form = TurnoDateForm(request.POST)
        form2 = DoctorMatriculaForm(request.GET)
        print(form.errors)
        if form.is_valid() and form2.is_valid():
            # print('p:', request.POST)
            # print('g:', request.GET)

            # lo que estamos haciendo es por matricula por ahora, cambiarlo a nombre del doctor despues
            # el nombre esta en su usuario
            matricula_form = form2.cleaned_data.get('matricula')
            doctor = Doctor.objects.get(matricula=matricula_form)
            print('doctor:', doctor.user.first_name )

            # faltaria agregar si es secretario tmb
            if request.user.is_superuser:
                paciente_dni = request.POST.get('paciente')

                print()
                print('dni:', paciente_dni)
                pac = Paciente.objects.get(dni=paciente_dni)
                print(pac.user.first_name)
                paciente = Paciente.objects.get(dni=paciente_dni) #Obtiene el dni desde un desplegable
            else:
                print('por aca no tiene que entrar')
                paciente = request.user.paciente
                # if is_user_auth(request.user, ('pacientes')): #secretarios
                #     paciente = Paciente.objects.get(user=request.user.id) #Obtiene el id desde el usuario
                # else:
                #     paciente_form = form.cleaned_data.get('paciente')
                #     paciente = Paciente.objects.get(dni=paciente_form) #Obtiene el dni desde un desplegable

            #secretary = User.objects.get(pk=1) #por ahora por defecto, se relaciona con un secretario (empiezo a dudar si es necesario)
            
            # esto por ahora, el tipo de estudio no deberia estar, es la especialidad la que usamos
            
            tipo_de_estudio = TipoEstudio.objects.get(pk=1)
            description = ''
            estudio = Estudio(tipo=tipo_de_estudio, doctor=doctor, paciente=paciente, description=description)
            
            new_estudio = estudio.save() #Crea el estudio
            
            # creacion del turno
            date = form.cleaned_data.get('date')
            timeFrom = form.cleaned_data.get('timeFrom')
            # timeTo = timeFrom.replace(hour=(timeFrom.hour+estudio1.type.duration) % 24) #Suma la duracion de estudio
            #turno = Turno(estudio=estudio1, date=date, timeFrom=timeFrom, timeTo=timeTo)
            turno = Turno(estudio=new_estudio, date=date, timeFrom=timeFrom)
            turno.save() # Crea el turno a partir de ese estudio
            # print('turno.estudio.doctor.user.first_name:', estudio.doctor.user.first_name, 'turno.estudio.paciente.user.first_name:', estudio.paciente.user.first_name)
            # return HttpResponse('hala madrid')
            return redirect('index')
        else:
            return HttpResponse('form no valid')
    else:
        # get method
        form = DoctorMatriculaForm(request.GET) # Me quedo con la matricula por el value dentro del select
        if form.is_valid():
            # la especialidad la llevo en el action del form - voy a probar con method get despues
            especialidad_name = form.cleaned_data.get('especialidad')
            especialidad = Especialidad.objects.get(name=especialidad_name)
            matricula = form.cleaned_data.get('matricula')
            doctor = Doctor.objects.get(matricula=matricula)


            # lo que habria que hacer es una vez que nos da el dia, recargar el horario con los turnos disponibles para ese dia
            context = {
                # 'tipo_estudios': TipoEstudio.objects.all(),
                'lista_pacientes': Paciente.objects.all(),
                'especialidad': especialidad,
                'doctor': doctor 
            }
            
            return render(request, 'create_turno_3.html', context)