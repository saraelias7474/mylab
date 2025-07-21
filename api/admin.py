from django.contrib import admin
from .models import User, Category, Authors, Book, Review, Order, OrderItem

# إدارة المستخدم
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Role Info', {'fields': ('role',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

# حماية إدارة الكتب: فقط admin
class BookAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.role.lower() == 'admin'

    def has_change_permission(self, request, obj=None):
        return request.user.role.lower() == 'admin'

    def has_delete_permission(self, request, obj=None):
        return request.user.role.lower() == 'admin'

# حماية إدارة المؤلفين
class AuthorsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.role.lower() == 'admin'

    def has_change_permission(self, request, obj=None):
        return request.user.role.lower() == 'admin'

    def has_delete_permission(self, request, obj=None):
        return request.user.role.lower() == 'admin'

# حماية إدارة التصنيفات
class CategoryAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.role.lower() == 'admin'

    def has_change_permission(self, request, obj=None):
        return request.user.role.lower() == 'admin'

    def has_delete_permission(self, request, obj=None):
        return request.user.role.lower()== 'admin'


# تسجيل بقية النماذج بشكل عادي
admin.site.register(Book, BookAdmin)
admin.site.register(Authors, AuthorsAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)

