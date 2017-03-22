from django import forms

class MainForm(forms.Form):
    keywords = forms.CharField(label= 'keywords', max_length = 100)
    startDate = forms.DateField(label = 'startDate')
    endDate = forms.DateField(label = 'endDate')
    
    #granularity = forms.ChoiceField(label = 'unit')
