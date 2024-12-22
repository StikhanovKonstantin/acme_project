from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView, DetailView
    )
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday

from typing import Any

from .utils import calculate_birthday_countdown


class BirthdayMixin:
    model = Birthday


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class BirthdayCreateView(LoginRequiredMixin, CreateView):
    """
    Отвечает за отображание формы, вызывает валидатор,
    даёт доступ к созданию И редактированию формы.
    """
    model = Birthday
    form_class = BirthdayForm

    def form_valid(self, form):
        # Присвоить полю author объект пользователя из запроса.
        form.instance.author = self.request.user
        # Продолжить валидацию, описанную в форме.
        return super().form_valid(form)


class BirthdayUpdateView(OnlyAuthorMixin, UpdateView):
    model = Birthday
    form_class = BirthdayForm


class BirhdayListView(BirthdayMixin, ListView):
    """
    Выводит список всех записей Дней Рождений из БД.
    """
    ordering = 'id'
    paginate_by = 10


class BirthdayDeleteView(OnlyAuthorMixin, DeleteView):
    """Удаляет выбранную запись."""
    model = Birthday
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(BirthdayMixin, DetailView):
    """Отвечает за отображение кол-ва дней до дня рождения."""

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["birthday_countdown"] = calculate_birthday_countdown(
            self.object.birthday
        )
        # Записываем в переменную form пустой объект формы.
        context['form'] = CongratulationForm()
        # Запрашиваем все поздравления для выбранного дня рождения.
        context['congratulations'] = (
            # Дополнительно подгружаем авторов комментариев,
            # чтобы избежать множества запросов к БД.
            self.object.congratulations.select_related('author')
        )
        return context


@login_required
def add_comment(request, pk):
    birthday = get_object_or_404(Birthday, pk=pk)
    form = CongratulationForm(request.POST)
    if form.is_valid():
        # Создаём объект поздравления, но не сохраняем его в БД.
        congratulation = form.save(commit=False)
        # В поле author передаём объект автора поздравления.
        congratulation.author = request.user
        # В поле birthday передаём объект дня рождения.
        congratulation.birthday = birthday
        # Сохраняем объект в БД.
        congratulation.save()
    # Перенаправляем пользователя назад, на страницу дня рождения.
    return redirect('birthday:detail', pk=pk)
