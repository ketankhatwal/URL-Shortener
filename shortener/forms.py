from django import forms
from .models import Short

class Short_URL_Form(forms.ModelForm):
    class Meta:
        model = Short
        fields = ['actual_url']