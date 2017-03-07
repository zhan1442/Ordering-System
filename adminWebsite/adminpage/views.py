from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Client, Order, Drug
from .forms import OrderStatus_Form, Drug_form
import json
from django.http import QueryDict

PROGRESS = {
    'new': '17%',
    'filled': '34%',
    'remove': '52%',
    'ready': '69%',
    'billing': '86%',
    'complete': '100%',
}

# Create your views here.)


def admin_home(request):
    new_orders = Order.objects.filter(status='new').order_by('date_time')
    fill_orders = Order.objects.filter(status='filled').order_by('date_time')
    remove_orders = Order.objects.filter(status='remove').order_by('date_time')
    ready_orders = Order.objects.filter(status='ready').order_by('date_time')

    context = {
        'new_orders': new_orders,
        'fill_orders': fill_orders,
        'remove_orders': remove_orders,
        'ready_orders': ready_orders,
    }

    return render(request, "pharmHome.html", context)


def admin_billing(request):
    billing_orders = Order.objects.filter(status='billing').order_by('date_time')

    return render(request, "billing.html", context={'billing_orders': billing_orders})


def admin_archive(request):
    archive_orders = Order.objects.filter(status='complete').order_by('date_time')

    return render(request, "archive.html", context={'archive_orders': archive_orders})


def admin_orderDetail(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    message = ""
    change_succeed = ""
    if request.method == 'POST':
        order.status = request.POST.get('status')
        order.save()
        change_succeed = "true"
        message = request.POST.get('notes')

    status_form = OrderStatus_Form(initial={'status': order.status})
    drug_set = order.drug_set.all()

    context = {'order': order,
               'status_form': status_form,
               'message': message,
               'progress': PROGRESS.get(order.status),
               'drug_set': drug_set,
               'change_succeed': change_succeed, }

    return render(request, "orderDetail.html", context)


def admin_editPage(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    form = Drug_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            drug = form.save(commit=False)
            drug.order_obj = order
            drug.save()

    drug_set = order.drug_set.all()

    context = {'order': order,
               'drug_set': drug_set,
               'form': form, }

    return render(request, "orderEdit.html", context)


def admin_revise(request):
    if request.method == 'PUT':
        put = QueryDict(request.body)
        drug_pk = put['pk']
        drug = get_object_or_404(Drug, pk=drug_pk)
        if put['name'] == 'brand':
            drug.brand = put['value']
        elif put['name'] == 'name':
            drug.name = put['value']
        elif put['name'] == 'strength':
            drug.strength = put['value']
        elif put['name'] == 'quantity':
            drug.quantity = put['value']

        drug.save()

        result = {'success': 'true', 'msg': 'failed'}
        oput = json.dumps(result)
        return HttpResponse(oput, content_type='application/json')

    elif request.method == 'DELETE':
        delete = QueryDict(request.body)
        drug_pk = delete['pk']
        drug = get_object_or_404(Drug, pk=drug_pk)
        drug.delete()
        return HttpResponse(status=200)
