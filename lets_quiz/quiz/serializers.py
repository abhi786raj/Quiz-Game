from rest_framework import serializers
from .models import Question, Choice, AttemptedQuestion, Leaderboard

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = ['id', 'text', 'published', 'choices']

    def create(self, validated_data):
        choices_data = validated_data.pop('choices', [])
        question = Question.objects.create(**validated_data)
        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)
        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop('choices', None)
        instance.text = validated_data.get('text', instance.text)
        instance.published = validated_data.get('published', instance.published)
        instance.save()

        if choices_data is not None:
            # Update choices if provided
            for choice_data in choices_data:
                choice_id = choice_data.get('id', None)
                if choice_id:
                    choice = Choice.objects.get(id=choice_id, question=instance)
                    choice.text = choice_data.get('text', choice.text)
                    choice.is_correct = choice_data.get('is_correct', choice.is_correct)
                    choice.save()
                else:
                    Choice.objects.create(question=instance, **choice_data)

        return instance


class AttemptedQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttemptedQuestion
        fields = ['user', 'question', 'selected_choice', 'timestamp']


class LeaderboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Leaderboard
        fields = ['user', 'score', 'joined_at']
