from django.views.generic import (
    CreateView, DeleteView, ListView, UpdateView, DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy

from .forms import BirthdayForm, CongratulationForm
from .models import Birthday
from .utils import calculate_birthday_countdown


@login_required
def add_comment(request, pk):
    birthday = get_object_or_404(Birthday, pk=pk)
    form = CongratulationForm(request.POST)
    if form.is_valid():
        congratulation = form.save(commit=False)
        congratulation.author = request.user
        congratulation.birthday = birthday
        congratulation.save()
    return redirect('birthday:detail', pk=pk)


class BirthdayMixin:
    model = Birthday


class OnlyAuthorMixin(UserPassesTestMixin):

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class BirthdayListView(ListView):
    model = Birthday
    ordering = 'id'
    paginate_by = 10


class BirhtdayCreateView(LoginRequiredMixin, BirthdayMixin, CreateView):
    form_class = BirthdayForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class BirthdayUpdateView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    BirthdayMixin,
    UpdateView
):
    form_class = BirthdayForm

    def test_func(self):
        object = self.get_object()
        return object.author == self.request.user


class BirthdayDeleteView(
    LoginRequiredMixin,
    OnlyAuthorMixin,
    BirthdayMixin,
    DeleteView
):
    success_url = reverse_lazy('birthday:list')


class BirthdayDetailView(DetailView):
    model = Birthday

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['birthday_countdown'] = calculate_birthday_countdown(
            self.object.birthday
        )
        context['form'] = CongratulationForm()
        context['congratulations'] = (
            self.object.congratulations.select_related('author')
        )
        return context
