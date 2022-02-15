from django.shortcuts import render, get_object_or_404
from itertools import chain
# Create your views here.
from django.views.generic import ListView, DetailView

from cost.models import Product, ProductDetail, ProductStandardDetail, Detail, DetailLabor, ProductLabor, \
    ProductAssembly, Assembly, AssemblyDetail, AssemblyLabor, AssemblyStandardDetail, DetailMaterial


def product_list(request,):
    """Функция показывает список изделий"""
    product = Product.objects.all()
    return render(request,
                  'cost/product_list.html',
                  {'product': product,
                   })


def detail_detail(request, id):
    """Функция отображает подробную информацию о детали."""
    detail = get_object_or_404(Detail, id=id)
    detail_labors = DetailLabor.objects.filter(detail=detail)
    detail_materials = DetailMaterial.objects.filter(detail=detail)
    return render(request,
                  'cost/detail_detail.html',
                  {'detail': detail,
                   'detail_labors': detail_labors,
                   'detail_materials': detail_materials
                   })


def assembly_detail(request, assembly_slug):
    """Функция отображает подробную информацию о сборочной единице."""
    assembly = get_object_or_404(Assembly, slug=assembly_slug)
    assemblydetails = AssemblyDetail.objects.filter(assembly=assembly)
    assemblylabor = AssemblyLabor.objects.filter(assembly=assembly)
    assemblystandarddetail = AssemblyStandardDetail.objects.filter(assembly=assembly)
    print(assemblylabor)
    return render(request,
                  'cost/assembly_detail.html',
                  {'assembly': assembly,
                   'assemblydetails': assemblydetails,
                   'assemblylabor': assemblylabor,
                   'assemblystandarddetail': assemblystandarddetail
                   })


def product_detail(request, product_slug):
    """Функция отображает подробную информацию о продукте."""
    product = get_object_or_404(Product, slug=product_slug)
    productdetails = ProductDetail.objects.filter(product=product)
    productassemblies = ProductAssembly.objects.filter(product=product)
    productlabor = ProductLabor.objects.filter(product=product)
    productstandarddetail = ProductStandardDetail.objects.filter(product=product)

    return render(request,
                  'cost/product_detail.html',
                  {'product': product,
                   'productdetails': productdetails,
                   'productassemblies': productassemblies,
                   'productlabor': productlabor,
                   'productstandarddetail': productstandarddetail
                   })


def product_requirements(request, product_slug):
    """Функция отображает все затраты для изготовления продукта."""
    product = get_object_or_404(Product, slug=product_slug)

    assembly_detail_material_dict = dict()
    assembly_detail_labor_dict = dict()
    for assembly in ProductAssembly.objects.filter(product=product):  # перебираем узлы в изделии
        # print(assembly.assembly.name + ' - ' + str(assembly.amount))
        for detail in assembly.assembly.details.all():  # перебираем детали в узле
            for assemblydetail in AssemblyDetail.objects.filter(detail_id=detail.id).filter(assembly_id=assembly.id):
                # перебираем модель отношения деталей в узле, для возможности обратиться к количеству деталей в узле
                for det in DetailMaterial.objects.filter(detail_id=detail.id):
                    # перебираем модель отношение материалов в деталях, для возможности обратиться к количеству
                    # материалов в детали
                    count = det.amount * assemblydetail.amount * assembly.amount
                    # print(detail.name + ' - ' + det.material.name + ' - ' + str(assemblydetail.amount) +
                    #       ' * ' + str(det.amount) + ' * ' + str(assembly.amount) + ' = ' + str(count))
                    # соберем словарь ключ id материала значение количество
                    temp_dict = dict.fromkeys([det.material.id], count)
                    try:
                        assembly_detail_material_dict[det.material.id] += temp_dict[det.material.id]
                    except KeyError:
                        assembly_detail_material_dict[det.material.id] = temp_dict[det.material.id]
                for assemblydetlab in DetailLabor.objects.filter(detail_id=detail.id):
                    count = assemblydetlab.time * assemblydetail.amount * assembly.amount
                    # print(detail.name + ' - ' + str(assemblydetlab.labor.id) + ' - ' + assemblydetlab.labor.name
                    #       + ' - ' + assemblydetlab.labor.machine + ' - ' + str(assemblydetlab.time)
                    #       + ' * ' + str(assemblydetail.amount) + ' * ' + str(assembly.amount) + ' = ' +
                    #       str(count))
                    temp_dict = dict.fromkeys([assemblydetlab.labor.id], count)
                    try:
                        assembly_detail_labor_dict[assemblydetlab.labor.id] += temp_dict[assemblydetlab.labor.id]
                    except KeyError:
                        assembly_detail_labor_dict[assemblydetlab.labor.id] = temp_dict[assemblydetlab.labor.id]
    # print(assembly_detail_material_dict)
    # print(assembly_detail_labor_dict)

    detail_material_dict = dict()
    detail_labor_dict = dict()
    for productdetail in ProductDetail.objects.filter(product=product):  # перебираем детали в изделии
        # print(productdetail.detail.name + ' - ' + str(productdetail.amount))
        for detmat in DetailMaterial.objects.filter(detail_id=productdetail.detail.id):
            # перебираем модель отношение материалов в деталях, для возможности обратиться к количеству
            # материалов в детали
            count = detmat.amount * productdetail.amount
            # print(productdetail.detail.name + ' - ' + detmat.material.name + ' - ' + str(productdetail.amount) +
            #       ' * ' + str(detmat.amount) + ' = ' + str(count))
            temp_dict = dict.fromkeys([detmat.material.id], count)
            try:
                detail_material_dict[detmat.material.id] += temp_dict[detmat.material.id]
            except KeyError:
                detail_material_dict[detmat.material.id] = temp_dict[detmat.material.id]
        for detlab in DetailLabor.objects.filter(detail_id=productdetail.detail.id):
            count = detlab.time * productdetail.amount
            # print(str(detlab.labor.id) + ' - ' + detlab.labor.name + ' - ' + detlab.labor.machine
            #       + ' - ' + str(detlab.time) + ' - ' + str(count))
            temp_dict = dict.fromkeys([detlab.labor.id], count)
            try:
                detail_labor_dict[detlab.labor.id] += temp_dict[detlab.labor.id]
            except KeyError:
                detail_labor_dict[detlab.labor.id] = temp_dict[detlab.labor.id]
    # print(detail_material_dict)
    # print(detail_labor_dict)




    # detail_material_dict = dict()
    # for detail in productdetails.all():
    #     detailmaterial = DetailMaterial.objects.filter(detail_id=detail.id)
    #     for det in detailmaterial.all():
    #         pass
    #     count = det.amount * detail.amount
    #     temp_dict = dict.fromkeys([detail.id], count)
    #     print(temp_dict)
    #     try:
    #         detail_material_dict[detail.id] += temp_dict[detail.id]
    #     except KeyError:
    #         detail_material_dict[detail.id] = temp_dict[detail.id]

    productdetails = ProductDetail.objects.filter(product=product)
    productassemblies = ProductAssembly.objects.filter(product=product)
    productlabor = ProductLabor.objects.filter(product=product)
    productstandarddetail = ProductStandardDetail.objects.filter(product=product)

    # print(detail_material_dict)

    # for material, val in zip(detailmaterial, detail_material_dict.values()):
        # print(material.material.name + ' - ' + str(val))

    return render(request,
                  'cost/product_requirements.html',
                  {'product': product,
                   'productdetails': productdetails,
                   'productassemblies': productassemblies,
                   'productlabor': productlabor,
                   'productstandarddetail': productstandarddetail,

                   })


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


# def productdetails_detail(request, product_slug):
#     """Функция отображает подробную информацию о продукте."""
#     product = get_object_or_404(Product, slug=product_slug)
#     productdetails = ProductDetail.objects.filter(product=product)

    # productstandarddetails = ProductStandardDetail.objects.filter(product=product)
    # details = productdetails.filter(detail__in=detail.detail)


# Следующая конструкция позволяет объединить трудозатраты по станкам
#     detaillaborcosts = []
#     for detail in productdetails.all():  # Собираем в список все трудозатраты всех деталей через изделия
#         detaillaborcosts=list(chain(detaillaborcosts, DetailLabor.objects.filter(detail=detail.detail)))
#     labor_machine_list = []
#     for labor in detaillaborcosts:  # Собираем в словарь все станки - ключ слаг станка : значение = 0
#         labor_machine_list.append(labor.labor.mach_slug)
#     labor_machine = dict.fromkeys(labor_machine_list, 0)
#     for labor in detaillaborcosts:  # Создаем временный словарь и добавляем его значения в основной
#         temp_dict = dict.fromkeys([labor.labor.mach_slug], labor.time_details)
#         try:
#             labor_machine[labor.labor.mach_slug] += temp_dict[labor.labor.mach_slug]
#         except KeyError:  # Если ключа еще нет - создаем
#             labor_machine[labor.labor.mach_slug] = temp_dict[labor.labor.mach_slug]

    # Следующая конструкция позволяет объединить одинаковые стандартные изделия
    # productstandarddetails_list = []
    # for detail in productstandarddetails:
    #     productstandarddetails_list.append(detail.standard_detail.slug)
    # standard_details = dict.fromkeys(productstandarddetails_list, 0)
    # for detail in productstandarddetails:
    #     temp_dict = dict.fromkeys([detail.standard_detail.slug], detail.amount_standard_detail)
    #     try:
    #         standard_details[detail.standard_detail.slug] += temp_dict[detail.standard_detail.slug]
    #     except KeyError:
    #         standard_details[detail.standard_detail.slug] = temp_dict[detail.standard_detail.slug]

        # Следующая конструкция позволяет объединить одинаковые материал
        # materialdetails_list = []
        # for detail in productdetails:
        #     materialdetails_list.append(detail.detail.mat_slug)
        # details = dict.fromkeys(materialdetails_list, 0)
        # for detail in productdetails:
        #     temp_dict = dict.fromkeys([detail.detail.mat_slug], detail.detail.amount_material)
        #     try:
        #         details[detail.detail.mat_slug] += temp_dict[detail.detail.mat_slug]
        #     except KeyError:
        #         details[detail.detail.mat_slug] = temp_dict[detail.detail.mat_slug]

    # return render(request,
    #               'cost/product_detail.html',
    #               {'product': product,
    #                'productdetails': productdetails,
    #                'details': details,
    #                'standard_details': standard_details,
    #                'labor_machine': labor_machine
    #                })
