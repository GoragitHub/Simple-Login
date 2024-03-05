from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from .forms import PictureUploadForm
from .models import UserPicture
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
import os
from django.http import HttpResponseForbidden, FileResponse


def login_view(request):
    if request.user.is_authenticated:
        return redirect("picture_list")
    if request.method == 'POST':
        redirect_url = request.POST.get('next', 'picture_list')
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(redirect_url)
    else:
        redirect_url = request.GET.get('next', 'picture_list')
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form, 'next': redirect_url})
# ----------------------------------------------------------Alter--------------------------------------------------------------------
# def login_view(request):
#     if request.method == 'POST':
#         redirect_url = request.POST.get('next', '')
#         form = AuthenticationForm(request, request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 if redirect_url:
#                     return redirect(redirect_url)
#                 else:
#                     return redirect('picture_list')  # Replace 'picture_list' with your actual URL name
#     else:
#         redirect_url = request.GET.get('next', '')
#         form = AuthenticationForm()
#     return render(request, 'accounts/login.html', {'form': form, 'next': redirect_url})
# ------------------------------------------------------------------------------------------------------------------------------

@login_required
def upload_picture(request):
    if request.method == 'POST':
        form = PictureUploadForm(request.POST, request.FILES)
        if form.is_valid():
            picture = form.save(commit=False)
            picture.user = request.user
            picture.save()
            return redirect('picture_list')
    else:
        form = PictureUploadForm()
    return render(request, 'accounts/upload_picture.html', {'form': form})

@login_required
def picture_list(request):
    pictures = UserPicture.objects.filter(user=request.user)
    return render(request, 'accounts/picture_list.html', {'pictures': pictures})

@permission_required('Admin.can_access_pictures')
def view_picture(request, picture_id):
    if request.user.is_authenticated:
        picture = get_object_or_404(UserPicture, id=picture_id, user=request.user)
        return render(request, 'accounts/view_picture.html', {'picture': picture})   
    else:
        return redirect("login") 

def protected_media(request, path):
    if not request.user.is_authenticated:
        # If the user is not authenticated, redirect to the login page
        return redirect('/?next=/protected_media/'+path)

    # Get the absolute file path
    file_path = os.path.join(settings.MEDIA_ROOT, path)                # how can restrict access to media image url in django

    # Check if the file exists and is a file (not a directory)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        # Serve the file using FileResponse
        return FileResponse(open(file_path, 'rb'), content_type='image/jpg')  # Adjust content_type accordingly
    else:
        # Return forbidden response if the file doesn't exist or is a directory
        return HttpResponseForbidden("Access forbidden")    

    