from django.urls import path
from .views import login_view, upload_picture, picture_list,view_picture,protected_media
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('upload/', upload_picture, name='upload_picture'),
    path('pictures/', picture_list, name='picture_list'),
    path("pictures/<int:picture_id>/",view_picture,name="view_picture"), 
    path('protected_media/<path:path>/', protected_media, name='protected_media')
]
