from django.shortcuts import render, redirect, reverse
from main.forms import ProductEntryForm
from main.models import Product
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from decimal import Decimal, InvalidOperation
import json

# Create your views here.

@login_required(login_url='/login')
def show_main(request):
    products = Product.objects.filter(user=request.user)
    context = {
        'application_name': 'coquette-shop',
        'class': 'PBD KKI',
        'name': request.user.username,
        'products': products,
        'last_login': request.COOKIES['last_login'],
    }
    return render(request, "main.html", context)

def create_product(request):
    form = ProductEntryForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        product = form.save(commit=False)
        product.user = request.user
        product.save()
        return redirect('main:show_main')
    context = {'form': form}
    return render(request, "create_product.html", context)

def show_xml(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Product.objects.filter(user=request.user)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Product.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has successfully been created!')
            return redirect('main:login')
    context = {'form': form}
    return render(request, 'register.html', context)

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                response = HttpResponseRedirect(reverse("main:show_main"))
                response.set_cookie('last_login', str(datetime.datetime.now()))
                return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")
    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

def edit_product(request, id):
    product = Product.objects.get(pk=id)
    form = ProductEntryForm(request.POST or None, instance=product)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))
    context = {'form': form}
    return render(request, "edit_product.html", context)

def delete_product(request, id):
    product = Product.objects.get(pk=id)
    product.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

@csrf_exempt
@require_POST
def create_product_ajax(request):
    try:
        data = json.loads(request.body)
        
        # Strip HTML tags and remove leading/trailing whitespace
        name = strip_tags(data.get("name", "")).strip()
        description = strip_tags(data.get("description", "")).strip()
        
        # Convert price to Decimal
        try:
            price = Decimal(data.get("price", "0"))
        except InvalidOperation:
            return JsonResponse({"status": "error", "message": "Invalid price format"}, status=400)

        # Convert coquetteness to integer
        try:
            coquetteness = int(data.get("coquetteness", "0"))
        except ValueError:
            return JsonResponse({"status": "error", "message": "Invalid coquetteness format"}, status=400)

        # Print debug information
        print(f"Received data: {data}")
        print(f"Processed name: {name}")
        print(f"Processed description: {description}")
        print(f"Processed price: {price}")
        print(f"Processed coquetteness: {coquetteness}")

        product = Product.objects.create(
            name=name,
            price=price,
            coquetteness=coquetteness,
            description=description,
            user=request.user
        )
        return JsonResponse({"status": "success", "id": product.id}, status=201)
    except json.JSONDecodeError:
        return JsonResponse({"status": "error", "message": "Invalid JSON in request body"}, status=400)
    except Exception as e:
        print(f"Error creating product: {str(e)}")
        return JsonResponse({"status": "error", "message": str(e)}, status=500)

def get_products_ajax(request):
    data = Product.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
def create_product_flutter(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        new_product = Product.objects.create(
            user=request.user,
            name=data["name"],
            price=int(data["price"]),
            coquetteness=int(data["coquetteness"]),
            description=data["description"]
        )

        new_product.save()

        return JsonResponse({"status": "success"}, status=200)
    else:
        return JsonResponse({"status": "error"}, status=401)