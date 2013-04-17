# -*- coding: utf-8 -*-

import logging

from django.contrib import auth
from django.shortcuts import render, redirect
from django.forms.models import inlineformset_factory

from ffclub.event.forms import *
from forms import *
from models import *
from ffclub.settings import CUSTOM_ORDER_DETAIL_CHOICES, CUSTOM_PRODUCT_KEYWORDS
from ffclub.person.models import Person
from utils import *


log = logging.getLogger('ffclub')


def wall(request):
    if request.user.is_authenticated() and not Person.objects.filter(user=request.user).exists():
        return redirect('user.register')

    products = Product.objects.all()
    OrderDetailFormset = inlineformset_factory(Order, OrderDetail,
                                               extra=products.count(), can_delete=False,
                                               form=OrderDetailForm, formset=BaseOrderDetailFormSet)
    orderDetailData = []

    for product in products:
        orderDetailData.append({'product': product})

    orderDetailFormset = OrderDetailFormset(initial=orderDetailData)

    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        orderForm = OrderForm(request.POST)
        OrderDetailFormset = inlineformset_factory(Order, OrderDetail,
                                                   extra=0, can_delete=False,
                                                   form=OrderDetailForm, formset=BaseOrderDetailFormSet)
        orderDetailFormset = OrderDetailFormset(request.POST, initial=orderDetailData)

        if orderDetailFormset.is_valid() and eventForm.is_valid() and orderForm.is_valid():
            event = eventForm.save(commit=False)
            order = orderForm.save(commit=False)
            event.create_user = auth.get_user(request)
            order.create_user = auth.get_user(request)
            event.save()
            order.event = event
            order.save()

            for orderDetailForm in orderDetailFormset:
                orderDetail = orderDetailForm.save(commit=False)
                if orderDetail.quantity > 0:
                    orderDetail.order = order
                    orderDetail.save()

            verification_code = generate_random_string(36, string.ascii_letters + string.digits)
            verification = OrderVerification(order=order, create_user=auth.get_user(request),
                                             code=verification_code)
            verification.save()
            send_order_verification_mail(order.fullname, order.email, verification_code)
            return redirect('product.order.verify')
    else:
        if request.user.is_active:
            profile = request.user.get_profile()
            initialValues = {
                'fullname': profile.fullname,
                'email': request.user.email,
                'address': profile.address,
                'occupation': profile.occupation,
            }
        else:
            initialValues = {}
        eventForm = EventForm()
        orderForm = OrderForm(initial=initialValues)

    for orderDetailForm in orderDetailFormset:
        product_id = orderDetailForm.initial['product'].id
        orderDetailForm.fields['quantity'].widget.attrs['size'] = 5
        if product_id in CUSTOM_ORDER_DETAIL_CHOICES:
            orderDetailForm.fields['quantity'].choices = CUSTOM_ORDER_DETAIL_CHOICES[product_id]

    data = {
        'event_form': eventForm,
        'order_form': orderForm,
        'order_detail_formset': orderDetailFormset,
    }
    return render(request, 'product/wall.html', data)


def product_photos(request, product_id):
    product = Product.objects.get(id=product_id)
    productKeywords = CUSTOM_PRODUCT_KEYWORDS[product_id] if product_id in CUSTOM_PRODUCT_KEYWORDS.keys() else None
    data = {'product': product, 'photos': product.photos.filter(usage='original'),
            'productKeywords': productKeywords}
    return render(request, 'product/product_photos.html', data)


def order_complete(request):
    data = {}
    # You'd add data here that you're sending to the template.
    return render(request, 'product/order_complete.html', data)


def order_verify(request):
    data = {}
    verification_code = request.GET.get('code', None)
    if None != verification_code:
        # verify code
        verifications = OrderVerification.objects.filter(code=verification_code)
        if verifications.exists():
            for v in verifications:
                v.status = 'confirmed'
                v.save()
                v.order.status = 'confirmed'
                send_order_notification_mail(v.order.fullname, v.order.id)
                v.order.save()
            return redirect('product.order.complete')
            # You'd add data here that you're sending to the template.
    return render(request, 'product/order_verify.html', data)
