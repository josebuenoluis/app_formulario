from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.files.base import ContentFile
from django.contrib.auth.base_user import BaseUserManager
from mensajeria.utils import generar_qr_vendedor_bytes
from django.utils.text import slugify
import uuid
from django.conf import settings
# Create your models here.




class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, **extra_fields)

class Users(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=200,null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=200,null=True)
    codigo_qr = models.ImageField(upload_to='qrs_vendedores/', blank=True, null=True)
    state = models.CharField(max_length=200,null=True)
    country = models.CharField(max_length=100,null=True)
    zip_code = models.CharField(max_length=20, db_index=True,null=True)
    slug = models.SlugField(
        max_length=150,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def save(self, *args, **kwargs):
        if not self.slug:
            nombre_base = f"{self.first_name} {self.last_name}".strip()
            if not nombre_base:
                nombre_base = self.email.split("@")[0]

            base = slugify(nombre_base)
            # Añade 4 caracteres únicos garantizando que nunca colisionen
            while True:
                codigo = uuid.uuid4().hex[:4]
                candidato = f"{base}-{codigo}"
                if not Users.objects.filter(slug=candidato).exists():
                    self.slug = candidato
                    break
        # 2. Genera y guarda la imagen PNG usando tu función auxiliar
        if not self.codigo_qr and self.slug:
            qr_bytes = generar_qr_vendedor_bytes(self.slug)
            nombre_archivo = f"qr_{self.slug}.png"
            self.codigo_qr.save(nombre_archivo, ContentFile(qr_bytes), save=False)            
        super().save(*args, **kwargs)

    def regenerar_qr(self):
        # 1. Elimina el archivo de imagen anterior de media/qrs_vendedores/
        if self.codigo_qr:
            self.codigo_qr.delete(save=False)
            self.codigo_qr = None

        # 2. Vacía el slug para que save() genere uno completamente nuevo
        self.slug = None

        # 3. Guarda para disparar la generación del nuevo slug y nuevo QR
        self.save()
        
    class Meta:
        db_table = 'Users'
        verbose_name = "Vendedor"
        verbose_name_plural = "Vendedores"