from django import forms

class MainForm(forms.Form):
    keywords = forms.CharField(label= 'keywords', max_length = 100)
    startDate = forms.CharField(label = 'startDate', max_length = 100)
    endDate = forms.CharField(label = 'endDate', max_length = 100)
