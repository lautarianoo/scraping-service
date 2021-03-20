from django import forms
from scraping.models import City, NameProf, Vacancy

class FindVac(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False)
    prof = forms.ModelChoiceField(queryset=NameProf.objects.all(), to_field_name='slug', required=False )

class VForm(forms.ModelForm):
    city = forms.ModelChoiceField(queryset=City.objects.all(), label='City', widget=forms.Select(attrs={'class': 'form_control'}))
    prof = forms.ModelChoiceField(queryset=NameProf.objects.all(), label='Specialization', widget=forms.Select(attrs={'class': 'form_control'}))

    url = forms.CharField(label='URL', widget=forms.URLInput(attrs={'class': 'form_control'}))
    title = forms.CharField(label='Name Vacancy', widget=forms.TextInput(attrs={'class': 'form_control'}))
    company = forms.CharField(label='Name Company', widget=forms.TextInput(attrs={'class': 'form_control'}))
    description = forms.CharField(label='Description Vacancy', widget=forms.Textarea(attrs={'class': 'form_control'}))

    class Meta:
        model = Vacancy
        fields = '__all__'