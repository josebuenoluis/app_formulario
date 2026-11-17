# users/admin.py
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.shortcuts import get_object_or_404, redirect
from django.urls import path, reverse
from django.utils.html import format_html
from django.conf import settings
from .models import Users


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'phone')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = Users
        fields = ('email', 'first_name', 'last_name', 'phone', 'slug', 'is_active', 'is_staff', 'is_superuser')


@admin.register(Users)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = Users

    list_display = (
        'email',
        'first_name',
        'last_name',
        'enlace_formulario',
        'qr_en_tabla',
        'is_active',
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone', 'slug')
    ordering = ('email',)
    readonly_fields = ('enlace_formulario', 'vista_previa_qr', 'last_login', 'date_joined')
    actions = ['accion_regenerar_qr']

    # URL interna del Admin para el botón de regenerar
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:user_id>/regenerar-qr/',
                self.admin_site.admin_view(self.vista_regenerar_qr),
                name='users_regenerar_qr',
            ),
        ]
        return custom_urls + urls

    def vista_regenerar_qr(self, request, user_id):
        usuario = get_object_or_404(Users, pk=user_id)
        # Seguridad: un vendedor normal solo puede regenerar su propio QR
        if not request.user.is_superuser and request.user.id != usuario.id:
            self.message_user(request, "No tienes permiso para modificar este QR.", level=messages.ERROR)
            return redirect('admin:users_users_changelist')

        usuario.regenerar_qr()
        self.message_user(
            request,
            f"QR eliminado y regenerado con éxito. Nuevo enlace: /{usuario.slug}",
            level=messages.SUCCESS
        )
        return redirect('admin:users_users_change', user_id)

    @admin.action(description="Eliminar QR actual y generar nuevo enlace + QR")
    def accion_regenerar_qr(self, request, queryset):
        for usuario in queryset:
            usuario.regenerar_qr()
        self.message_user(request, f"Se han regenerado {queryset.count()} enlaces y códigos QR.", level=messages.SUCCESS)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(id=request.user.id)

    def get_readonly_fields(self, request, obj=None):
        if not request.user.is_superuser:
            return ('email', 'slug', 'enlace_formulario', 'vista_previa_qr', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined')
        return self.readonly_fields

    fieldsets = (
        ('Mi Código QR y Enlace', {
            'fields': ('enlace_formulario', 'vista_previa_qr'),
        }),
        ('Información Personal', {
            'fields': ('email', 'first_name', 'last_name', 'phone', 'slug')
        }),
        ('Dirección', {
            'fields': ('address', 'city', 'state', 'country', 'zip_code'),
            'classes': ('collapse',),
        }),
        ('Seguridad y Permisos', {
            'fields': ('password', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    def enlace_formulario(self, obj):
        if not obj.slug:
            return "Se generará al guardar"
        base_url = getattr(settings, "FRONTEND_BASE_URL", "https://contacto.seguros.com").rstrip("/")
        url = f"{base_url}/contacto/{obj.slug}"
        return format_html('<a href="{}" target="_blank" style="font-weight:bold;">{}</a>', url, url)
    enlace_formulario.short_description = "Enlace Directo"

    def qr_en_tabla(self, obj):
        if not obj.codigo_qr:
            return "-"
        return format_html(
            '<div style="display:flex;align-items:center;gap:10px;">'
            '<img src="{}" width="80" height="80" style="border:1px solid #cbd5e1;border-radius:6px;background:#fff;padding:4px;" />'
            '<a href="{}" download="qr_{}.png" style="background:#0f172a;color:#fff;padding:6px 10px;border-radius:4px;text-decoration:none;font-weight:bold;">Descargar</a>'
            '</div>',
            obj.codigo_qr.url,
            obj.codigo_qr.url,
            obj.slug,
        )
    qr_en_tabla.short_description = "Código QR"

    def vista_previa_qr(self, obj):
        if not obj.pk:
            return "Guarda el usuario primero para generar su código QR."

        url_regenerar = reverse('admin:users_regenerar_qr', args=[obj.pk])

        if not obj.codigo_qr:
            return format_html(
                '<a href="{}" style="background:#0f172a;color:#fff;padding:8px 16px;border-radius:6px;text-decoration:none;font-weight:bold;">Generar Código QR</a>',
                url_regenerar
            )

        return format_html(
            '<div style="padding:16px;background:#fff;border:1px solid #e2e8f0;border-radius:12px;display:inline-block;text-align:center;">'
            '<img src="{}" width="250" height="250" style="display:block;margin:0 auto;" />'
            '<div style="margin-top:14px;display:flex;gap:10px;justify-content:center;">'
            '<a href="{}" download="qr_{}.png" style="background:#0f172a;color:#fff;padding:8px 14px;border-radius:6px;text-decoration:none;font-weight:bold;">Descargar PNG</a>'
            '<a href="{}" onclick="return confirm(\'¿Seguro que quieres eliminar este QR? El enlace anterior dejará de funcionar y se creará uno nuevo.\');" '
            'style="background:#dc2626;color:#fff;padding:8px 14px;border-radius:6px;text-decoration:none;font-weight:bold;">Eliminar y generar nuevo</a>'
            '</div>'
            '</div>',
            obj.codigo_qr.url,
            obj.codigo_qr.url,
            obj.slug,
            url_regenerar,
        )
    vista_previa_qr.short_description = "Código QR y Acciones"