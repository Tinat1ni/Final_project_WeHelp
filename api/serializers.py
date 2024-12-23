from rest_framework import serializers
from post.models import Post, Category

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    custom_input_1 = serializers.CharField(required=False)
    custom_input_2 = serializers.CharField(required=False)
    deadline_date = serializers.DateField()
    deadline_time = serializers.TimeField(required=False)
    location = serializers.CharField()
    picture = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = [
            'title', 'description', 'deadline_date', 'deadline_time',
            'location', 'picture', 'custom_input_1', 'custom_input_2'
        ]


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'description', 'location', 'deadline_date', 'deadline_time', 'picture']
        read_only_fields = ['author']