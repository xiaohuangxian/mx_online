from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})

    def post(self, request):
        return render(request, )


class RegisterView(View):
    def get(self, request):
        return render(request,'register.html',{} )

    def post(self, request):
        return render(request, )
