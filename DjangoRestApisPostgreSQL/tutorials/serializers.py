from rest_framework import serializers, viewsets
from tutorials.models import Tutorial
 
 
class TutorialSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    description = serializers.CharField(max_length=70, allow_blank=False, default='')
    published = serializers.BooleanField(default=False)

    class Meta:
        model = Tutorial
        fields = ('id',
                  'title',
                  'description',
                  'published')     

