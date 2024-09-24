# PWS Deployment URL:
http://isaac-jesse-coquetteshop.pbp.cs.ui.ac.id/

<details>
<Summary><b>Assignment 2</b></Summary>
# How I implemented the [assignment checklist](https://pbp-fasilkom-ui.github.io/ganjil-2025/en/assignments/individual/assignment-2)

### Creating a new Django project
First, I created the main directory `coquette_shop` with:
```
mkdir coquette-shop
```

To avoid Python version conflicts and to contain the project, I use a Python virtual environment:
```
python -m venv env
env\Scripts\activate
```

Then, populated a **requirements.txt** file, and then installed them with
```
pip install -r requirements.txt
```

After Django is installed, I initialized the project with
```
django-admin startproject coquette_shop .
```

To test if the project is initialized, I added localhost(127.0.0.1) to the allowed hosts section of `settings.py`, then checked if Django showed the new project screen with

```
python manage.py runserver
```

### Creating an application `main` in the project

To create the 'main' application:
```
python manage.py startapp main
```

### Performing routing in the project so that the application `main` can run
This 'main' app needs to be added to the project directory (coquette_shop, not coquette-shop) settings.py **INSTALLED_APPS** field.

So far, 'main' does not have any html files to display, so I will add one in the templates directory as such:
```
cd main
mkdir templates
nvim main.html
```

I filled the **main.html** file with placeholder fields `{{ application_name }}`, `{{ name }}`, and `{{ class }}` where the 'context' will be supplied by views.py at a later step.

### Creating the Product model in `main` application

Since it was specified that there should be a field `name` with CharField, `price` with IntegerField, and `description` with TextField, I filled `main/models.py` with the following class:

```
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    coquetteness = models.IntegerField()
```

### Creating a function in `views.py` to display the application name , name, and class

Since I already created a template `main.html` with placeholder fields two steps ago, I need to create a function in `main/views.py` that simply shows `main.html` and provides context such as the application name, name, and class:

```
from django.shortcuts import render

def show_main(request):
    context = {
            'application_name': 'coquette-shop',
            'class': 'PBD KKI',
            'name': 'Isaac Jesse Boentoro',
    }
    return render(request, "main.html", context)
```

### Routing the `show_main` function in `views.py` to `urls.py`

I added ` path('', include('main.urls'))` to the `urlpatterns` field in `coquette-shop/urls.py` and
```
from django.urls import path
from main.views import show_main

app_name = 'main'
urlpatterns = [
        path('', show_main, name = 'show_main'),
]
```
to `main/urls.py`

### Performing deployment to PWS

I created a PWS project named coquetteshop, added `isaac-jesse-coquetteshop.pbp.cs.ui.ac.id` to `ALLOWED_HOSTS` in settings.py, then added it as remote and pushed it to PWS.

## Diagram explaining flow from Client request to `urls.py`, `views.py`, `models.py`, and the `html` file

![Diagram](readme_images/diagram.png)

## The use of `git` in software development

git is extremely useful for software developers to be able to track their changes, revert to previous versions of their project if need be, and allows developers to store their projects in remote repositories such as Github or Gitlab, making it possible to collaborate with others easily.

## Why is Django used as the starting point for learning software development?

In my opinion, Django is fairly straightforward to setup, and has an inherent user-friendly syntax because it is built on Python.

## Why is Django called an ORM?

Django is called an ORM because it maps entries in a database to objects in the object oriented programming language (namely, Python). Django in particular does this through the `models.py` file.
</details>

<details>
<Summary><b>Assignment 3</b></Summary>
## Why do we need Data delivery in implementing a platform?

Data delivery is useful to enable asynchronous communication between users of the platform, or between the administrator of the platform and its users. Platforms cannot function effectively as just a static site.

## JSON or XML?
In my opinion, JSON is simply superior. JSON is also more widely used for some reasons such as not needing a dedicated parser, shorter, and not needing closing tags.

## Explaining `is_valid()`
is_valid() is used to validate the user input before saving it to the database. It is not guaranteed that site users will submit the correct format of data, then it is crucial to make sure that the form input is valid before being submitted to the database, potentially preventing errors down the line.

## CSRF Token 
CSRF Tokens are a hidden field that makes sure that the connection between the user's web browser is valid with the website. This prevents Cross-Site Request Forgery attacks, where a malicious website tricks a user's browser into falsely performing actions on another website where they are already authenticated. Without this, it is possible for the user's web browser to be manipulated and submit data to the Django form without their consent.

# How I implemented the [assignment checklist](https://pbp-fasilkom-ui.github.io/ganjil-2025/en/assignments/individual/assignment-3)

### Setting up base template
To avoid code repetition and ease extending the site template, I created a template directory in the root directory and created `base.html`.

To reflect these changes, I then added BASE_DIR / 'templates' in settings.py to the DjangoTemplates DIR field.

### Creating forms
In the 'main' application folder, I created `forms.py` which uses the previously created `Product` model in `models.py`.

```py
from django.forms import ModelForm
from main.models import Product

class ProductEntryForm(ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "description", "coquetteness"]

```

To correctly identify each `Product` model, I added a UUID to the model as such:

```py
class Product(modelsModel):
    ...
   id = models.UUIDField(primary_key = True, default=uuid.uuid4, editable=False)
   ...
```

### Creating the HTML field to use the form
Using codeblocks, I created `create_product.html` that uses the form created earlier, and then displayed the stored models in `main.html` by returning all Products in `views.py` as context.

`create_product.html`
```html
{% extends 'base.html' %} 
{% block content %}
<h1>Add Product</h1>

<form method="POST">
  {% csrf_token %}
  <table>
    {{ form.as_table }}
    <tr>
      <td></td>
      <td> 
        <input type="submit" value="Add Product" />
      </td>
    </tr>
  </table>
</form>

{% endblock %}
```

`main.html`

```html
{% if not products %}
<p>There are no producs.</p>
{% else %}
<table>
  <tr>
    <th>Product Name</th>
    <th>Price</th>
    <th>Description</th>
    <th>Coquetteness</th>
  </tr>

  {% comment %} This is how to display Product data
  {% endcomment %} 
  {% for product in products %}
  <tr>
    <td>{{product.name}}</td>
    <td>{{product.price}}</td>
    <td>{{product.description}}</td>
    <td>{{product.coquetteness}}</td>
  </tr>
  {% endfor %}
</table>
{% endif %}

<br />

<a href="{% url 'main:create_product' %}">
  <button>Add New Product</button>
</a>
{% endblock content %}
```

`views.py`
```py
def show_main(request):
    ...
    return render(request, "main.html", context)
        products = Product.objects.all()
    ...
```
Then, added the actual form to `views.py` and implemented input validation.
`views.py`
```py
def create_product(request):
       form = ProductEntryForm(request.POST or None)
       if form.is_valid() and request.method == "POST":
              form.save()
              return redirect('main:show_main')
       context = {'form': form}
       return render(request, "create_product.html", context)
```


### To access the XML and JSON data from the forms directly, I created 4 functions  (show_json, show_xml, show_json_by_id, show_xml_by_id)

`views.py`

```py

def show_xml(request):
        data = Product.objects.all()
        return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
        data = Product.objects.all()
        return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
        data = Product.objects.filter(pk=id)
        return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
        data = Product.objects.filter(pk=id)
        return HttpResponse(serializers.serialize("json", data), content_type="application/json")
```

## Using Postman to test GET requests:
![postman test](readme_images/postman_1.png)
![postman test](readme_images/postman_2.png)
![postman test](readme_images/postman_3.png)
![postman test](readme_images/postman_4.png)

</details>
<details>
<Summary><b>Assignment 4</b></Summary>
# How I implemented the [assignment checklist](https://pbp-fasilkom-ui.github.io/ganjil-2025/en/assignments/individual/assignment-4)


## Creating the register, log in and log out functions
In `views.py`, I added the following lines:

```py
def register(request):
        form = UserCreationForm()
        if request.method == "POST":
                form = UserCreationForm(request.POST)
                if form.is_valid():
                        form.save()
                        messages.success(request, 'Your account has been successfully created!')
                        return redirect('main:login')
        context = {'form':form}
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
                        # login(request, user)
                        # response = HttpResponseRedirect(reverse("main:show_main"))
                        # response.set_cookie('last_login', str(datetime.datetime.now()))
                        # return response
        else:
                form = AuthenticationForm(request)

        context = {'form':form}
        return render(request, 'login.html', context)
        

def logout_user(request):
        logout(request)
        response = HttpResponseRedirect(reverse('main:login'))
        response.delete_cookie('last_login')
        return response
```

The login and logout functions also use cookies to automatically log-in a user unless specified otherwise. The cookie is then sent as context to `show_main`:

`views.py`
```py
def show_main(request):
...
                'last_login': request.COOKIES['last_login'],
        }
        return render(request, "main.html", context)  
```

Since the `register` function expects a `register.html`, let's make that:
```html
{% extends 'base.html' %} {% block meta %}
<title>Register</title>
{% endblock meta %} {% block content %}

<div class="login">
  <h1>Register</h1>

  <form method="POST">
    {% csrf_token %}
    <table>
      {{ form.as_table }}
      <tr>
        <td></td>
        <td><input type="submit" name="submit" value="Register" /></td>
      </tr>
    </table>
  </form>

  {% if messages %}
  <ul>
    {% for message in messages %}
    <li>{{ message }}</li>
    {% endfor %}
  </ul>
  {% endif %}
</div>

{% endblock content %}
```

This `register.html` file extends to the main template `base.html` for simplicity.

Now to perform routing on all of these new functions, import them to `urls.py` and add them to `urlpatterns`:

`urls.py`
```py
from main.views import (
      ...
      register,
      login_user,
      logout_user,
      ...
)

app_name = 'main'
urlpatterns = [
        ...
        path('register/', register, name='register'),
        path('login/', login_user, name='login'),
        path('logout/', logout_user, name='logout'),
        ...
]
```

Since we want to force users to login before accessing the site, we can add that restriction to the `show_main` function as such:

```py
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def show_main(request):
...
```

## Connecting the `Product` model to each user:

`views.py`
```py
def show_main(request):
        products = Product.objects.filter(user=request.user)
        context = {
        ...
```

`models.py`
```py
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ...
```

This makes each instance of the `Product` model tied to each user, so that only authorized users can view their respective `Product` models.

We also modify `create_product` in `views.py` as such, to modify the `user` field *before* saving it to the database to tie it to the user that created it.

```py
def create_product(request):
       form = ProductEntryForm(request.POST or None)
       if form.is_valid() and request.method == "POST":
              # These lines
              product = form.save(commit=False)
              product.user = request.user
              product.save()
              #
              return redirect('main:show_main')
       context = {'form': form}
       return render(request, "create_product.html", context)
```

## Difference between `HttpResponseRedirect()` and `redirect()`

`HttpResponseRedirect()`:

Usage: Redirects to a URL.
Syntax: Requires a URL string.

`redirect()`:

Usage: A shortcut for redirection.
Syntax: Can take a URL, a view name, or a view name with arguments.

## How is `Product` model linked with `User`?

The `Product` model is linked to each user via a foreign-key approach:

`models.py`

```py
class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
```

And when each Product is created via `create_product`, it is linked to the user:

`views.py`
```py
def create_product(request):
       form = ProductEntryForm(request.POST or None)
       if form.is_valid() and request.method == "POST":
              product = form.save(commit=False)
              product.user = request.user
```

## How does Django remember logged in users? What are the other uses of cookies and are all of them safe?

Django uses sessions and cookies stored on the user's browser to remember logged in users. 

Cookies can be used for other uses, such as:
- User settings
- Tracking and analytics
- Authentication tokens

Not all cookies are inherently safe, and the safety of said cookies depends on how they are implemented and managed.

- Cookies should be marked as secure to enable that they are only sent over HTTPS connections.

- Marking them as HttpOnly prevents client scripts from accessing them, reducing the risk of XSS (Cross site scripting) attacks.

- The SameSite attribute helps prevent cross-site request forgery attacks

- Cookies should have a set expiration date

- Cookies should not be used to store sensitive information directly inside. Instead, use session IDs or tokens that reference server-side data.

## Difference between authentication and authorization, and what happens when a user logs in.

Authentication: Verifying the identity of a user (ensuring they are who they claim to be)

Django implements this with built in views and forms such as `LoginView`, `LogoutView`, and `AuthenticationForm`

Authorization: Determining what an authenticated user is allowed to do based on its roles and permissions.

Django implements this via the `User` model and `Permissions`.

What hapepns when a user logs in?
1. User submits Login form
2. Authentication
- Django checks if the provided credentials are in the database
- The user is then authenticated
3. Session creation:
- Django creates a session for the authenticated user
- Session ID is stored as a cookie on the user's browsesr
4. User Object:
- Authenticated users are associated with a `User` object, accessible via `request.user` in `views.py`.
5. Redirection
- The user is then redirected to `main.html`

</details>