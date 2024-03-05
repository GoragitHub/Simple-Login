from django import forms
from .models import UserPicture

class PictureUploadForm(forms.ModelForm):
    class Meta:
        model = UserPicture
        fields = ['picture']
