from django.contrib import admin
from .models import Product, Variation, ProductGallery, ReviewRating
import admin_thumbnails
@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1  # Number of empty forms to display by default
    #fields = ['image', 'variation']  # Show only these fields in the inline form

    # Filtering the variation field based on the selected product
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'variation':
            # Get the currently selected product instance
            if request.resolver_match.kwargs.get('object_id'):
                product_id = request.resolver_match.kwargs['object_id']
                kwargs['queryset'] = Variation.objects.filter(product_id=product_id)
            else:
                kwargs['queryset'] = Variation.objects.none()  # No variations available if no product is selected yet
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
@admin_thumbnails.thumbnail('image')
class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ("product_name", 'price', 'shipping', 'category', 'article_nummer', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [VariationInline, ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ("product", 'variation_category', 'variation_value', 'is_active')
    list_editable = ("is_active",)
    list_filter = ("product", 'variation_category', 'variation_value')

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "status")



admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductGallery)