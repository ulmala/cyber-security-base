from django import forms
from . import models

class CreateQuestionForm(forms.ModelForm):
    class Meta:
        model = models.Question
        fields = ['question_text']

class CreateChoiceForm(forms.ModelForm):
    class Meta:
        model = models.Choice
        fields = ['choice_text']