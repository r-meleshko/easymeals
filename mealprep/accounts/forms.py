from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible


class LoginForm(forms.Form):
    username = forms.CharField(max_length=69)
    password = forms.CharField(max_length=69)
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible)
