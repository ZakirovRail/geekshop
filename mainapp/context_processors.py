from basketapp.models import Basket


def basket(request):
    basket_item = []

    if request.user.is_authenticated:
        # improved for performance, reduced number of requests to DB
        # basket_item = Basket.objects.filter(user=request.user).order_by('product__category')
        # basket_item = Basket.objects.filter(user=request.user).order_by('product__category').select_related()
        basket_item = Basket.objects.filter(user=request.user)
    return {'basket': basket_item}
