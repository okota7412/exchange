from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

#ユーザ管理用
class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

#simuページ用
class SimParameterForm(forms.Form):
    temperature =  forms.FloatField(label="温度(℃)", initial=25.0, min_value=-273.15)
    exe_time = forms.FloatField(label="シミュレーション時間(ns)", min_value=0)
    exe_step = forms.FloatField(label="時間刻み(fs)", min_value=0)


# class SimParameterForm(forms.Form):
#     molecularName = forms.ChoiceField(label="分子名", choices=molecular, initial="水")
#     molecularNumber = forms.IntegerField(label="分子数", initial=100)
#     pressure = forms.FloatField(label="圧力(atm)")
#     temperature =  forms.FloatField(label="温度(℃)", initial=25.0)
#     exeTime = forms.FloatField(label="シミュレーション時間(ns)", min_value=0)
#     exeStep = forms.FloatField(label="時間刻み(fs)", min_value=0)
#     boxSelect = forms.ChoiceField(label="ボックス", choices=box, widget=forms.RadioSelect(), initial="立方体")

# molecularName 
# molecularNumber 
# pressure 
# temperature 
# exeTime 
# exeStep 
# boxSelect
