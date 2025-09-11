from rest_framework import serializers
from tutorials.models import Tutorial
 
 
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

