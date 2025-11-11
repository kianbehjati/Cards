from django import forms

class Contact_form(forms.Form):
    title = forms.CharField(max_length=50,widget=forms.TextInput(attrs={
        "class":"input",
        "placeholder":"title"
    }))
    text = forms.CharField(widget=forms.Textarea(attrs={
        "class":"text",
        "placeholder": "details"
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "class":"input",
        "placeholder": "email"
    }))

