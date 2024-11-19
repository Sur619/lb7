from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .models import Bet
from .serializer import *
from rest_framework.permissions import IsAuthenticated


class BetViewSet(ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


def home(request):
    return render(request, 'home.html')


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def bets_page(request):
    return render(request, 'bets.html')


def login_view(request):
    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Аккаунт успешно создан. Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})
