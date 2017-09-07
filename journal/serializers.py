from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Event, Post, Performance


# Event Serializers

class LastPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Performance
        fields = ('value', 'set1', 'set2', 'set3', 'set4', 'set5')


class EventSerializer(serializers.ModelSerializer):
    last_performance = LastPerformanceSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'unit', 'value', 'remark', 'last_performance')


# Performance Serializers

class PerformanceEventSerializer(serializers.ModelSerializer):
    id = serializers.ModelField(model_field=Event()._meta.get_field('id'))
    last_performance = LastPerformanceSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'unit', 'value', 'remark', 'last_performance')


class PerformanceSerializer(serializers.ModelSerializer):
    event = PerformanceEventSerializer()

    class Meta:
        model = Performance
        fields = ('id', 'event', 'value', 'set1', 'set2', 'set3', 'set4', 'set5')


# Post Serializers

class PostSerializer(serializers.ModelSerializer):
    performances = PerformanceSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'workout_date', 'performances')

    def create(self, validated_data):
        performances_data = validated_data.pop('performances')
        post = Post.objects.create(**validated_data)
        for performance_data in performances_data:
            event_data = performance_data.pop('event')
            event = Event.objects.get(id=event_data.get('id'))
            performance = Performance.objects.create(post=post, event=event, **performance_data)
            post.performances.add(performance)

        return post

    def update(self, instance, validated_data):
        Performance.objects.filter(post=instance).delete()
        instance.performances = []
        performances_data = validated_data.pop('performances')
        for performance_data in performances_data:
            event_data = performance_data.pop('event')
            event = Event.objects.get(id=event_data.get('id'))
            performance = Performance.objects.create(post=instance, event=event, **performance_data)
            instance.performances.add(performance)

        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email',)
