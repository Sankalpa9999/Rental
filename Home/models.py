from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.safestring import mark_safe

from userauths.models import User

# Create your models here.

STATUS_CHOICE = (
    ('process', 'Processing'),
    ('shipped', 'Shipped'),
    ('delivered', 'Delivered'),
)
STATUS = (
    ('draft', 'Draft'),
    ('disabled', 'Disabled'),
    ('rejected', 'Rejected'),
    ('in_review', 'In Review'),
    ('published', 'Published'),
)
RATING = (
    ('1', '★☆☆☆☆'),
    ('2', '★★☆☆☆'),
    ('3', '★★★☆☆'),
    ('4', '★★★★☆'),
    ('5', '★★★★★')
)

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class Department(models.Model):
    did = ShortUUIDField(unique=True, length=10, max_length=20, prefix='dat',alphabet='abcdefgh12345')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='department', default='department.jpg')
    
    class Meta:
        verbose_name_plural = 'Departments'
        
    def department_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
    
    def __str__ (self):
        return self.title


class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='cat',alphabet='abcdefgh12345')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='category', default='category.jpg')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
    
    def __str__ (self):
        return self.title
        
class Tags(models.Model):
    pass

class Vendor(models.Model):
    vid = ShortUUIDField(unique=True, length=10, max_length=20, prefix='ven',alphabet='abcdefgh12345')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path, default='vendor.jpg')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True, default='Pokhara')
    contact = models.CharField(max_length=100, null=True, blank=True, default='977-9000000')   
    chat_resp_time = models.CharField(max_length=100, null=True, blank=True, default='10:00 AM - 5:00 PM')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Vendors'
        
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
    
    def __str__ (self):
        return self.title
    

class Product(models.Model):
    pid = ShortUUIDField(unique=True, length=10, max_length=20,alphabet='abcdefgh12345')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, related_name='vendor')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='department')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=user_directory_path, default='product.jpg')
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=99999, decimal_places=2,default=100)
    old_price = models.DecimalField(max_digits=99999, decimal_places=2,default=100)
    specifications = models.TextField(null=True, blank=True)
    # Tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices= STATUS, max_length=100, default='in_review')
    status = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=False)
    digital = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    sku = ShortUUIDField(unique=True, length=10, max_length=20, prefix = "sku", alphabet='abcdefgh12345')
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True) 
    
    class Meta:
        verbose_name_plural = 'Products'
        
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />'%(self.image.url))
    
    def __str__ (self):
        return self.title
    
    def get_percentage(self):
        if self.old_price > self.price:  # Ensure old_price is greater to avoid negative or incorrect values
            discount_percentage = ((self.old_price - self.price) / self.old_price) * 100
            return round(discount_percentage, 2)  # Round to 2 decimal places
        return 0  # Return 0 if there's no discount

    
class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to="product-images", default='product.jpg')
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Product Images'
    
class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=99999, decimal_places=2,default=100)
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices= STATUS_CHOICE, max_length=100, default='Processing')
    
    class Meta:
        verbose_name_plural = 'Cart Order'
        

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    Product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.ImageField(upload_to="cart-order", default='product.jpg')
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=99999, decimal_places=2,default=100)
    total = models.DecimalField(max_digits=99999, decimal_places=2,default=100)
    
    
    class Meta:
        verbose_name_plural = 'Cart Order Items'
        
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />'%(self.image))
    
class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    rating = models.IntegerField(choices= RATING, default=None)
    review = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Product Reviews'
                
    def __str__ (self):
        return self.rating
    
    def get_rating(self):
        return self.rating
    
class wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'wishlist'
        
    def __str__ (self):
        return self.product.title
    
class Address(models.Model):
    user= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200 , null=True, blank=True)
    status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Address'
    
