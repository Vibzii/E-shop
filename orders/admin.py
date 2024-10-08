from django.contrib import admin
from .models import Payment, Order, OrderProduct

class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    list_display = ['payment', 'product', 'variations', 'quantity', 'product_price', 'ordered']
    readonly_fields = ('payment', 'product', 'variations', 'quantity', 'product_price', 'ordered')
    extra = 0



class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'email', 'city', 'order_total', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
# Register your models here.

