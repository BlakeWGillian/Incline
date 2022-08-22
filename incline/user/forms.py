from django import forms


class ContractProgress(forms.Form):
    description = forms.CharField(max_length=1024)
    notes = forms.CharField(max_length=300, blank=False)
    date = forms.DateField()
    file = forms.FileField(blank=False)

class SearchSubmissions(forms.Form):
    selected_submission = forms.IntegerField()