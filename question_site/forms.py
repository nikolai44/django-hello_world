from django import forms
from django.core.validators import RegexValidator, validate_email, validate_image_file_extension
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from question_site.models import Question, Tag, User, Answer

text_validator = RegexValidator(r"[а-яА-Яa-zA-Z]", "Текст должен содержать буквы")
tags_validator = RegexValidator(r"[а-яА-Яa-zA-Z]", "Тэги состоят из букв")
password_validator = RegexValidator(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
                                    "Пароль - 8+ символов на латиннице. Буквы и цифры")


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label="First name", validators=[text_validator], widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 1,
        'maxlength': 30,
        'placeholder': 'Имя'
    }))

    last_name = forms.CharField(label="Last name", validators=[text_validator], widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 1,
        'maxlength': 30,
        'placeholder': 'Фамилия'
    }))

    username = forms.CharField(label="Username", validators=[text_validator], widget=forms.TextInput(attrs={
        'class': 'form-control',
        'minlength': 5,
        'maxlength': 30,
        'placeholder': 'Логин'}))

    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'E-mail'}))

    password = forms.CharField(label="Enter password", validators=[password_validator], widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Пароль'}))

    password_confirmation = forms.CharField(label="Reenter password", widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Подтверждение пароля'}))

    avatar = forms.ImageField(label="Photo", required=False)

    def clean(self):
        cleaned_data = super(UserRegistrationForm, self).clean()
        password = cleaned_data.get("password")
        password_confirmation = cleaned_data.get("password_confirmation")
        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        avatar = cleaned_data.get("avatar")

        try:
            RegexValidator(password_validator, password)
        except ValidationError:
            raise ValidationError("Only letters, numbers, underscores or hyphens in password")
        if password != password_confirmation:
            raise ValidationError("Password and Confirm password does not match")
        if User.objects.by_username(username) is not None:
            raise ValidationError("This user name is already taken.")
        if User.objects.by_email(email) is not None:
            raise ValidationError("This email is already taken.")
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError("This email is invalid")       # ???
        return cleaned_data

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', 'password_confirmation', 'avatar']


class AddQuestionForm(forms.ModelForm):
    title = forms.CharField(validators=[text_validator], widget=forms.TextInput(attrs={
        'class': 'form-control',
        'maxlength': 100,
        'minlength': 5,
        'placeholder': 'Title'}))

    text = forms.CharField(validators=[text_validator], widget=forms.Textarea(attrs={
        'class': 'form-control',
        'maxlength': 1000,
        'minlength': 5,
        'placeholder': 'Write your question here...'}))

    tags = forms.CharField(required=False, validators=[text_validator], widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'List here tags by separating them with a commas.'}))

    def clean(self):
        title = self.cleaned_data.get('title')
        tags = self.cleaned_data.get('tags')
        if len(str(title)) > 100:
            raise ValidationError("Sorry, a title should contain no more than 100 characters. ")
        if len(str(tags)) > 50:
            raise ValidationError("Sorry, length of tags line must be no more than 20 characters.  ")
        return self.cleaned_data

    class Meta:
        model = Question
        fields = ['title', 'text', 'tags']


class AddAnswerForm(forms.ModelForm):
    text = forms.CharField(validators=[text_validator], widget=forms.Textarea(attrs={
        'class': 'form-control',
        'maxlength': 1000,
        'minlength': 5,
        'placeholder': 'Write your answer here...'}))

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Question
        fields = ['text']


class AddAvatarForm(forms.ModelForm):
    avatar = forms.ImageField(label="Photo")

    def clean(self):
        return self.cleaned_data

    class Meta:
        model = Question
        fields = ['avatar']