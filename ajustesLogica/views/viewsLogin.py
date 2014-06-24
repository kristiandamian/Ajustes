from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.admin.forms import AdminAuthenticationForm
from django.template import RequestContext, loader

def loginUsuario(request):
    if request.method == 'POST':    
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if  user is not None and user.is_active :
            login (request,user)
            return HttpResponseRedirect('/ajustes')
        else:
            return renderLogin(request,True)
    else:
        return renderLogin(request,False)
    
def renderLogin(request,ConError):
    template = loader.get_template('login.html')
    context = RequestContext(request, {
        'form': AdminAuthenticationForm,
        'error': ConError,
        })
    return HttpResponse(template.render(context))

def logoutUsuario(request):
    logout(request)
    return HttpResponseRedirect('/ajustes/login')