from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from user.help import login_required
from user.forms import RegisterForm
from user.models import User


def register(request):
    if request.method =='POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user=form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'error': form.errors})

    return render(request, 'register.html')

def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return render(request, 'login.html',{'error':'用户不存在'})
        else:
            if check_password(password,user.password):
                request.session['uid'] = user.id
                request.session['nickname'] = user.nickname
                return redirect('user/info')
            else:
                return render(request, 'login.html',{'error':'密码错误'})
    return  render(request, 'login.html')

def logout(request):
    return render(request, 'login.html')
@login_required
def user_info(request):
    uid = request.session['uid']
    user = User.objects.get(id=uid)
    return render(request, 'user_info.html', {'user':user})