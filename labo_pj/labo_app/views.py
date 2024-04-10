import subprocess,os,json,re,sys,time
from django.shortcuts import render
from django.http import FileResponse
from .gmxapp import gmx
from .ajax import remove_sp_char
from .forms import SimParameterForm, SignupForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

# Create your views here.
def top_view(request):
    return render(request, 'labo_app/top.html')


@login_required
def logout_view(request):
   logout(request)
   return render(request, 'labo_app/top.html')

def signup_view(request):
    if request.method == 'POST':

        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'labo_app/simu.html',{'SimForm': SimParameterForm()})

    else:
        form = SignupForm()
    
    params = {
        'form': form
    }
    return render(request, 'labo_app/signup.html', params)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user:
                login(request, user)
                return render(request, 'labo_app/simu.html', {'SimForm': SimParameterForm()})
    else:
        form = AuthenticationForm()

    param = {
        'form': form,
    }

    return render(request, 'labo_app/login.html', param)

@login_required
def simu_view(request):
    params ={
        'SimForm': SimParameterForm()
    }
    return render(request, 'labo_app/simu.html', params)

@login_required
def real_time_execute_command_view(request):
    return render(request, 'labo_app/real_time_execute_command.html')

@login_required
def result_view(request):
    # フォルダ名のためにuser.idを取得する
    user = getattr(request, "user", None)
    user_id = user.id
    template_name = "labo_app/result.html"
    sim_form = SimParameterForm(request.POST or None)

    molecular_name = remove_sp_char(request.POST.getlist("molecular_name"))
    molecular_number = remove_sp_char(request.POST.getlist("molecular_number"))
    box_size = remove_sp_char(request.POST.getlist("box_size"))
    pressure = remove_sp_char(request.POST.get("pressure"))
    ensemble = remove_sp_char(request.POST.get("ensemble"))
    print(ensemble)
    
    if sim_form.is_valid():
        temperature = sim_form.cleaned_data["temperature"]
        exe_time = sim_form.cleaned_data["exe_time"]
        exe_step = sim_form.cleaned_data["exe_step"]
        print("POSTが確認されました")
        print(molecular_name)
        print(molecular_number)
        print(pressure)
        print(temperature)
        print(exe_time)
        print(exe_step)
        print(box_size)
        
        ctx = {"ensemble": ensemble,
               "molecular_name": molecular_name,
               "molecular_number": molecular_number,
               "pressure": pressure,
               "temperature": temperature,
               "exe_time": exe_time,
               "exe_step": exe_step,
               "box_size": box_size,
               "user_id": user_id,
               }
        print(ctx)
        # start = time.time()
        # ここでシミュレーションを実行させる
        # gmx.simulation(ctx)
        # finish = time.time()
        # elapsed_t = finish - start
        # ctx["elapsed_t"] = int(elapsed_t)
        return render(request, template_name, ctx)
    else:
        return render(request, 'labo_app/simu.html', {'SimForm': SimParameterForm()})

def gmx_gztar(request, user_id):
    gmx.gmx_gztar(user_id)
    path = r'/home/labo_pj/labo_app/gmxapp/user_id/%s/gmx.tar.gz' % user_id
    return FileResponse(open(path, "rb"), as_attachment=True, filename='gmx.tar.gz')
