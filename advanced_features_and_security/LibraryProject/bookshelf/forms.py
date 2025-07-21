from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(required=False, max_length=100, label='Search Title')

class ExampleForm(forms.Form):
    name = forms.CharField(label='Your Name', max_length=100)
    email = forms.EmailField(label='Email')
    message = forms.CharField(label='Message', widget=forms.Textarea)
