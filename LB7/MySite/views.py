from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .serializer import *
from rest_framework.permissions import IsAuthenticated
from .models import SportsCategory, Vote, Match
from django.core.paginator import Paginator


class BetViewSet(ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def home(request):
    sports_categories = SportsCategory.objects.distinct()[:4]  # Отображать только 1 категорию
    return render(request, 'home.html', {'sports_categories': sports_categories})


@login_required
def profile(request):
    last_bet = request.user.bets.last()  # Последняя ставка пользователя
    last_vote = request.user.votes.last()  # Последнее голосование пользователя
    return render(request, 'profile.html', {
        'user': request.user,
        'last_bet': last_bet,
        'last_vote': last_vote,
    })



@login_required
def bets_page(request):
    return render(request, 'bets.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    return render(request, 'login.html')


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


def register(request):
    if request.user.is_authenticated:
        return redirect('profile')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. You are now logged in.')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        user.save()
        messages.success(request, 'Profile updated successfully.')
        return redirect('profile')
    return render(request, 'edit_profile.html', {'user': request.user})


@login_required
def vote(request, category_id):
    category = get_object_or_404(SportsCategory, id=category_id)
    match = Match.objects.filter(category=category).first()

    if request.method == 'POST':
        team = request.POST.get('team')
        amount = request.POST.get('amount')  # Сумма ставки, если нужно
        outcome = request.POST.get('outcome')  # Исход ставки, если требуется

        # Сохранение ставки
        Bet.objects.create(
            user=request.user,
            outcome=outcome,
            amount=amount
        )

        messages.success(request, f"You placed a bet on {team} in {category.name}.")
        return redirect('profile')

    return render(request, 'vote.html', {'category': category, 'match': match})


@login_required
def history(request):
    bets = Bet.objects.filter(user=request.user).order_by('-created_at')  # Сортировка по дате
    paginator = Paginator(bets, 3)  # Пагинация: 10 ставок на страницу
    page_number = request.GET.get('page', 1)  # Используем значение по умолчанию (1), если параметр отсутствует
    page_obj = paginator.get_page(page_number)
    return render(request, 'history.html', {'page_obj': page_obj})
