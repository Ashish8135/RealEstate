from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from contacts.models import Contact


# Create your views here.


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')


def register(request):
    if request.method == 'POST':
        # here user should be register itself with credentials
        # messages.error(request,"Testing error message")
        # here we get the form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # if password matches then
        if password == password2:
            # check username is exists or not
            if User.objects.filter(username=username).exists():
                # if user exists show error
                messages.error(request, 'Username already exists')
                return redirect('register')
            else:
                # continue to check email is exists or not
                if User.objects.filter(email=email).exists():
                    # if user exists show error
                    messages.error(request, 'Email already exists')
                    return redirect('register')
                else:
                    # everything is good and looks forward this form i.e fill all fields
                    user = User.objects.create_user(username=username, email=email, password=password,
                                                    first_name=first_name, last_name=last_name)
                    # login after user registration in the form
                    # auth.login(request, user)
                    # # show message to
                    # messages.success(request,'You are now logged in')
                    # return  redirect('index')
                    user.save()
                    messages.success(request, 'You are Successfully Registered and can log in')
                    return redirect('login')

        else:
            messages.error(request, 'password do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')


def dashboard(request):
    # if request.method == 'POST':
    #     # here register should be login with credentials
    #     return redirect('login')
    # else:
    # from RealEstate.contacts.models import Contact
    user_contact = Contact.objects.order_by('contact_date').filter(user_id=request.user.id)
    context = {
        'contact': user_contact
    }
    return render(request, 'accounts/dashboard.html', context)


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')
