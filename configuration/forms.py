from django import forms


class Configuration (forms.Form):
    name = forms.CharField(max_length=255)
    IP = forms.GenericIPAddressField()
    port = forms.IntegerField()
    TypeSNMP = forms.CharField(max_length=255)