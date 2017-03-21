from django import forms

class MainForm(forms.Form):
    keywords = forms.CharField(label= 'keywords', max_length = 100)
    startDate = forms.DateField(label = 'startDate')
    endDate = forms.DateField(label = 'endDate')
    """
    CHOICES = (('1', 'N Closest Neighbours'), ('2', 'Cosine Distance of Word Pairs'), ('3', 'Average TFIDF'), ('4', 'Pairwise conditional probabilities'))
    choice_field = forms.ChoiceField(widget = forms.RadioSelect, choices = CHOICES)
    n_closest = forms.IntegerField()
    textfile = forms.FileField()
    """
