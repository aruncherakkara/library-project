from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from .form import *
from django.contrib.auth.models import User,auth,Group
from datetime import timedelta
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils import timezone
from django.urls import reverse
from django.contrib import messages





def home(request):
    is_librarian_or_admin = False
    if request.user.is_authenticated:
        if request.user.is_superuser or request.user.groups.filter(name='Librarian').exists():
            is_librarian_or_admin = True

    return render(request, 'home.html', {
        'is_librarian_or_admin': is_librarian_or_admin
    })
@login_required
def addbookfn(request):
    if request.method == "POST":
        form = bookform(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)

            
            book.added_by = request.user  

            
            if not hasattr(book, "available_copies") or book.available_copies is None:
                book.available_copies = 1

            book.save()
            messages.success(request, f"Book '{book.name}' added successfully.")
            return redirect('/viewbooks')  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = bookform()
    return render(request, "addbook.html", {"form": form})



def viewbooksfn(request):
    x = Book.objects.all()
    y= Category.objects.all()
    return render(request, 'viewbooks.html', {'book': x,'category':y })

def categorydisplayfn(request, c_id):
    x = Book.objects.filter(category_id=c_id)
    y = Category.objects.get(id=c_id)
    return render(request, 'categorydisplay.html', {
        'cat_books': x,
        'category': y
    })
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

@login_required
def viewdetailfn(request, e_id):
    b = get_object_or_404(Book, id=e_id)
    is_librarian = request.user.is_superuser or request.user.groups.filter(name='Librarian').exists()
    return render(request, 'viewdetail.html', {'view': b, 'is_librarian': is_librarian})

@login_required
def editbookfn(request, e_id):
    if not (request.user.is_superuser or request.user.groups.filter(name='Librarian').exists()):
        return render(request, 'Access_denied.html')

    b = get_object_or_404(Book, id=e_id)

    if request.method == 'POST':
        f = bookform(request.POST, request.FILES, instance=b)
        if f.is_valid():
            f.save()
            return redirect('/viewbooks')
    else:
        f = bookform(instance=b)
    return render(request, 'addbook.html', {'form': f})


@login_required
def deletebookfn(request, d_id):
    if not (request.user.is_superuser or request.user.groups.filter(name='Librarian').exists()):
        return render(request, 'Access_denied.html')

    b = get_object_or_404(Book, id=d_id)

    if request.method == 'POST':
        b.delete()
        return redirect('/viewbooks')
    else:
        return render(request, 'delete.html', {'del': b})

   
def searchfn(request):
   s=request.GET['srch']
   f=Book.objects.filter(Q(name__icontains=s) |Q(category__name__icontains=s)|Q(author__icontains=s))
   return render(request,'search.html',{'search':f})

@login_required
def adminpanelfn(request):
    if not (request.user.is_superuser or request.user.groups.filter(name='Librarian').exists()):
        return HttpResponseForbidden('Access denied')

    total_books = Book.objects.count()
    total_users = User.objects.count()

    try:
        librarian_group = Group.objects.get(name='Librarian')
        total_librarians = librarian_group.user_set.count()
    except Group.DoesNotExist:
        total_librarians = 0  

    categories = Category.objects.all() 
    users = User.objects.all()
    languages = Language.objects.all()

    return render(request, 'adminpanel.html', {
        'total_books': total_books,
        'total_users': total_users,
        'total_librarians': total_librarians,
        'categories': categories,   
        'users': users,
        'languages': languages,             
        'librarian_group': librarian_group if 'librarian_group' in locals() else None
    })


@login_required
def profilefn(request):
    profile = Profile.objects.get(user=request.user)

    borrowed_books = Borrow.objects.filter(user=request.user)

    added_books = None
    if request.user.is_superuser or request.user.groups.filter(name="Librarian").exists():
        added_books = Book.objects.filter(added_by=request.user)

    return render(request, 'profile.html', {
        'profile': profile,
        'borrowed_books': borrowed_books,
        'added_books': added_books
    })

    
@login_required
def completeprofilefn(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        f = ProfileForm(request.POST, request.FILES, instance=profile)  
        if f.is_valid():
            f.save()
            return redirect('/profile')   
    else:
        f = ProfileForm(instance=profile)

    return render(request, 'completeprofile.html', {'fm': f})

def is_librarian_or_admin(user):
    return user.is_superuser or user.groups.filter(name='Librarian').exists()


@login_required
def librarian_borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BorrowForm(request.POST)
        if form.is_valid():
            if book.available_copies > 0: 
                borrow = form.save(commit=False)
                borrow.book = book
                if not borrow.user:
                    borrow.user = request.user
                borrow.borrow_date = timezone.now()
                borrow.save()

                book.available_copies -= 1
                book.save()

                messages.success(request, f"{borrow.user.username} borrowed {book.name}")
            else:
                messages.error(request, "No copies available for this book.")
            return redirect('viewdetail', e_id=book.id)
    else:
        form = BorrowForm()

    return render(request, "borrow_book.html", {"form": form, "book": book})

@login_required
def librarian_return_book(request, borrow_id):
    borrow = get_object_or_404(Borrow, id=borrow_id)

    if not borrow.is_returned:
        borrow.return_date = timezone.now()
        borrow.save()

        # Increase available copies
        borrow.book.available_copies += 1
        borrow.book.save()

        messages.success(request, f"Book '{borrow.book.name}' returned successfully!")
    else:
        messages.warning(request, "This book has already been returned.")

    return redirect('/librarian_borrows', e_id=borrow.book.id)


@login_required
def all_borrowsfn(request):
    if not is_librarian_or_admin(request.user):
        return render(request, 'Access_denied.html')

    borrows = Borrow.objects.select_related('book', 'user').all()
    return render(request, 'all_borrows.html', {'borrows': borrows})

@login_required
def borrow_book(request, book_id):
    
    if not request.user.is_superuser:
        messages.error(request, "Only librarians can borrow books.")
        return redirect('viewdetail', e_id=book_id)

    book = get_object_or_404(Book, id=book_id)

    if request.method == "POST":
        form = BorrowForm(request.POST)
        if form.is_valid():
            if book.available_copies > 0:
                borrow = form.save(commit=False)
                borrow.book = book
                borrow.borrow_date = timezone.now()
                borrow.save()

                
                book.available_copies -= 1
                if book.available_copies < 0:
                    book.available_copies = 0 
                book.save()

                messages.success(request, f"{borrow.user.username} borrowed '{book.name}'.")
            else:
                messages.error(request, f"No copies of '{book.name}' left.")
            return redirect('viewdetail', e_id=book.id)
    else:
        
        form = BorrowForm(initial={'book': book})

    return render(request, "borrow_book.html", {"form": form, "book": book})

@login_required
def delete_borrow(request, borrow_id):
    if not request.user.is_superuser:
        messages.error(request, "Only librarians can delete borrow records.")
        return redirect('librarian_borrows')  

    borrow = get_object_or_404(Borrow, id=borrow_id)
    borrow.delete()
    messages.success(request, "Borrow history deleted successfully.")
    return redirect('all_borrows')

@login_required
def members_list(request):
    if not request.user.is_superuser:
        messages.error(request, "Only librarians can view members.")
        return redirect('home')  

    members = User.objects.filter(is_superuser=False).order_by('username')
    total_members = members.count()

    return render(request, 'members.html', {
        'members': members,
        'total_members': total_members
    })

@login_required
def add_category(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
    return redirect('adminpanel')

@login_required
def delete_category(request, cat_id):
    Category.objects.filter(id=cat_id).delete()
    return redirect('adminpanel')



@login_required
def reserve_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not book.is_available:
        Reservation.objects.create(user=request.user, book=book)
        messages.success(request, f'You have reserved "{book.name}". The librarian will be notified.')
    else:
        messages.warning(request, f'"{book.name}" is still available. You can borrow it directly.')

    return redirect('viewdetail', e_id=book.id)


@login_required
def reservation_list(request):
    if not request.user.is_superuser:  
        return redirect('home')  

    reservations = Reservation.objects.all().order_by('-reserved_at')
    return render(request, "reservation_list.html", {"reservations": reservations})


@login_required
def approve_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = "Approved"
    reservation.save()
    return redirect("reservation_list")


@login_required
def reject_reservation(request, pk):
    reservation = get_object_or_404(Reservation, pk=pk)
    reservation.status = "Rejected"
    reservation.save()
    return redirect("reservation_list")


@login_required
def add_language(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Language.objects.create(name=name)
    return redirect('adminpanel')

@login_required
def delete_language(request, language_id):
    Language.objects.filter(id=language_id).delete()
    return redirect('adminpanel')