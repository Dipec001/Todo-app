from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Todo, TodoList
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import login, authenticate


# Create your views here.
def index(request):
    return render(request, 'index.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username,email=email,password=password)

                # Check if there are session todos
                if 'todos' in request.session:
                    session_todos = request.session.get('todos', [])
                    if session_todos:
                        user = authenticate(request, username=username, password=password)
                        if user:
                            # Create a new todo list for the user
                            todo_list = TodoList.objects.create(title="Session Todo List", user=user)

                            # Create Todo objects and associate with the new todo list
                            for title in session_todos:
                                Todo.objects.create(title=title, user=user, todolist=todo_list)

                            # Clear session todos
                            del request.session['todos']
                            request.session.modified = True
                
                
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')
        else:
            messages.info(request, 'Password Not The Same')
            return redirect('register')

    return render(request,'register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            # Check if there are session todos
            if 'todos' in request.session:
                session_todos = request.session.get('todos', [])
                if session_todos:
                    # Create a new todo list for the user
                    todo_list = TodoList.objects.create(title="Session Todo List", user=user)

                    # Create Todo objects and associate with the new todo list
                    for title in session_todos:
                        Todo.objects.create(title=title, user=user, todolist=todo_list)

                    # Clear session todos
                    del request.session['todos']
                    request.session.modified = True

            return redirect('/')
        else:
            messages.info(request, "Invalid email or password")
            return redirect('login')

    return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


def add_todo(request):
    if request.method == 'POST':
        title = request.POST['title']
        todolist_id = request.POST.get('todolist_id')  # Get the todolist_id from the form
        user = request.user

        if title:
            if user.is_authenticated:
                if todolist_id:
                    # User is adding to an existing TodoList
                    todo_list = TodoList.objects.filter(id=todolist_id, user=user).first()
                else:
                    # User is adding to a new TodoList
                    todo_list = TodoList.objects.create(title="New Todo List", user=user)

                # Associate the new todo with the user's TodoList
                Todo.objects.create(title=title, user=user, todolist=todo_list)
                messages.success(request, "Todo added successfully.")
            else:
                # Unauthenticated users, add to session todos
                if 'todos' not in request.session:
                    request.session['todos'] = []
                request.session['todos'].append(title)
                request.session.modified = True
                messages.success(request, "Great, we've created a list for you. You should save your list so you don't forget it.")

        return redirect('todolist:index')
    return HttpResponse("Invalid request")

def delete_session_todo(request, index):
    index = int(index)  # Convert index to integer
    if 'todos' in request.session:
        session_todos = request.session.get('todos', [])
        if 0 <= index < len(session_todos):
            del session_todos[index]
            request.session['todos'] = session_todos
        else:
            messages.error(request, "Todo not found or index out of range")
    return redirect('todolist:index')  # Redirect back to the todos page


def clear_session_todos(request):
    if 'todos' in request.session:
        del request.session['todos']
    return redirect('todolist:index')


@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']

        if name != user.username:
            if User.objects.filter(username=name).exclude(pk=user.pk).exists():
                messages.error(request, 'Username already in use by another user.')
            else:
                user.username = name
                user.save()
                messages.success(request, 'Username changed successfully')

        if email != user.email:
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                messages.error(request, 'Email already in use by another user.')
            else:
                user.email = email
                user.save()
                messages.success(request, 'Email changed successfully')

        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password and new_password == confirm_password:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password changed successfully')
        elif new_password and new_password != confirm_password:
            messages.error(request, 'Password and confirm password do not match.')

    return render(request, 'profile.html', {'user': user})


def manage_lists(request):
    user = request.user
    todolists = TodoList.objects.filter(user=user)
    context = {'todolists': todolists}
    return render(request, 'managelists.html', context)

def todolist_detail(request, todolist_id):
    todolist = get_object_or_404(TodoList, id=todolist_id, user=request.user)
    todos = todolist.todo_set.all()  # Retrieve all todos associated with the todo list
    context = {'todolist': todolist, 'todos': todos}
    return render(request, 'todolist.html', context)


def create_todolist(request):
    user = request.user
    todo_list = TodoList.objects.create(title="New Todo List", user=user)
    messages.success(request, "New TodoList created successfully.")
    return redirect('todolist:manage_lists')


def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    
    todo.delete()
    messages.success(request, "Todo deleted successfully.")

    return redirect('todolist:index')  # Redirect back to the todos page

def update_todolist_title(request, todolist_id):
    todolist = get_object_or_404(TodoList, id=todolist_id, user=request.user)

    if request.method == 'POST':
        new_title = request.POST['new_title']
        if new_title:
            todolist.title = new_title
            todolist.save()
            return redirect('todolist:manage_lists')

    return render(request, 'manage_lists.html')  # Render the same template if not a POST request

def delete_todolist(request, todolist_id):
    todolist = get_object_or_404(TodoList, id=todolist_id, user=request.user)

    if request.method == 'POST':
        todolist.delete()
        return redirect('todolist:manage_lists')
