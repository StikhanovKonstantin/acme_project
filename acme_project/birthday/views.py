from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
    )

from django.urls import reverse_lazy

from .forms import BirthdayForm
from .models import Birthday

from typing import Any

from .utils import calculate_birthday_countdown


class BirthdayMixin:
    model = Birthday


class BirthdayCreateView(BirthdayMixin, CreateView):
    """
    Отвечает за отображание формы, вызывает валидатор,
    даёт доступ к созданию И редактированию формы.
    """
    form_class = BirthdayForm


class BirthdayUpdateView(BirthdayMixin, UpdateView):
    form_class = BirthdayForm


class BirhdayListView(BirthdayMixin, ListView):
    """
    Выводит список всех записей Дней Рождений из БД.
    """
    ordering = 'id'
    paginate_by = 10


class BirthdayDeleteView(BirthdayMixin, DeleteView):
    """Удаляет выбранную запись."""
    success_url = reverse_lazy('birthday:birthday_list')


class BirthdayDetailView(BirthdayMixin, DetailView):
    """Отвечает за отображение кол-ва дней до дня рождения."""

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["birthday_countdown"] = calculate_birthday_countdown(
            self.object.birthday
        )
        return context
