from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class StuffType(models.Model):
    description = models.CharField(max_length=128)
    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = 'Stuff types'


class Stuff(models.Model):
    account = models.ForeignKey(get_user_model(), verbose_name='User', on_delete=models.PROTECT)
    type = models.ForeignKey(StuffType, verbose_name='Type', on_delete=models.PROTECT)
    amount = models.DecimalField('Money Amount', max_digits=8, decimal_places=2)
    date_out = models.DateTimeField('Date in', null=True)
    date_in = models.DateTimeField('Date out', auto_now_add=True)

    def __str__(self):
        return '%s' % self.account

    class Meta:
        ordering = ('-date_in', )


class Feedback(models.Model):
    account = models.ForeignKey(get_user_model(), verbose_name='User', on_delete=models.PROTECT)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.CharField(max_length=2048)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s' % self.pk

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Feedback'
