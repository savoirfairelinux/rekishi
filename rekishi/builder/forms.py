from django import forms

class QueryForm(forms.Form):
    host = forms.CharField(label='Host:', required=True)
    service = forms.CharField(label='Service:', required=True)
    series = forms.CharField(label='Time Series:', required=True)
    field = forms.CharField(label='Fields:', required=True)
