from django import forms
from django.core.exceptions import ValidationError

from .models import Birthday
from .constants import BEATLES


class BirthdayForm(forms.ModelForm):

    class Meta:
        model = Birthday
        fields = '__all__'
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'})
        }

    def clean_first_name(self):
        """
        Валидатор: в поле 'Имя' отбирает только 1-е слово.
        """
        first_name = self.cleaned_data['first_name']
        return first_name.split()[0]

    def clean(self):
        """
        Валидатор: проверяет, являются ли
        'допустимыми' имя и фамилия человека в форме.
        """
        super().clean()
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']
        if f'{first_name} {last_name}' in BEATLES:
            raise ValidationError(
                'Мы тоже любим Битлз, но введите лучше настоящее имя:)'
            )
