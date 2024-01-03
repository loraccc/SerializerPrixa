from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import item,Person,Product,CartItem
from .serializers import itemSerializer
from .forms import UserCreationForm,AuthenticationForm,RegistrationForm,LoginForm
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail


# Create your views here.
#APIView

class ItemListAPIView(ListAPIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = item.objects.all()
    serializer_class = itemSerializer  # Set the serializer class here

    def post(self, request):
        serializer = itemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ItemDetail(LoginRequiredMixin,APIView):
    # @login_required(login_url='/login/')   
    login_url = 'users/login.html' 
    def get_object(self, pk):
        
        return get_object_or_404(item, pk=pk)
    login_url = 'users/login.html'
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
    login_url = 'users/login.html'
    context_object_name = 'my_custom_name'   #overriding the context name of object_list
    paginate_by = 2  # Specify the number of items per page
    

    def get_queryset(self):
        # print("Number of pages:", self.object_list.paginator.num_pages)
        return item.objects.all().order_by('id')  

class itemDetail(LoginRequiredMixin, DetailView):
    model = item
    template_name = 'item_detail.html'
    login_url = 'users/login.html'  

class itemCreate(LoginRequiredMixin, CreateView):
    model = item
    template_name = 'item_form.html'
    fields = ['name', 'desc']
    login_url = 'users/login.html'  

    def form_valid(self, form):
        form.instance.owner = self.request.user.person
        return super().form_valid(form)

class itemUpdate(LoginRequiredMixin, UpdateView):
    model = item
    template_name = 'item_form.html'
    fields = ['name', 'desc']
    login_url = 'users/login.html'  

class itemDelete(LoginRequiredMixin, DeleteView):
    model = item
    template_name = 'item_confirm_delete.html'
    success_url = reverse_lazy('item-list')
    login_url = 'users/login.html'  


class UserRegisterView(View):
    template_name = 'users/register.html'

    def get(self, request):
        form = RegistrationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            person = Person.objects.create(user=user)
            person.save()
            print("CREDENTIALS OF PERSON :",person)
            subject = 'User Created Successfully'
            message = f'Congratulations! A user named {{person}} has been created .'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['carolacharya1@gmail.com']

            send_mail(subject, message, from_email, recipient_list)
            auth_login(request, user)
            return redirect('product_list')
        return render(request, self.template_name, {'form': form})

class UserLoginView(LoginView):
    template_name = 'users/login.html'

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
            print(f'LOGIN_URL: {settings.LOGIN_URL}')
            return redirect('product_list')
        else:
            form = LoginForm(request.POST)
            return render(request, self.template_name, {'form': form, 'login_failed': True})

# ECOMMERCE 
# @login_required(login_url='/users/login/')
def product_list(request):
    products = Product.objects.all()
    return render(request, 'ecom/index.html', {'products': products})
 
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'ecom/cart.html', {'cart_items': cart_items, 'total_price': total_price})
 
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product, 
                                                       user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')
 
def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()

    return redirect('view_cart')