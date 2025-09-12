from rest_framework import serializers
from tutorials.models import Tutorial, Classes
 
 
class TutorialSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=70)
    description = serializers.CharField(max_length=200, allow_blank=False)
    published = serializers.BooleanField(default=False)

    class Meta:
        model = Tutorial
        fields = ('id',
                  'title',
                  'description',
                  'published')


class ClassesSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=70)
    description = serializers.CharField(max_length=200, allow_blank=False)
    grade = serializers.IntegerField(default=7)

    class Meta:
        model = Classes
        fields = ('id',
                  'name',
                  'description',
                  'grade')

