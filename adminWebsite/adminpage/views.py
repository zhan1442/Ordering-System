from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Order, Drug, Product
from .forms import LoginForm, OrderStatus_Form, Drug_form, Product_form
import json
from django.http import QueryDict
from django.urls import reverse
# login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login


# login view
def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        error_message = ""
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            # If the user object is empty, no matching username and password were found
            if user is not None:
                # if user.is_active:
                    if user.profile.user_type == "Administrator":
                        auth_login(request, user)
                    # Redirect the user to their profile page
                        return redirect(reverse("adminpage:admin_home"))
                    else:
                        error_message = "You are not authorized to login here."
                # else:
                #    error_message = "Your account is disabled"
            else:
                error_message = "Username or Password incorrect."

                # The page is being loaded for the first time, so load a blank page
    else:
        form = LoginForm()
        error_message = ""
    return render(request, 'registration/styled_login.html',
                  {'form': form,
                   'error_message': error_message, })


PROGRESS = {
    'new': '17%',
    'filled': '34%',
    'remove': '52%',
    'ready': '69%',
    'billing': '86%',
    'complete': '100%',
}


# logined views from here.

@login_required
def admin_home(request):
    user = request.user

    new_orders = Order.objects.filter(status='new').order_by('date_time')
    fill_orders = Order.objects.filter(status='filled').order_by('date_time')
    remove_orders = Order.objects.filter(status='remove').order_by('date_time')
    ready_orders = Order.objects.filter(status='ready').order_by('date_time')

    context = {
        'user': user,
        'new_orders': new_orders,
        'fill_orders': fill_orders,
        'remove_orders': remove_orders,
        'ready_orders': ready_orders,
    }

    return render(request, "pharmHome.html", context)


@login_required
def admin_billing(request):
    user = request.user

    billing_orders = Order.objects.filter(status='billing').order_by('date_time')

    return render(request, "billing.html", context={'user': user, 'billing_orders': billing_orders})


@login_required
def admin_archive(request):
    user = request.user

    archive_orders = Order.objects.filter(status='complete').order_by('date_time')

    return render(request, "archive.html", context={'user': user, 'archive_orders': archive_orders})


@login_required
def admin_orderDetail(request, order_id):
    user = request.user

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

    # calculate the total quantity
    # the total price is not possible because client side does not support it...
    total_q = 0
    for drug in drug_set:
        total_q += drug.quantity

    context = {'user': user,
               'order': order,
               'status_form': status_form,
               'message': message,
               'progress': PROGRESS.get(order.status),
               'drug_set': drug_set,
               'total_q': total_q,
               'change_succeed': change_succeed, }

    return render(request, "orderDetail.html", context)


@login_required
def admin_editPage(request, order_id):
    user = request.user

    order = get_object_or_404(Order, pk=order_id)
    form = Drug_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            drug = form.save(commit=False)
            drug.order_obj = order
            drug.save()
            form = Drug_form()

    drug_set = order.drug_set.all()

    context = {'user': user,
               'order': order,
               'drug_set': drug_set,
               'form': form, }

    return render(request, "orderEdit.html", context)


@login_required
def admin_manageProducts(request):
    user = request.user

    actives = "A"
    if 'query' in request.GET:
        query = request.GET['query']
        if query:
            actives = query

    if request.method == 'POST':
        actives = request.POST.get('actives')

    product_lists = []
    if actives != "":
        for active in actives:
            product_lists.append(Product.objects.filter(name__iregex=r"^[%s].*$" % active))
            active_products = zip(actives, product_lists)
    else:
        active_products = None

    import string
    atoz = list(string.ascii_uppercase)
    atoz = atoz[1:]

    context = {
        'user': user,
        'active_products': active_products,
        'atoz': atoz,
        'actives': actives,
    }

    return render(request, "manageProducts.html", context)


@login_required
def admin_productEdit(request, product_id):
    user = request.user

    product = get_object_or_404(Product, pk=product_id)
    if request.method != 'POST':
        form = Product_form(initial={'brand': product.brand,
                                     'name': product.name,
                                     'strength': product.strength,
                                     'price': str(product.price),
                                     'CIN': str(product.CIN),
                                     'description': product.description,
                                     })
    else:
        form = Product_form(request.POST)
        if form.is_valid():
            product.name = request.POST.get('name')
            product.strength = request.POST.get('strength')
            product.price = request.POST.get('price')
            product.CIN = request.POST.get('CIN')
            product.description = request.POST.get('description')
            product.save()

            link = reverse('adminpage:admin_manageProducts')
            link += "?query=" + product.name[0].upper()
            return redirect(link)

    context = {
        'user': user,
        'product': product,
        'form': form,
    }

    return render(request, "productEdit.html", context)


@login_required
def admin_newProduct(request):
    user = request.user

    form = Product_form(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            product = form.save(commit=False)
            product.save()
            link = reverse('adminpage:admin_manageProducts')
            link += "?query=" + product.name[0].upper()
            return redirect(link)

    context = {
        'user': user,
        'form': form,
    }

    return render(request, "productEdit.html", context)


# temp API
# product
@login_required
def admin_productDelete(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)

        product.delete()

        return redirect(reverse('adminpage:admin_manageProducts'))


# order
@login_required
def admin_orderRevise(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, pk=order_id)

        order.delete()

        if order.status == "billing":
            return redirect(reverse('adminpage:admin_billing'))
        elif order.status == "complete":
            return redirect(reverse('adminpage:admin_archive'))
        else:
            return redirect(reverse('adminpage:admin_home'))


# order detail change api
@login_required
def admin_revise(request):
    if request.method == 'PUT':
        query = QueryDict(request.body)
        drug_pk = query['pk']
        drug = get_object_or_404(Drug, pk=drug_pk)
        if query['name'] == 'brand':
            drug.brand = query['value']
        elif query['name'] == 'name':
            drug.name = query['value']
        elif query['name'] == 'strength':
            drug.strength = query['value']
        elif query['name'] == 'quantity':
            drug.quantity = query['value']

        drug.save()

        result = {'success': 'true', 'msg': 'failed'}
        out = json.dumps(result)
        return HttpResponse(out, content_type='application/json')

    elif request.method == 'DELETE':
        delete = QueryDict(request.body)
        drug_pk = delete['pk']
        drug = get_object_or_404(Drug, pk=drug_pk)
        drug.delete()
        return HttpResponse(status=200)


# search drug list API for auto completion
@login_required
def admin_autoDruglist(request):
    # error checking
    if request.method != 'GET':
        return HttpResponse("failed: not GET")
    if 'field' not in request.GET or 'query' not in request.GET:
        return HttpResponse("failed: missing 'field' or 'query' in request")

    field = request.GET['field']
    q = request.GET['query']
    if not field:
        return HttpResponse("failed: 'field' or 'query' should not be None")

    # start query process
    response = []
    query_set = Product.objects.none()

    if field == 'brand':
        if 'name' in request.GET:
            name = request.GET['name']
            if name:
                query_set = Product.objects.filter(brand__icontains=q, name=name)
            else:
                query_set = Product.objects.filter(brand__icontains=q)
        else:
            query_set = Product.objects.filter(brand__icontains=q)

    elif field == 'name':
        if 'brand' in request.GET:
            brand = request.GET['brand']
            if brand:
                query_set = Product.objects.filter(name__icontains=q, brand=brand)
            else:
                query_set = Product.objects.filter(name__icontains=q)
        else:
            query_set = Product.objects.filter(name__icontains=q)

    # important: must have brand and name provided to return not empty
    elif field == 'strength':
        if 'brand' in request.GET and 'name' in request.GET:
            brand = request.GET['brand']
            name = request.GET['name']
            if brand and name:
                if not q:
                    query_set = Product.objects.filter(brand=brand, name=name)
                else:
                    query_set = Product.objects.filter(strength__icontains=q, brand=brand, name=name)
    else:
        return HttpResponse("failed: this 'field' does not exist")

    # serialize to response array
    for product in query_set:
        if product.brand not in response:
            if field == 'brand':
                response.append(product.brand)
            elif field == 'name':
                response.append(product.name)
            elif field == 'strength':
                response.append(product.strength)

    result = {"suggestions": response}
    out = json.dumps(result)
    return HttpResponse(out, content_type='application/json')
