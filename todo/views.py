from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Todo

# 메인 화면
def index(request):
    if request.user.is_authenticated:
        return redirect('todo_list')
    return render(request, 'todo/index.html')

# 로그인
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/login/?success=true')
        else:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
    
    return render(request, 'todo/login.html')

# 회원가입
def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        if password != password_confirm:
            messages.error(request, '비밀번호가 일치하지 않습니다.')
            return render(request, 'todo/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, '이미 존재하는 아이디입니다.')
            return render(request, 'todo/signup.html')
        
        User.objects.create_user(username=username, password=password)
        return redirect('/signup/?success=true')
    
    return render(request, 'todo/signup.html')

# 로그아웃
def logout_view(request):
    logout(request)
    return redirect('index')

# 할 일 목록
def todo_list(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            # 추가
            title = request.POST.get('title')
            category = request.POST.get('category', 'todo')
            deadline = request.POST.get('deadline')
            
            if title:
                todo = Todo.objects.create(
                    user=request.user, 
                    title=title, 
                    category=category
                )
                if deadline:
                    todo.deadline = deadline
                    todo.save()
            
        elif action == 'update':
            # 수정
            todo_id = request.POST.get('todo_id')
            title = request.POST.get('title')
            deadline = request.POST.get('deadline')
            
            if todo_id and title:
                try:
                    todo = Todo.objects.get(id=todo_id, user=request.user)
                    todo.title = title
                    if deadline:
                        todo.deadline = deadline
                    else:
                        todo.deadline = None
                    todo.save()
                except Todo.DoesNotExist:
                    pass
            
        elif action == 'delete':
            # 삭제
            todo_id = request.POST.get('todo_id')
            
            if todo_id:
                try:
                    Todo.objects.filter(id=todo_id, user=request.user).delete()
                except Exception as e:
                    pass
        
        elif action == 'change_category':  # ← 들여쓰기 수정!
            # 카테고리 변경
            todo_id = request.POST.get('todo_id')
            category = request.POST.get('category')
            
            if todo_id and category:
                try:
                    todo = Todo.objects.get(id=todo_id, user=request.user)
                    todo.category = category
                    todo.save()
                except Todo.DoesNotExist:
                    pass
        
        return redirect('todo_list')
    
    # GET 요청: 할 일 목록 표시
    todos_todo = Todo.objects.filter(user=request.user, category='todo').order_by('-created_at')
    todos_end = Todo.objects.filter(user=request.user, category='end').order_by('-created_at')
    todos_not = Todo.objects.filter(user=request.user, category='not').order_by('-created_at')
    
    context = {
        'todos_todo': todos_todo,
        'todos_end': todos_end,
        'todos_not': todos_not,
    }
    return render(request, 'todo/todo_list.html', context)