from django.contrib import admin
from django.db.models import Count

# Register your models here.
from .models import Player, Question, Choice, Response


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'active')


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('question', 'choice_text', 'correct', 'count_votes')

    def count_votes(self, obj):
        result = Response.objects.filter(choice=obj).aggregate(Count('id'))
        return result['id__count']


admin.site.register(Player)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Response)
admin.site.register(Choice, ChoiceAdmin)
