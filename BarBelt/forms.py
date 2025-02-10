from django import forms
from .models import User

class NewFaceForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']