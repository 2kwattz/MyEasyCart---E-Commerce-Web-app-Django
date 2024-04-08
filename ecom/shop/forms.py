from django import forms
from .models import Contact
from django.core.exceptions import ValidationError
import re

class ContactForm(forms.ModelForm):

    forbidden_words = ['badword1', 'badword2']
    class Meta:
        model = Contact
        fields = '__all__'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        name = name.title()
        if not name:
            raise forms.ValidationError("Name field cannot be blank")
        if len(name) < 3:
            raise forms.ValidationError("Name must be of atleast 3 characters")
        if len(name) > 50:
            raise forms.ValidationError("Name cannot exceed more than 50 characters")
        
        for word in self.forbidden_words:
            if word.lower() in name.lower():
                raise forms.ValidationError(f"Name contains a forbidden word")
        return name
    
    def clean_emailAddress(self):
        emailAddress = self.cleaned_data.get('emailAddress')

        #  if not email.endswith('@example.com'):
            # raise forms.ValidationError("Only emails from example.com domain are allowed.")

        if not emailAddress:
            raise forms.ValidationError("Email Field cannot be blank")
        

        try:
            # Django's EmailField performs basic email format validation
            forms.EmailField().clean(emailAddress)
        except ValidationError:
            raise forms.ValidationError("Invalid email address format")
         
        
        return emailAddress
        
    def clean_message(self):
        message = self.cleaned_data.get('message')

        if not message:
            raise forms.ValidationError("Message field cannot be blank")
        if len(message) < 3:
            raise forms.ValidationError("Message cannot be so short")
        if len(message) > 400:
            raise forms.ValidationError("Message exceeds 400 characters")
        for forbidden_word in self.forbidden_words:
            if forbidden_word.lower() in message.lower():
                raise forms.ValidationError("Message cannot contain a forbidden word")
        return message
    
    