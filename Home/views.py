from django.shortcuts import render,redirect
from django.http import HttpResponse
from Home.models import Product, Category, Department, Vendor, CartOrder, CartOrderItems, ProductImages, ProductReview, wishlist, Address



def index(request):
    # products = Product.objects.all().order_by('-id')
    products = Product.objects.filter(featured = True).order_by('-id')
    context = {
        'products':products
        }
    

    
    return render(request,'Home/index.html', context)  


def product_list_view(request):
    products = Product.objects.all().order_by('-id')
    # products = Product.objects.filter(product_status = "Published").order_by('-id')
    context = {
        'products':products
        }
    
    return render(request,'Home/product-list.html', context)  


def category_list_view(request):
    categories = Category.objects.all()

    context = {
        'categories':categories,


        }
    return render(request,'Home/category-list.html', context)

def department_list_view(request):
    departments = Department.objects.all()
    context = {
        'departments':departments
        }
    return render(request,'Home/department-list.html', context)

def category_product_list_view(request, cid):
    category = Category.objects.get(cid = cid)
    department = Department.objects.filter(category = category).order_by('-id')
    products = Product.objects.filter( product_status = "published", category = category).order_by('-id')
    context = {
        'category':category,
        'products':products,
        'department':department
        }
    
    return render(request,'Home/category-product-list.html', context)


def department_category_list_view(request, did):
    department = Department.objects.get(did = did)
    category = Category.objects.filter(department = department).order_by('-id')
    products = Product.objects.filter( product_status = "published", department = department).order_by('-id')

    context = {
        'category':category,
        'department':department,
        'products':products
        }
    
    return render(request,'Home/department-category-list.html', context)



def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        'vendors':vendors
        }
    return render(request,'Home/vendor-list.html', context)



def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid = vid)
    context = {
        'vendor':vendor
        }
    return render(request,'Home/vendor-detail.html', context)

