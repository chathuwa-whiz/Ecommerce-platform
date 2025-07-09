from django.db import models
from django.contrib.auth import get_user_model
from stores.models import Store

User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    Category = models.ForeignKey(Category, on_delete=models.CASCADE)

    # Basic info
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    
    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2)
    compare_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    track_stock = models.BooleanField(default=True)
    
    # Physical properties (for shipping calculation)
    weight = models.DecimalField(max_digits=8, decimal_places=2, help_text="Weight in grams")
    length = models.DecimalField(max_digits=8, decimal_places=2, help_text="Length in cm")
    width = models.DecimalField(max_digits=8, decimal_places=2, help_text="Width in cm")
    height = models.DecimalField(max_digits=8, decimal_places=2, help_text="Height in cm")
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['store', 'slug']

    def __str__(self):
        return f'{self.name} - {self.store.name}'
    
    @property
    def is_in_stock(self):
        return self.stock_quantity > 0 if self.track_stock else True
    
    @property
    def is_low_stock(self):
        return self.stock_quantity <= self.low_stock_threshold if self.track_stock else False
    
    class ProductImage(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
        image = models.ImageField(upload_to='products/')
        alt_text = models.CharField(max_length=200, blank=True)
        is_primary = models.BooleanField(default=False)
        order = models.PositiveIntegerField(default=0)
        
        class Meta:
            ordering = ['order', 'id']
        
        def __str__(self):
            return f"Image for {self.product.name}"
        
    class ProductVariant(models.Model):
        product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
        name = models.CharField(max_length=100)  # e.g., "Size", "Color"
        value = models.CharField(max_length=100)  # e.g., "Large", "Red"
        price_adjustment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
        stock_quantity = models.PositiveIntegerField(default=0)
        sku = models.CharField(max_length=100, unique=True)
        
        def __str__(self):
            return f"{self.product.name} - {self.name}: {self.value}"