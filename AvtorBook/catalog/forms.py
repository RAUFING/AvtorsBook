from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Введите имя:", max_length=20, widget=forms.TextInput(attrs={ 'class':'form-control'}))
    password = forms.CharField(label="Введите пароль:", max_length=64, widget=forms.PasswordInput(attrs={ 'class':'form-control'}))
class RegisterForm(forms.Form):
    mail = forms.EmailField(label="Почта:", help_text="Например: avtorbook@email.com", widget=forms.TextInput(attrs={ 'class':'form-control'}))
    firstname = forms.CharField(label='Имя',max_length=30, widget=forms.TextInput(attrs={ 'class':'form-control'}))
    lastname = forms.CharField(label='Фамилия',max_length=30, widget=forms.TextInput(attrs={ 'class':'form-control'}))
    username = forms.CharField(label="Пользвательское имя:", help_text="Оно уникальное, его в будущем нельзя изминить", widget=forms.TextInput(attrs={ 'class':'form-control'}))
    password = password = forms.CharField(label="Введите пароль:" , max_length=64, widget=forms.PasswordInput(attrs={ 'class':'form-control'}))
    password_povtor = forms.CharField(label="Введите повторный пароль:" , max_length=64, widget=forms.PasswordInput(attrs={ 'class':'form-control'}))
    sogl = forms.BooleanField(label="Я соглашаюсь с политикой сайта")
class CreateBook(forms.Form):
    title = forms.CharField(label="Введите название книги:" , max_length=64, widget=forms.TextInput(attrs={ 'class':'form-control'}))
    opis = forms.CharField(label='Введите описание книги:', widget=forms.Textarea(attrs={'cols': 20, 'rows': 10,  'class':'form-control'}))
    text = forms.CharField(label="Текст:",widget=forms.Textarea(attrs={'cols': 70, 'rows': 10}))
    yes = forms.BooleanField(label="Я соглашаюсь с политикой добавления книги:")

class Filter(forms.Form):
    text = forms.CharField(max_length=64, label='',  widget=forms.TextInput(attrs={'placeholder': 'Введите запрос',  'class':'form-control'}))

class CreateComment(forms.Form):
    text = forms.CharField(max_length=64, label='',  widget=forms.Textarea(attrs={'cols': 20, 'rows': 3, 'placeholder': 'Введите коментарий', 'class':'form-control'}))