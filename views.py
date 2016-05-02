from socketio import socketio_manage
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse
from chat.models import ChatRoom
from chat.sockets import ChatNamespace
from django.shortcuts import render_to_response,render,get_object_or_404,redirect
from django.core.urlresolvers import reverse
from django.contrib import auth
from django.http import HttpResponseRedirect,HttpResponse
from chat.models import UserPro
from django.core.context_processors import csrf
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.core.mail import send_mail
from django.contrib.auth.views import password_reset, password_reset_confirm, password_reset_complete, password_reset_done
from forms import MyRegistrationForm
from django.contrib.auth.models import User

def rooms(request, template="rooms.html"):
    """
    Homepage - lists all rooms.
    """
    context = {"rooms": ChatRoom.objects.all()}

    return render(request,template, context)

def room(request, slug, template="room.html"):
    
    context = {"room":get_object_or_404(ChatRoom, slug=slug)}
    return render(request, template)

def create(request):
    """
    Handles post from the "Add room" form on the homepage, and
    redirects to the new room.
    """
    name = request.POST.get("name")
    if name:
        roomf, created = ChatRoom.objects.get_or_create(name=name)
        return HttpResponseRedirect(reverse('authentic:rooms'))
    return HttpResponseRedirect(reverse('authentic:rooms'))

def reset(request):
    return password_reset(request, template_name='authentic/password_reset_form.html',
                   email_template_name='authentic/password_reset_email.html',
                   subject_template_name='authentic/password_reset_subject.txt',
                   post_reset_redirect = reverse('authentic:reset_done'))

def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(request, template_name='authentic/password_reset_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('authentic:reset_complete'))

def reset_complete(request):
    return password_reset_complete(request,
                            template_name='authentic/password_reset_complete.html');

def reset_done(request):
    return password_reset_done(request,
                        template_name='authentic/password_reset_done.html');

def index(request):
    return render_to_response('authentic/index.html')
    
def register_user(request):
    if request.method == 'POST':
        form = MyRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('authentic:register_success'))
    args = {}
    args.update(csrf(request))

    args['form'] = MyRegistrationForm()
    return render_to_response('authentic/register.html',args)

def register_confirm(request, activation_key):
    
    user_profile = get_object_or_404(UserPro, activation_key=activation_key)
    user = user_profile.user
    if user.is_active:
        return HttpResponseRedirect(reverse('authentic:login'))
    
    user.is_active = True
    user.save()
    return render_to_response('authentic/confirm.html')

def register_success(request):
    return render_to_response('authentic/register_success.html')

# check that user is authenticated or not
def login(request):
    if request.user.is_authenticated():
        #user_profile = get_object_or_404(UserPro, user=request.user)
        return HttpResponseRedirect(reverse('authentic:rooms'))
    c = {}
    c.update(csrf(request))
    return render_to_response('authentic/login.html',c)
    

def auth_view(request):
    
    username=request.POST['username']
    password=request.POST['password']
    user = auth.authenticate(username=username,password=password)

    if user is not None:
            #user_profile = get_object_or_404(UserPro, user=user)
            if user.is_active:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('authentic:rooms'))
            else:
                return render_to_response('authentic/activate.html')
            
    else:
            return HttpResponseRedirect(reverse('authentic:incorrect'))

def loggedin(request):
    user_profile = get_object_or_404(UserPro, user=request.user)
    if request.user.is_authenticated():
        return render_to_response('authentic/loggedin.html',{'userpro':user_profile})
    else:
        return render_to_response('authentic/login.html',{'full_name':request.user.username})

def incorrect(request):
    return render_to_response('authentic/invalid_login.html')
    

def logout(request):
    auth.logout(request)
    return render_to_response('authentic/logout.html')
    
def profile(request,slug):
    return render_to_response('authentic/profile.html')
    return render_to_response('authentic/profile.html')