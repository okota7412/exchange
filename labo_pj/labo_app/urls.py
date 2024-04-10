from django.urls import path
from . import views,ajax

urlpatterns = [
    path('', views.top_view, name='top'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('simu/', views.simu_view, name='simu'),
    path('result/', views.result_view, name='result'),
    path('ajax_exe_com/', ajax.ajax_exe_com, name='ajax_exe_com'),
    path('execute_command/', views.real_time_execute_command_view, name='execute_command'),
    path('get_output/', ajax.get_output, name='get_output'),
    path('ajax_exe_gmx_com/', ajax.ajax_exe_gmx_com, name='ajax_exe_gmx_com'),
    path('ajax_heavy_task/', ajax.ajax_heavy_task, name='ajax_heavy_task'),
    path('ajax_rdf/', ajax.ajax_rdf, name='ajax_rdf'),
    path('ajax_msd/', ajax.ajax_msd, name='ajax_msd'),
    # path('download/xtc/', views.xtc_download, name='xtc'),
    # path('hamburger/', views.hamburger, name='hamburger'),
    # path('download/<int:user_id>/', views.gro_download, name='gro_download'),
    # path('download/<int:user_id>/', views.users, name='users'),
    # path('download/<int:user_id>/zip/', views.gmx_zip, name='gmx_zip'),　二重圧縮ならないように
    path('download/<int:user_id>/gztar/', views.gmx_gztar, name='gmx_gztar'),
]
