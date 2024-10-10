import random
from rest_framework.response import Response
from rest_framework import generics, permissions, viewsets
from .models import Question, AttemptedQuestion, Leaderboard, Choice
from .serializers import QuestionSerializer, AttemptedQuestionSerializer, LeaderboardSerializer, ChoiceSerializer


# Admin view for CRUD operations on Questions
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can view, create, retrieve, update, or delete questions


# User view for attempting one unattempted question
class UnattemptedQuestionView(generics.RetrieveAPIView):
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can get an unattempted question

    def get(self, request, *args, **kwargs):
        user = request.user
        attempted_questions = AttemptedQuestion.objects.filter(user=user).values_list('question_id', flat=True)
        unattempted_questions = Question.objects.exclude(id__in=attempted_questions).filter(published=True)

        # If there are no unattempted questions, return a message
        if not unattempted_questions.exists():
            return Response({'message': 'No unattempted questions available.'}, status=404)

        # Select a random question from the unattempted questions
        question = random.choice(unattempted_questions)
        serializer = self.get_serializer(question)
        return Response(serializer.data)


# AttemptedQuestion View
class AttemptedQuestionView(generics.ListCreateAPIView):
    queryset = AttemptedQuestion.objects.all()
    serializer_class = AttemptedQuestionSerializer
    permission_classes = [permissions.IsAuthenticated]  # Only authenticated users can attempt questions

    def get_queryset(self):
        user = self.request.user
        return self.queryset.filter(user=user)  # Return only attempted questions for the logged-in user


# Choice List View for Admin Users
class ChoiceListView(generics.ListAPIView):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can view choices


# Leaderboard View
class LeaderboardView(generics.ListAPIView):
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer
    permission_classes = [permissions.IsAuthenticated]  # All authenticated users can view the leaderboard

    def get_queryset(self):
        return super().get_queryset().order_by('-score', 'joined_at')  # Order by score and join date
