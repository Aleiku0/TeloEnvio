from django import forms
from .models import Producto, Direccion, Pedido,User,Cliente

class LoginForm(forms.Form):
    username = forms.CharField(label='Usuario', required=True,
                               max_length=50, min_length=5,
                               error_messages={
                                   'required': 'El usuario es obligatorio',
                                   'max_length': 'El usuario no puede superar los 50 caracteres',
                                   'min_length': 'El usuario debe tener al menos 5 caracteres'
                               },
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'Ingrese su usuario',
                                   'class': 'form-control'
                               })
                               )
    password = forms.CharField(label='Contraseña', required=True,
                               max_length=50, min_length=1,
                               error_messages={
                                   'required': 'La contraseña es obligatoria',
                                   'max_length': 'La contraseña no puede superar los 50 caracteres',
                                   'min_length': 'La contraseña debe tener al menos 1 caracter'
                               },
                               widget=forms.PasswordInput(attrs={
                                   'placeholder': 'Ingrese su contraseña',
                                   'class': 'form-control'
                               })
                               )

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion', 'imagen']

class DireccionForm(forms.ModelForm):
    class Meta:
        model = Direccion
        fields = ['calle', 'ciudad', 'codigo_postal']

FORMA_PAGO_CHOICES = [
    ('efectivo', 'Efectivo'),
    ('tarjeta', 'Tarjeta de crédito'),
    ('transferencia', 'Transferencia bancaria'),
]


class PedidoGestionForm(forms.Form):
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), empty_label='Nuevo Cliente', required=False)
    nuevo_cliente_nombre = forms.CharField(max_length=100, required=False)
    nuevo_cliente_direccion = forms.CharField(max_length=100, required=False)
    nuevo_cliente_correo = forms.EmailField(required=False)
    nuevo_cliente_telefono = forms.CharField(max_length=20, required=False)
    productos = forms.ModelMultipleChoiceField(queryset=Producto.objects.all(), widget=forms.CheckboxSelectMultiple)
    cantidades = forms.IntegerField(min_value=1)

class DetallePedidoGestionForm(forms.Form):
    nombre_cliente = forms.CharField(max_length=100, disabled=True)
    direccion_cliente = forms.CharField(max_length=100, disabled=True)
    numero_pedido = forms.CharField(max_length=100, disabled=True)
    productos = forms.CharField(widget=forms.Textarea, disabled=True)
    subtotal = forms.DecimalField(decimal_places=2, disabled=True)
    total = forms.DecimalField(decimal_places=2, disabled=True)




