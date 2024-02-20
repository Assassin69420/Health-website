from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .forms import NewOfferForm, EditOfferForm
from .models import Item, Cart, CartItem

# Create your views here.


def index(request):
    return render(request, 'index.html')


def error404(request):
    return render(request, 'error.html')

def About(request):
    return render(request, 'About.html')

def newcart(request):
    return render(request, 'newcart.html')

def category(request, category):
    sport_items = Item.objects.filter(category='Sport')
    fashion_items = Item.objects.filter(category='Fashion')
    electronics_items = Item.objects.filter(category='Electronics')
    automobile_items = Item.objects.filter(category='Automobile')

    return render(request, 'category.html',
                  {
                      'category': category, 'sport_items': sport_items, 'fashion_items': fashion_items,
                      'electronics_items': electronics_items, 'automobile_items': automobile_items
                  })


def add_offer(request):
    form = NewOfferForm()
    if request.method == 'POST':
        form = NewOfferForm(request.POST, request.FILES)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            categ_num = form.cleaned_data['category']
            category = NewOfferForm.CATEGORIES[int(categ_num) - 1][1]
            image = request.FILES.get('image')
            item = Item(user=user, name=name, description=description,
                        price=price, category=category, image=image)
            print(item.image.url)
            item.save()
            return redirect(f'/offer/{item.id}')
        else:
            form = NewOfferForm()
    return render(request, 'add_offer.html', {'form': form})

def edit_offer(request, id):
    item = Item.objects.get(id=id)
    form = EditOfferForm(item=item)
    if request.method == 'POST':
        
        if 'cancel' in request.POST:
            print(request.POST)
            form.is_valid = True
            return redirect(f'/offer/{item.id}')

        form = EditOfferForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            categ_num = form.cleaned_data['category']
            if categ_num:
                category = NewOfferForm.CATEGORIES[int(categ_num) - 1][1]
                item.category = category
            
            """Don't change value if user didn't change it in edit window"""
            if len(name) >= 1:
                item.name = name
            else:
                pass
            if len(description) >= 1:
                item.description = description
            else:
                pass
            if not price == None:
                item.price = price
            else:
                pass

            item.save()
            return redirect(f'/offer/{item.id}')
        else:
            form = EditOfferForm(item=item)

    return render(request, 'edit_offer.html', {'item': item, 'form': form})



def view(request, id):
    item = Item.objects.get(id=id)

    if request.method == 'POST' and 'add' in request.POST:
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart(user=user, total=0, quantity=0)
            cart.save()

        cart_item = CartItem(cart=cart, item=item, quantity=1, image=item.image, price=item.price, user=item.user)
        cart_item.save()
        cart.total += item.price
        cart.save()
        return redirect('/cart/')
    if request.method == 'POST' and 'edit' in request.POST:
        return redirect(f'/offer/{id}/edit')

    return render(request, 'item_details.html', {'item': item})


@login_required
def cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)
    except Cart.DoesNotExist:
        cart = None
        cart_items = []

    if request.method == 'POST':
        for cart_item in cart_items:
            item_name_remove = f'{cart_item.item.name}_remove'
            item_name_save = f'{cart_item.item.name}_save'
            item_quantity = f'{cart_item.item.name}_quantity'
            
            if item_name_remove in request.POST:
                # cart.total = 0
                cart_item.delete()
                cart.total -= cart_item.price * cart_item.quantity
                cart.save()
                return redirect('/cart/')
            
            if item_name_save in request.POST:
                if int(request.POST.get(item_quantity)) < 0:
                    pass
                elif int(request.POST.get(item_quantity)) >= 0:
                    if cart_item.quantity < int(request.POST.get(item_quantity)):
                        cart.total += cart_item.price * (int(request.POST.get(item_quantity)) - cart_item.quantity)
                    elif cart_item.quantity > int(request.POST.get(item_quantity)):
                        cart.total -= cart_item.price * (cart_item.quantity - int(request.POST.get(item_quantity)))    
                    cart.save()
                    cart_item.quantity = request.POST.get(item_quantity)
                    cart_item.save()

                if int(cart_item.quantity) == 0:
                    cart_item.delete()
                    cart.save()
                    return redirect('/cart/')
                
    return render(request, 'cart.html', {'cart': cart, 'cart_items': cart_items})

def user_view(request, id):  
    current_user = request.user
    
    try:
        user = User.objects.get(id=id)
        items = Item.objects.filter(user=user)
        
        if request.method == "POST":
            for item in items:
                if f'{item.id}_remove' in request.POST:
                    item.delete()
                    return redirect(f'/user/{user.id}')
        
        if request.user.is_authenticated:
            return render(request, 'user.html', {'user': user, 'current_user': current_user, 'items': items})
        else:
            return redirect('/404/')
    
    except ObjectDoesNotExist:
        raise Http404
    
def category_list(request):
    return render(request, 'category_list.html')

def search_results(request):
    searched = request.POST['searched']
    items = Item.objects.all()
    if request.method == 'POST':
        items_list = []
        for item in items:
            if searched.lower() in item.name.lower():
                items_list.append(item)
        return render(request, 'search_results.html', {'searched': searched, 'items_list':items_list})
    else:
        return render(request, 'search_results.html')
    

    