from django.contrib import admin
from .models import Task
from django.contrib.auth.models import User

# Custom admin site header and title
admin.site.site_header = "TODO App Administration"
admin.site.site_title = "TODO App Admin"
admin.site.index_title = "Welcome to TODO App Admin Portal"


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ['title', 'user', 'completed', 'created_at', 'short_description']

    # Fields that can be used for filtering
    list_filter = ['completed', 'created_at', 'user']

    # Fields that can be searched
    search_fields = ['title', 'description', 'user__username']

    # Fields that can be edited directly from the list view
    list_editable = ['completed']

    # Fields to use for date-based navigation
    date_hierarchy = 'created_at'

    # Fields to display in the detail view with organization
    fieldsets = [
        ('Basic Information', {
            'fields': ['title', 'description', 'user']
        }),
        ('Status', {
            'fields': ['completed']
        }),
        ('Timestamps', {
            'fields': ['created_at'],
            'classes': ['collapse']
        })
    ]

    # Fields that are read-only in the admin
    readonly_fields = ['created_at']

    # Custom admin actions
    actions = ['mark_completed', 'mark_pending']

    def short_description(self, obj):
        """Display shortened description in list view"""
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "-"

    short_description.short_description = "Description"

    def mark_completed(self, request, queryset):
        """Admin action to mark selected tasks as completed"""
        updated = queryset.update(completed=True)
        self.message_user(request, f'{updated} task(s) marked as completed.')

    mark_completed.short_description = "Mark selected tasks as completed"

    def mark_pending(self, request, queryset):
        """Admin action to mark selected tasks as pending"""
        updated = queryset.update(completed=False)
        self.message_user(request, f'{updated} task(s) marked as pending.')

    mark_pending.short_description = "Mark selected tasks as pending"

    def save_model(self, request, obj, form, change):
        """Automatically assign current user if no user is selected"""
        if not obj.user_id:  # Si aucun utilisateur n'est assigné
            obj.user = request.user  # Assigner l'utilisateur connecté
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        """Superusers see all tasks, regular users see only their tasks"""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit user choices for non-superusers"""
        if db_field.name == "user":
            if not request.user.is_superuser:
                # Les utilisateurs normaux ne peuvent choisir que leur propre compte
                kwargs["queryset"] = User.objects.filter(id=request.user.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        """Prevent non-superusers from changing the user after creation"""
        readonly_fields = list(self.readonly_fields)
        if not request.user.is_superuser and obj:
            # Les utilisateurs normaux ne peuvent pas changer l'utilisateur après création
            readonly_fields.append('user')
        return readonly_fields