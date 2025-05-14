from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from .models import (
    Category, Product, Order, OrderItem, 
    Wishlist, WishlistItem, Review, Coupon,
    Payment, BlogPost, BlogCategory, BlogTag,
    Variation, VariationOption, ProductVariation, Address
)

# Custom admin site
class AngelPlantsAdminSite(AdminSite):
    site_header = "Angel's Plant Shop Administration"
    site_title = "Angel's Plant Shop Admin"
    index_title = "Welcome to Angel's Plant Shop Admin"

# Create an instance of the custom admin site
angel_plants_admin = AngelPlantsAdminSite(name='angel_plants_admin')

# Admin classes
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_category', 'price', 'get_quantity', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at', 'updated_at', 'category']
    list_editable = ['price', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'
    
    def get_category(self, obj):
        return obj.category.name if obj.category else 'No Category'
    get_category.short_description = 'Category'
    get_category.admin_order_field = 'category__name'
    
    def get_quantity(self, obj):
        return obj.quantity
    get_quantity.short_description = 'Qty'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'updated_at', 'payment_status']
    list_filter = ['payment_status', 'created_at', 'updated_at']
    search_fields = ['user__username', 'id']
    inlines = [OrderItemInline]
    ordering = ['-created_at']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity', 'get_cost']
    list_filter = ['order__payment_status', 'order__created_at']
    search_fields = ['order__id', 'product__name']
    raw_id_fields = ['order', 'product']
    list_select_related = ['order', 'product']

class WishlistItemInline(admin.StackedInline):
    model = WishlistItem
    extra = 1
    raw_id_fields = ('product',)
    fields = ('product', 'quantity', 'notes')
    show_change_link = True

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_username', 'get_name', 'get_is_public', 'get_item_count', 'get_created_at', 'get_updated_at']
    list_filter = ['is_public', 'created_at', 'updated_at']
    search_fields = ['user__username', 'name']
    inlines = [WishlistItemInline]
    raw_id_fields = ['user']
    date_hierarchy = 'created_at'
    list_select_related = ['user']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_username(self, obj):
        if obj.user:
            return obj.user.username
        return 'Anonymous'
    get_username.short_description = 'User'
    get_username.admin_order_field = 'user__username'
    
    def get_name(self, obj):
        return obj.name
    get_name.short_description = 'Name'
    get_name.admin_order_field = 'name'
    
    def get_is_public(self, obj):
        return obj.is_public
    get_is_public.boolean = True
    get_is_public.short_description = 'Public'
    get_is_public.admin_order_field = 'is_public'
    
    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.short_description = 'Created At'
    get_created_at.admin_order_field = 'created_at'
    
    def get_updated_at(self, obj):
        return obj.updated_at
    get_updated_at.short_description = 'Updated At'
    get_updated_at.admin_order_field = 'updated_at'
    
    def get_item_count(self, obj):
        return obj.wishlist_items.count()
    get_item_count.short_description = 'Items'
    get_item_count.admin_order_field = 'items_count'
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            items_count=Count('wishlist_items')
        )

class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_wishlist', 'product', 'quantity', 'get_created_at']
    list_filter = ['created_at', 'wishlist__user__username', 'wishlist__name']
    search_fields = [
        'wishlist__user__username', 
        'wishlist__name',
        'product__name',
        'product__description'
    ]
    raw_id_fields = ['product', 'wishlist']
    list_select_related = ['wishlist', 'wishlist__user', 'product']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']
    
    def get_wishlist(self, obj):
        if obj.wishlist:
            return f"{obj.wishlist.name} ({obj.wishlist.user.username if obj.wishlist.user else 'Anonymous'})"
        return 'No Wishlist'
    get_wishlist.short_description = 'Wishlist'
    get_wishlist.admin_order_field = 'wishlist__name'
    
    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.short_description = 'Created At'
    get_created_at.admin_order_field = 'created_at'

# Register models with the default admin site
admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(WishlistItem, WishlistItemAdmin)

# Register models with the custom admin site
angel_plants_admin.register(Category, CategoryAdmin)
angel_plants_admin.register(Product, ProductAdmin)
angel_plants_admin.register(Order, OrderAdmin)
angel_plants_admin.register(OrderItem, OrderItemAdmin)
angel_plants_admin.register(Wishlist, WishlistAdmin)
angel_plants_admin.register(WishlistItem, WishlistItemAdmin)
