from django.contrib import admin
from .models import Phone, Category


@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ['phone_name', 'phone_model', 'phone_os', 'phone_status', 'phone_operator', 'phone_storage', 'phone_battery',
                    'phone_date', 'phone_isCompleted', 'phone_isHome', 'phone_isActive', 'phone_isUpdated',
                    'category_list']
    list_filter = ['phone_date', 'phone_isCompleted', 'phone_isUpdated', 'phone_isHome']
    search_fields = ['phone_name', 'phone_model', 'phone_os', 'phone_status', 'phone_operator', 'phone_storage',
                     'phone_battery', 'phone_date', 'phone_isCompleted', 'phone_isUpdated']
    list_editable = ['phone_isCompleted', 'phone_isUpdated', 'phone_isHome', 'phone_date']
    list_per_page = 10
    date_hierarchy = 'phone_date'
    save_as = True
    save_on_top = True
    fieldsets = [
        ('Phone Information', {
            'fields': ['phone_name', 'phone_model', 'phone_os', 'phone_status', 'phone_operator', 'phone_storage',
                       'phone_battery', 'phone_image', 'categories']}),
        ('ADB Information', {
            'fields': ['phone_version_sdk', 'phone_manufacturer', 'phone_hardware', 'phone_platform', 'phone_serial_no',
                       'phone_product_name', 'phone_brand', 'phone_language', 'phone_boot_completed', 'phone_timezone',
                       'phone_sms', 'phone_call', 'phone_wifi', 'phone_bluetooth', 'phone_gps', 'phone_network',
                       'phone_sim', 'phone_battery_status', 'phone_battery_level']}),
        ('Date Information', {'fields': ['phone_date', 'phone_isCompleted', 'phone_isUpdated']})
    ]
    readonly_fields = ['phone_date']
    actions = ['make_completed', 'make_not_completed', 'make_updated', 'make_not_updated']

    def make_completed(self, request, queryset):
        queryset.update(phone_isCompleted=True)
        self.message_user(request, 'Phone(s) has been marked as completed')

    def make_not_completed(self, request, queryset):
        queryset.update(phone_isCompleted=False)
        self.message_user(request, 'Phone(s) has been marked as not completed')

    def make_updated(self, request, queryset):
        queryset.update(phone_isUpdated=True)
        self.message_user(request, 'Phone(s) has been marked as updated')

    def make_not_updated(self, request, queryset):
        queryset.update(phone_isUpdated=False)
        self.message_user(request, 'Phone(s) has been marked as not updated')

    make_completed.short_description = 'Mark as completed'
    make_not_completed.short_description = 'Mark as not completed'
    make_updated.short_description = 'Mark as updated'
    make_not_updated.short_description = 'Mark as not updated'

    def category_list(self, obj):
        html = ""
        for category in obj.categories.all():
            html += category.name + " "
        return html


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'phone_count']
    list_filter = ['name']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_per_page = 10
    save_as = True
    save_on_top = True
    fieldsets = [
        ('Category Information', {'fields': ['name', 'slug']})
    ]
    actions = ['make_slug']

    def make_slug(self, request, queryset):
        queryset.update(slug='slug')
        self.message_user(request, 'Slug has been created')

    make_slug.short_description = 'Create slug'

    # how much phone is in the category
    def phone_count(self, obj):
        return obj.phones.count()

    phone_count.short_description = 'Phone Count'
    phone_count.admin_order_field = 'phones'
