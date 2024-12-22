from django import forms
from django.core.exceptions import ValidationError

from django.core.mail import send_mail

from .models import Birthday, Congratulation
from .constants import BEATLES


class BirthdayForm(forms.ModelForm):

    class Meta:
        model = Birthday
        exclude = ('author',)
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
            send_mail(
                subject='Another Beatles member',
                message=(
                    f'{first_name} {last_name} пытался опубликовать запись!'
                ),
                from_email='birthday_form@acme.not',
                recipient_list=['admin@acme.not'],
                fail_silently=True,
            )
            raise ValidationError(
                'Мы тоже любим Битлз, но введите лучше настоящее имя:)'
            )


class CongratulationForm(forms.ModelForm):

    class Meta:
        model = Congratulation
        fields = ('text',)
