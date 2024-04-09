from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from django import forms
from .models import Contact
from .models import Products
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated 
from django.contrib.auth import authenticate
from .renderers import UserRenderer


from rest_framework.views import APIView
from django.http import JsonResponse
from .serializers import ContactSerializer,UserRegistrationSerializer,UserLoginSerializer,UserProfileSerializer
import requests
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import ContactForm

# Form Validations


# Create your views here.
def index(request):
    return render(request, 'shop/index.html')

def about(request):
    return render(request, 'shop/about.html')
def contact(request):

    request_type = request.POST.get('requestType')
    success = False
    form = None
    alert_message = ""
    
    if request.method == 'GET':
        request_type = request.GET.get('requestType')
        name = request.GET.get('name', None)
        emailAddress = request.GET.get('emailAddress',None)
        message = request.GET.get('textMessage',None)
        
        if name and emailAddress and message:
            # form_data = {'name': name, 'emailAddress': emailAddress,'message': message}
            # form = ContactForm(form_data)
            form = ContactForm({'name': name, 'emailAddress': emailAddress, 'message': message})
            
            try:
                if form.is_valid():
                    form.save()
                    success = True
                    alert_message = "Data has been stored successfully"
         
            except ValidationError as e:
        
                alert_message = str(e)


    if request.method == 'POST':

        # if request_type == 'GET':
        #         request_type = request.GET.get('requestType')
        #         name = request.GET.get('name', None)
        #         emailAddress = request.GET.get('emailAddress',None)
        #         message = request.GET.get('textMessage',None)
        #         form_data = {'name': name, 'emailAddress': emailAddress,'message': message}

        #         form = ContactForm(form_data)
                
        #         try:
        #             if form.is_valid():
        #                 form.save()
        #                 success = True
        #                 alert_message = "Data has been stored successfully"
        #                 print(alert_message)
                
        #         except ValidationError as e:
        #             print(e)
        #             alert_message = str(e)



        if request_type == 'POST':
            # form = ContactForm(form_data)
            name = request.POST.get('name')
            emailAddress = request.POST.get('emailAddress')
            message = request.POST.get('textMessage')
            form_data = {'name': name, 'emailAddress': emailAddress,'message': message}
            
            form = ContactForm(form_data)
            try:
                if form.is_valid():
                    form.save()
                    success = True
                    alert_message = "Data has been stored successfully"
                    print(alert_message)
                
            except ValidationError as e:
                print(e)
                alert_message = str(e)
            
        # storeContact = Contact(
        #     name = username,
        #     emailAddress = emailAddress,
        #     message = message
        # )

        # storeContact.save()

        # # print("Store ID :: " + str(storeContact.id))

        # if storeContact.pk:
        #     # alert = {
        #     #     'isSuccess': True,
        #     #     'message': 'Feedback has been recorded successfully'
        #     # }
        #     success = True
        #     msgResponse = "Feedback has been recorded successfully"
        # else:
        #     success = False
        #     msgResponse = "Internal Server Error" 
        #     # alert = {
        #     #     'isSuccess': False,
        #     #     'message': 'Internal Server Error'
        #     # }

    # return render(request, 'shop/contact.html', {'success': success, 'message':msgResponse})
    return render(request, 'shop/contact.html',{'form': form,'alert_message': alert_message, 'success': success})

def contact_api(request):
    if request.method == 'GET':
        contacts = Contact.objects.all()
        serializer = ContactSerializer(contacts, many=True)
        return JsonResponse(serializer.data, safe=False)
    
def contactData(request):
    if request.method == 'GET':
        contactDataApi = 'http://127.0.0.1:8000/shop/api/contacts/'
        response = requests.get(contactDataApi)

        if response.status_code == 200:
            data = response.json()
            return render(request, 'shop/contactdata.html', {'data': data})
        else:
            return render(request, 'shop/contactdata.html')
    
        
def search(request):
    return render(request, 'shop/search.html')

def productView(request):
    return render(request, 'shop/productview.html')

def checkout(request):
    return render(request, 'shop/checkout.html')

def tracker(request):
    return render(request, 'shop/tracker.html')

def login(request):
    if request.method == 'POST':
        emailAddress = request.POST.get('email')
        password = request.POST.get('pswd')
        print(emailAddress)
        print(password)

    return render(request, 'shop/login.html')
def products(request):

    isSuccess = False
    alert = None

    print(request)

    if request.method == 'POST':

        if 'submit_edit_product' in request.POST:
            print("Inside Edit If Statement")
            updated_pId = int(request.POST.get('editPId'))
            updated_pname = request.POST.get('editPName')
            updated_category = request.POST.get('editPCat')
            updated_subcategory = request.POST.get('editPSubCat')
            updated_desc = request.POST.get('editPDesc')
            updated_price = request.POST.get('editPrice')
            updated_pub_date = request.POST.get('editPDate')
            updated_image = request.FILES.get('editPImage')
            updateQuery = get_object_or_404(Products, id=updated_pId)
            
            print(updateQuery)

            updateQuery.product_name = updated_pname
            updateQuery.category = updated_category
            updateQuery.subcategory = updated_subcategory
            updateQuery.desc = updated_desc
            updateQuery.price = updated_price
            updateQuery.pub_date = updated_pub_date
            updateQuery.image = updated_image

            try:
                updateQuery.save()
            except Exception as e:
                print(e )
            isSuccess = True
            alert = "Product Data has been stored successfully"

        elif 'submit_add_product' in request.POST:
            product_name = request.POST.get('pName')
            category = request.POST.get('pCat')
            subcategory = request.POST.get('pCat')
            desc = request.POST.get('pDesc')
            price = request.POST.get('pPrice')
            pub_date = request.POST.get('pDate')
            image = request.FILES.get('pImage')
            print(f'Initial Image Stored Value : {image} ')

            print(product_name,image)

            addProduct = Products(
            product_name=product_name,
            category=category,
            subcategory=subcategory,
            desc=desc,
            price=price,
            pub_date=pub_date,
            image=image
        )
            try:
                addProduct.save()

                isSuccess = True
                alert = "Product Data has been stored successfully"
            except Exception as e:
                isSuccess = False   
                print(e)
                alert = f"An error occurred: {e}"

    productsList = Products.objects.all()
    # print(productsList)

    return render(request, 'shop/products.html', {'productsList': productsList, 'isSuccess': isSuccess, 'alert': alert})

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):

    def post(self, request, format=None):    
        # return render(request, 'shop/registration.html')
        serializer = UserRegistrationSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)

            return Response({'token': token, 'msg': 'Reg Success'})
        
    
    def get(self, request, format=None):
        
        return render(request, 'shop/registration.html')


def registration(request):

    if request.method == 'POST':

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        emailAddress = request.POST.get('emailAddress')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')
        username = request.POST.get('username')

        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            password = password,
            confirm_password = confirm_password,
            emailAddress = emailAddress,
            username = username
        )

        user.set_password(password)
        user.save()
       


        # user.save()
        print("User Created")
        return render(request, 'shop/registration.html', {'msg': 'Reg Successful'})

    return render(request, 'shop/registration.html')

def jsoneg(request):
    jsonData = [{'Name':'Roshan Bhatia','Age':21,'Passion':'Coding,Photography,Military Aviation'},{'Name':'Tom Bhatia','Age':21,'Passion':'Aerodynamics,Military Aviation'}]
    
    return render(request, 'shop/jsoneg.html', context = {'jsonData': jsonData})
# class UserLoginView(APIView):
#     def post(self,request,format=None):
#         serializer = UserLoginSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             email = serializer.data.get('email')
#             password = serializer.data.get('password')
#             user = authenticate(email=email, password=password)

#             if user is not None:
#                 return Response({'msg':'Login Success'})
#             else:
#                 return Response({'errors': {'non_field_errors' : ['Email Or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
#     def get(self,request,format=None):
#         return render(request, 'shop/login.html')

class UserLoginView(APIView):

    def get(self, request, format=None):
        return render(request, 'shop/login.html')   

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Authentication successful
                token = get_tokens_for_user(user)

                return Response({'token':token,'msg': 'Login Success'})
            else:
                # Authentication failed
                return Response({'errors': {'non_field_errors': ['Email or Password is not valid']}}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Serializer is not valid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

class UserChangePasswordView(APIView):
    pass


def custom_404_view(request, exception):
    return render(request, '404.html', status=404)
    