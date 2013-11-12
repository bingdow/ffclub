# -*- coding: utf-8 -*-
from ffclub.base import admin
from django.contrib.admin import ModelAdmin, StackedInline, TabularInline
from .models import *
from ffclub.product.models import Order
from ffclub.upload.admin import ImageUploadInline


class ParticipationInline(TabularInline):
    model = Participation
    extra = 0


class AwardInline(TabularInline):
    model = Award
    extra = 0


class OrderInline(StackedInline):
    model = Order
    extra = 0


class ActivityAdmin(ModelAdmin):
    change_form_template = 'admin/custom_activity_change_form.html'


class EventAdmin(ActivityAdmin):
    search_fields = ['title', 'description', 'location',
                     'orders__usage', 'orders__fullname', 'orders__email',
                     'orders__address', 'orders__occupation', 'orders__feedback']
    list_filter = ['num_of_ppl', 'create_time', 'status', 'orders__create_time', 'orders__status']
    inlines = [AwardInline, OrderInline, ParticipationInline, ImageUploadInline]


admin.site.register(Event, EventAdmin)


class CampaignAdmin(ActivityAdmin):
    search_fields = ['title', 'description']
    list_filter = ['create_time', 'status']
    inlines = [AwardInline, ParticipationInline, ImageUploadInline]


admin.site.register(Campaign, CampaignAdmin)


class VoteAdmin(ModelAdmin):
    search_fields = ['note']
    list_filter = ['vote_time', 'status']


admin.site.register(Vote, VoteAdmin)


class VideoAdmin(ModelAdmin):
    search_fields = ['title', 'description']
    list_filter = ['create_time', 'status']


admin.site.register(Video, VideoAdmin)
