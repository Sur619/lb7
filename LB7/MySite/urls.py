from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import BetViewSet, home, profile, bets_page

router = DefaultRouter()
router.register(r'bets', BetViewSet)

urlpatterns = router.urls

# Добавляем дополнительные маршруты
urlpatterns += [
    path('bets/', bets_page, name='bets'),      # Ставки
]
