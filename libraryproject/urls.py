"""
URL configuration for libraryproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from libraryapp.views import *



from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user-autocomplete/', UserAutocomplete.as_view(), name='user-autocomplete'),
    path('', home, name='home'),
    path('addbook/', addbookfn, name='addbook'),
    path('viewbooks/', viewbooksfn, name='viewbooks'),
    path('categorydisplay/<int:c_id>/', categorydisplayfn, name='categorydisplay'),
    path('registeruser/', registeruserfn, name='registeruser'),
    path('saveuser/', saveuserfn, name='saveuser'),
    path('login/', loginfn, name='login'),
    path('forgotpassword/', forgotpasswordfn, name='forgotpassword'),
    path('logout/', logoutfn, name='logout'),
    path('viewdetail/<int:e_id>/', viewdetailfn, name='viewdetail'),
    path('editbook/<int:e_id>/', editbookfn, name='editbook'),
    path('deletebook/<int:d_id>/', deletebookfn, name='deletebook'),
    path('search/', searchfn, name='search'),
    path('adminpanel/', adminpanelfn, name='adminpanel'),
    path('profile/', profilefn, name='profile'),
    path('completeprofile/', completeprofilefn, name='completeprofile'),
    path('librarian_borrow/<int:book_id>/', librarian_borrow_book, name='librarian_borrow_book'),
    path('librarian_return/<int:borrow_id>/', librarian_return_book, name='librarian_return_book'),
    path('librarian_borrows/', all_borrowsfn, name='all_borrows'),
    path('delete_borrow/<int:borrow_id>/', delete_borrow, name='delete_borrow'),
    path('members/', members_list, name='members_list'),
    path('add_category/', add_category, name='add_category'),
    path('delete_category/<int:cat_id>/', delete_category, name='delete_category'),
    path('reserve/<int:book_id>/', reserve_book, name='reserve_book'),
    path('reservations/', reservation_list, name='reservation_list'),
    path("reservations/<int:pk>/approve/", approve_reservation, name="approve_reservation"),
    path("reservations/<int:pk>/reject/", reject_reservation, name="reject_reservation"),
    path("languages/add/", add_language, name="add_language"),
    path("languages/delete/<int:language_id>/", delete_language, name="delete_language"),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('borrow-general/', BorrowBookView.as_view(), name='borrow-general'),
    path('book-autocomplete/', BookAutocomplete.as_view(), name='book-autocomplete'),
    path('borrow_book/<int:borrow_book_id>/return/', mark_returned, name='mark_returned'),



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

