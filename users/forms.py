from scraping.models import City, NameProf
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email and password:
            qs = User.objects.filter(email = email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя не существует')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль неверный')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Данный аккаунт отключён')
        return super(UserLoginForm, self).clean(*args, **kwargs)

class UserRegisterForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Username')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Repeat password')
    class Meta:
        model = User
        fields = ('email', 'name', )

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']

class UserUpdateForm(forms.Form):
    name = forms.CharField(max_length=50, required=True, label='Username')
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=True,
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Город'
                                  )
    prof = forms.ModelChoiceField(queryset=NameProf.objects.all(), to_field_name='slug', required=True,
                                  widget=forms.Select(attrs={'class': 'form-control'}), label='Специальность'
                                  )
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput(), label='Получать рассылку?')
    class Meta:
        model = User
        fields = ('city', 'prof', 'send_email', 'name', )