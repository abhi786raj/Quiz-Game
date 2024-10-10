from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuestionViewSet, ChoiceListView, AttemptedQuestionView, UnattemptedQuestionView, LeaderboardView

router = DefaultRouter()
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),  # Automatically includes all question routes
    path('choices/', ChoiceListView.as_view(), name='choice-list'),
    path('attempted-questions/', AttemptedQuestionView.as_view(), name='attempted-question'),
    path('unattempted-question/', UnattemptedQuestionView.as_view(), name='unattempted-question'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
]
