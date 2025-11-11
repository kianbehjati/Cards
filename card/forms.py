from django import forms

class Transfer(forms.Form):

    to = forms.CharField(max_length=36,min_length=36,widget=forms.TextInput(attrs={
        'class':"input",
        "placeholder":"destination Card",

    }))
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={
        'class':"input",
        "placeholder":"amount",

    }))
    description = forms.CharField(required=False,widget=forms.Textarea(attrs={
        'class':"description",
    }))

