from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import item,Person
from rest_framework import status
from .serializers import itemSerializer
from rest_framework.views import APIView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import UserCreationForm,AuthenticationForm,RegistrationForm,LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#APIView

class ItemListAPIView(APIView):
    @login_required(login_url='login/')
    def get(self, request):
        items = item.objects.all()
        serializer = itemSerializer(items, many=True)
        return Response(serializer.data)

    @login_required(login_url='login/')
    def post(self, request):
        serializer = itemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ItemDetail(APIView):
    @login_required(login_url='/login/')    
    def get_object(self, pk):
        
        return get_object_or_404(item, pk=pk)
    @login_required(login_url='login/')
    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = itemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class itemList(LoginRequiredMixin, ListView):
    model = item
    template_name = 'item_list.html'
    login_url = '/login/'  

class itemDetail(LoginRequiredMixin, DetailView):
    model = item
    template_name = 'item_detail.html'
    login_url = '/login/'  

class itemCreate(LoginRequiredMixin, CreateView):
    model = item
    template_name = 'item_form.html'
    fields = ['name', 'desc']
    login_url = '/login/'  

    def form_valid(self, form):
        form.instance.owner = self.request.user.person
        return super().form_valid(form)

class itemUpdate(LoginRequiredMixin, UpdateView):
    model = item
    template_name = 'item_form.html'
    fields = ['name', 'desc']
    login_url = '/login/'  

class itemDelete(LoginRequiredMixin, DeleteView):
    model = item
    template_name = 'item_confirm_delete.html'
    success_url = reverse_lazy('item-list')
    login_url = '/login/' 


class UserRegisterView(View):
    template_name = 'register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            person = Person.objects.create(user=user)
            person.save()
            print('new user is ', person)
            auth_login(request, user)
            return redirect('get_data')

        return render(request, self.template_name, {'form': form})

class UserLoginView(View):
    template_name = 'login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            print('user is : ', user)
            return redirect('get_data')
        else:
            form = LoginForm(request.POST)
            return render(request, self.template_name, {'form': form, 'login_failed': True})

