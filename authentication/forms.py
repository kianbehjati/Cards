from django import forms

class login_form(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(attrs=
        {
            'class':'input',
            'placeholder':"User name"
        }
    ))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class":"input pass",
                "placeholder":"Password"
            }
        )
    )

class signup_form(forms.Form):
    user_name = forms.CharField(
        widget=forms.TextInput(
            attrs= {
                'class':'input',
                'placeholder':"UserName"
            }
        )
    )
    email = forms.EmailField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'input pass',
                'placeholder':"Email(Optional)"
            }
        )
    )

    password = forms.CharField(
        widget = forms.TextInput(
            attrs={
                'class': 'input pass',
                'placeholder':"Password"

            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input pass',
                'placeholder':"Confirm password"
            }
        )
    )


class Forget_pass(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input pass',
        "placeholder":"User Name"
    }))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input pass',
        "placeholder":"Phone number"
    }))

class Change_pass(forms.Form):

    password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input pass',
                'placeholder': "Password"

            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'input pass',
                'placeholder': "Confirm password"
            }
        )
    )

class user_edit(forms.Form):
    user_name = forms.CharField(widget=forms.TextInput(attrs={
        "class":"input",
    }))
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "class":"input",
    }))
