from django import forms
from scraping.models import City, NameProf

class FindVac(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False)
    prof = forms.ModelChoiceField(queryset=NameProf.objects.all(), to_field_name='slug', required=False )