from django.shortcuts import render, get_object_or_404
from itertools import chain
# Create your views here.
from django.views.generic import ListView, DetailView

from cost.models import Product, ProductDetail, ProductStandardDetail, Detail, DetailLaborCosts


#
# class ProductsView(ListView):
#     """Список изделий"""
#     model = Product
#     queryset = Product.objects.all()


# class ProductDetailView(DetailView):
#     """Полное описание изделия"""
#     model = Product
#     slug_field = "slug"
#     print(model)
#     print("model_id")
#     print(model.details)
# print(model.self.request.query_params.get('id'))
# product = Product.objects.filter(slug="slug")
# print(product)
# proid = product.id
# details = ProductDetail.objects.filter(id=proid)
#

# def get_productdetails(self, request):
#     product_id = self.request.query_params.get('slug')
#     productdetails = ProductDetail.objects.filter(id=product_id)
#     return print(productdetails)
#     product = Product.objects.filter(id=product_id)
#     print(product)


def product_list(request,):
    """Функция показываем все инструменты по умолчанию,
    позволяет настроить фильтр по категориям и/или по владельцам."""
    product = Product.objects.all()
    return render(request,
                  'cost/product_list.html',
                  {'product': product,
                   })


def productdetails_detail(request, product_slug):
    """Функция отображает подробную информацию о продукте."""
    product = get_object_or_404(Product, slug=product_slug)
    productdetails = ProductDetail.objects.filter(product=product)
    productstandarddetails = ProductStandardDetail.objects.filter(product=product)




# Следующая конструкция позволяет объединить трудозатраты по станкам
    detaillaborcosts = []
    for detail in productdetails.all():  # Собираем в список все трудозатраты всех деталей через изделия
        detaillaborcosts=list(chain(detaillaborcosts, DetailLaborCosts.objects.filter(detail=detail.detail)))
    labor_machine_list = []
    for labor in detaillaborcosts:  # Собираем в словарь все станки - ключ слаг станка : значение = 0
        labor_machine_list.append(labor.labor.mach_slug)
    labor_machine = dict.fromkeys(labor_machine_list, 0)
    for labor in detaillaborcosts:  # Создаем временный словарь и добавляем его значения в основной
        temp_dict = dict.fromkeys([labor.labor.mach_slug], labor.time_details)
        try:
            labor_machine[labor.labor.mach_slug] += temp_dict[labor.labor.mach_slug]
        except KeyError:  # Если ключа еще нет - создаем
            labor_machine[labor.labor.mach_slug] = temp_dict[labor.labor.mach_slug]

    # Следующая конструкция позволяет объединить одинаковые стандартные изделия
    productstandarddetails_list = []
    for detail in productstandarddetails:
        productstandarddetails_list.append(detail.standard_detail.slug)
    standard_details = dict.fromkeys(productstandarddetails_list, 0)
    for detail in productstandarddetails:
        temp_dict = dict.fromkeys([detail.standard_detail.slug], detail.amount_standard_detail)
        try:
            standard_details[detail.standard_detail.slug] += temp_dict[detail.standard_detail.slug]
        except KeyError:
            standard_details[detail.standard_detail.slug] = temp_dict[detail.standard_detail.slug]

        # Следующая конструкция позволяет объединить одинаковые материал
        materialdetails_list = []
        for detail in productdetails:
            materialdetails_list.append(detail.detail.mat_slug)
        details = dict.fromkeys(materialdetails_list, 0)
        for detail in productdetails:
            temp_dict = dict.fromkeys([detail.detail.mat_slug], detail.detail.amount_material)
            try:
                details[detail.detail.mat_slug] += temp_dict[detail.detail.mat_slug]
            except KeyError:
                details[detail.detail.mat_slug] = temp_dict[detail.detail.mat_slug]

    return render(request,
                  'cost/product_detail.html',
                  {'product': product,
                   'productdetails': productdetails,
                   'details': details,
                   'standard_details': standard_details,
                   'labor_machine': labor_machine
                   })

