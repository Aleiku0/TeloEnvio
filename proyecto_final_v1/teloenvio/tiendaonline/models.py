from django.db import models
from django.contrib.auth.models import User

class Productor(models.Model):
    nombre_contacto = models.CharField(max_length=100)
    RUT = models.CharField(max_length=100)
    razon_social = models.CharField(max_length=100)
    direccion = models.ForeignKey('Direccion', on_delete=models.CASCADE)
    comuna = models.CharField(max_length=100)
    rubro = models.CharField(max_length=100)

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=20)
    nombre = models.CharField(max_length=100)
    correo_electronico = models.EmailField()
    identificador = models.CharField(max_length=100)
    numIdentificador = models.CharField(max_length=100)
    direccion = models.ForeignKey('Direccion', on_delete=models.CASCADE)
    comuna = models.CharField(max_length=100)

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.PositiveIntegerField()
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/')
    productor = models.ForeignKey(Productor, on_delete=models.SET_NULL, null=True, blank=True)

class Direccion(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    calle = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=100)
    codigo_postal = models.CharField(max_length=10)

class Carrito(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True)
    productos = models.ManyToManyField(Producto, through='ItemCarrito')
    total = models.PositiveIntegerField(default=0)

class ItemCarrito(models.Model):
    carrito = models.ForeignKey(Carrito, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.PositiveIntegerField()

class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    direccion = models.ForeignKey(Direccion, on_delete=models.SET_NULL, null=True)
    productos = models.ManyToManyField(Producto, through='ItemPedido')
    fecha = models.DateTimeField(auto_now_add=True)
    total = models.PositiveIntegerField(default=0)
    creado_por = models.ForeignKey(User, related_name='pedidos_creados', on_delete=models.SET_NULL, null=True)
    metodo_pago = models.CharField(max_length=100)
    estado = models.CharField(max_length=20)

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio = models.PositiveIntegerField()

