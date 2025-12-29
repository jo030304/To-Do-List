from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),                    # 메인 화면
    path('login/', views.login_view, name='login'),         # 로그인
    path('signup/', views.signup_view, name='signup'),      # 회원가입
    path('logout/', views.logout_view, name='logout'),      # 로그아웃
    path('todos/', views.todo_list, name='todo_list'),      # 할 일 목록
]