from django import forms

from .models import Mail

INPUT_CLASSES = "w-full py-4 px-6 rounded-xl border text-xl"
PUT_CLASSES = "py-4 px-6 border text-2xl text-white"

class NewMailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = ('login', 'password',)

        labels = {
            'login': 'New login name',         
            'password': 'Password',
        }

        widgets = {
            'login': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'password': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
        }
