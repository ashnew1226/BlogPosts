from django.contrib import messages
from django.shortcuts import render,HttpResponse,redirect
from . models import Contact
from blog.models import Post
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
# HTML Pages
def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        desc =request.POST['desc']
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(desc)<4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact=Contact(name=name, email=email, phone=phone, desc=desc)
            contact.save()
            messages.success(request, "Your message has been successfully sent")
    return render(request, "home/contact.html")
    
def search(request):
    query = request.GET['query']
    # allPosts = Post.objects.all()
    if len(query) > 78 :
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
        
        
    if allPosts.count() == 0:
        messages.error(request, "No search results found. Please refine your query")
    param = {'allPosts': allPosts, 'query': query}
    # print(query)
    return render(request, 'home/search.html', param)
# Aunthentication APIs
def handleSignup(request):
    
    if request.method == 'POST':
        #get the the parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        #checks for errorneos input
        if len(username) > 10:
            messages.error(request, "username must be under 10")
            return redirect('home')
        if not username.isalnum():
            messages.error(request, "username should only contain letters and numbers")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request, "password do not match")
            return redirect('home')

        # # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, "Your account has beed successfully created")
        return redirect('home')
    else:
        return HttpResponse('404 - not found')
    
def handleLogin(request):
    if request.method == "POST":
        Loginusername = request.POST['loginusername']
        Loginpassword = request.POST['loginpassword'] 
         
        user = authenticate(username=Loginusername, password=Loginpassword)
        
        if user is not None:
            login(request, user)
            messages.success(request, "successfully logged in")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials, Please try again")
            return redirect('home')
        
    return HttpResponse('404 - Not found')

def handleLogout(request):
    # if request.method == 'POST':
    logout(request)
    messages.success(request, "Successfully Logged out")
    return redirect('home')
   