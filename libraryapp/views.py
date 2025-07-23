from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .form import *
from django.contrib.auth.models import User,auth
from datetime import timedelta
from django.db.models import Q



# Create your views here.
def home(request):
    return render(request,'home.html')

def addbookfn(request):
    if request.method=='POST':
     form=bookform(request.POST,request.FILES)
     if form.is_valid():
        form.save()
        return redirect('/addbook')
    else:
       form=bookform()
       return render(request,'addbook.html',{'form':form})

def viewbooksfn(request):
   x=book.objects.all()
   y=Category.objects.all()
   return render(request,'viewbooks.html',{'book':x,'ctgry':y})

def categorydisplayfn(request,c_id):
   x=book.objects.filter(id=c_id)
   return render(request,'categorydisplay.html',{'cat':x})

def membersviewfn(request):
   return render(request,'members.html')

def registeruserfn(request):
   return render(request,'register.html')

def saveuserfn(request):
   a=request.POST['username']
   b=request.POST['firstname']
   c=request.POST['lastname']
   d=request.POST['email']
   e=request.POST['password']
   f=request.POST['cpassword']
   if e==f:
      if User.objects.filter(username=a).exists():
        return render(request,'register.html',{'wrong':'Username already taken'})
      elif User.objects.filter(email=d).exists():
        return render(request,'register.html',{'wrong':'Email ID already taken'})
      else:
        User.objects.create_user(username=a,first_name=b,last_name=c,email=d,password=e)
        return redirect('/')
   else:
        return render(request,'saveuser.html',{'wrong':'incorrect password'})


def loginfn(request):
   if request.method == 'POST':
      a = request.POST['username']
      e = request.POST['password']
      remember=request.POST.get('remember')
      x = auth.authenticate(username=a, password=e)
      if x:
         auth.login(request, x)
         if remember:
            request.session.set_expiry(timedelta(days=7))
         else:
            request.session.set_expiry(0)

         return redirect('/')
      else:
         return render(request, 'login.html', {'error': 'invalid username or password'})
   else:
      return render(request, 'login.html')
   

def forgotpasswordfn(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        newpass = request.POST['newpass']
        confirmpass = request.POST['confirmpass']

        user = User.objects.filter(username=username, email=email).first()

        if user:
            if newpass == confirmpass:
                user.set_password(newpass)
                user.save()
                return redirect('/login?msg=reset_success')

            else:
                return render(request, 'forgotpassword.html', {'invalid': 'Passwords do not match'})
        else:
            return render(request, 'forgotpassword.html', {'invalid': 'Invalid username or email'})
    
    else:
        return render(request, 'forgotpassword.html')

def logoutfn(request):
   auth.logout(request)
   return redirect('/')

def viewdetailfn(request,v_id):
   b=book.objects.get(id=v_id)
   return render(request,'viewdetail.html',{'view':b})

def editbookfn(request,e_id):
   if request.method=='POST':
      b=book.objects.get(id=e_id)
      f=bookform(request.POST,request.FILES,instance=b)
      if f.is_valid():
         f.save()
         return redirect('/viewdetail')  
   else:
      b=book.objects.get(id=e_id)
      f=bookform(instance=b)
      return render(request,'addbook.html',{'form':f}) 

def deletebookfn(request,d_id):
   if request.method=='POST':
      b=book.objects.get(id=d_id)
      b.delete()
      return redirect('/viewbooks')
   else:
      b=book.objects.get(id=d_id)
      return render(request,'delete.html',{'del':b})
   
def searchfn(request):
   s=request.GET['srch']
   f=book.objects.filter(Q(name__icontains=s) |Q(ctgry__name__icontains=s)|Q(author__icontains=s))
   return render(request,'search.html',{'search':f})

