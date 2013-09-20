# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
# from django.contrib.auth.models import User


# class CustomUser(User):
#
#     def __unicode__(self):
#         return self.email
#
#     class Meta:
#         proxy = True
#         verbose_name = verbose_name_plural = '使用者'
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver


class Person(models.Model):
    user = models.OneToOneField(User, primary_key=True, unique=True)
    nickname = models.CharField(max_length=255, verbose_name='暱稱', blank=True)
    email = models.EmailField(verbose_name='電子郵件', blank=True)
    fullname = models.CharField(max_length=255, verbose_name='姓名(*)', blank=True)
    gender = models.CharField(max_length=7, verbose_name='性別(*)',
                              choices=(('unknown', '未指定'), ('male', '男性'), ('female', '女性')), default='unknown')
    address = models.CharField(max_length=255, verbose_name='地址(*)', blank=True)
    occupation = models.CharField(max_length=255, verbose_name='職業(*)', blank=True)
    status = models.CharField(max_length=20,
                              choices=(('normal', '正常'), ('spam', '垃圾')),
                              default='normal')
    subscribing = models.BooleanField(default=True, verbose_name='我同意訂閱 Mozilla 電子報')

    def __unicode__(self):
        return unicode('%s (%s)' % (self.fullname, self.status))

    class Meta:
        verbose_name = verbose_name_plural = '個人資料'


# User.profile = property(lambda u: Person.objects.get_or_create(user=u)[0])
@receiver(pre_save, sender=Person)
def sync_person_default_email(sender, instance, **kwargs):
    if not instance.email:
        instance.email = instance.user.email
    if not instance.fullname:
        instance.fullname = instance.user.first_name + instance.user.last_name

@receiver(post_save, sender=User)
@receiver(post_save, sender=Person)
def manage_subscription(sender, instance, **kwargs):
    pass