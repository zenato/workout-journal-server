from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Event(models.Model):
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = verbose_name

    name = models.CharField(max_length=200, verbose_name='Name')
    unit = models.CharField(max_length=10, default='Kg', verbose_name='Unit')
    value = models.SmallIntegerField(blank=True, null=True, verbose_name='Value')
    remark = models.TextField(blank=True, null=True, verbose_name='Etc.')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def last_performance(self):
        return Performance.objects.filter(event=self.id).order_by('-post__workout_date').first()

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = verbose_name

    workout_date = models.DateTimeField(default=timezone.now, verbose_name='Workout date')
    remark = models.CharField(max_length=200, blank=True, null=True, verbose_name='Remark')
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def formatted_workout_date(self):
        return timezone.localtime(self.workout_date).strftime('%Y-%m-%d %H:%M')

    formatted_workout_date.short_description = 'Workout date'

    def __str__(self):
        return self.formatted_workout_date()


class Performance(models.Model):
    class Meta:
        verbose_name = 'Performance'
        verbose_name_plural = verbose_name

    post = models.ForeignKey(Post, related_name='performances', on_delete=models.CASCADE)
    event = models.ForeignKey(Event, verbose_name='Event')
    value = models.SmallIntegerField(blank=True, null=True, verbose_name='Value')
    set1 = models.SmallIntegerField(blank=True, null=True, verbose_name='Set 1')
    set2 = models.SmallIntegerField(blank=True, null=True, verbose_name='Set 2')
    set3 = models.SmallIntegerField(blank=True, null=True, verbose_name='Set 3')
    set4 = models.SmallIntegerField(blank=True, null=True, verbose_name='Set 4')
    set5 = models.SmallIntegerField(blank=True, null=True, verbose_name='Set 5')

    def __str__(self):
        return '%s - %s' % (self.post.workout_date, self.event.name)
