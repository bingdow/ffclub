# -*- coding: utf-8 -*-
import commonware

from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelChoiceField, Select
from django.forms.util import ErrorList
from ffclub.upload.models import ImageUpload
from ffclub.event.models import Event

log = commonware.log.getLogger('ffclub')


class ImageUploadForm(ModelForm):

    def __init__(self, user, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=':', empty_permitted=False, instance=None):
        super(ImageUploadForm, self).__init__(data, files, auto_id, prefix, initial, error_class, label_suffix,
                                              empty_permitted, instance)
        if data is not None and 'event' in data and data['event'] != '':
            self.event = Event.objects.get(id=data['event'])
        self.user = user
        if user.is_authenticated():
            # Choose from events user created
            userEvents = Event.objects.filter(create_user=user).order_by('-create_time')
            # Default newest event
            userDefaultEvent = userEvents[:1].get() if userEvents.count() > 0 else None
            self.hasEvent = userDefaultEvent is not None
            self.fields['event'] = ModelChoiceField(
                queryset=userEvents, label='活動名稱', initial=userDefaultEvent)
            # Set field order as first
            fieldOrder = self.fields.keyOrder
            fieldOrder.pop(fieldOrder.index('event'))
            fieldOrder.insert(0, 'event')

    def save(self, commit=True):
        self.instance.entity_object = self.event
        return super(ImageUploadForm, self).save(commit)

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image._size > 1 * 1024 * 1024:
                raise ValidationError('檔案超已過1MB上限')
            return image
        else:
            raise ValidationError('無法上傳檔案')

    class Meta:
        model = ImageUpload
        fields = ('image_large', 'description')