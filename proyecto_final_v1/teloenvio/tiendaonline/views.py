from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Sum, F
from django.contrib.auth.decorators import login_required
from django.views import View
from django.views.generic import TemplateView
from .forms import  LoginForm, DireccionForm, ProductoForm
from .models import Producto, Carrito, Pedido, Direccion, ItemCarrito, Cliente,ItemPedido


def home(request):
    return render(request, 'tiendaonline/index.html')


class LoginUsuarioView(TemplateView):
    template_name = 'registration/login.html'

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('home')
            form.add_error('username', 'Credenciales incorrectas')
            return render(request, self.template_name, {"form": form})
        else:
            return render(request, self.template_name, {"form": form})

#################################### VISTAS AGREGAR CARRITO CLIENTE #############################

def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tiendaonline/lista_productos.html', {'productos': productos})


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    return render(request, 'tiendaonline/detalle_producto.html', {'producto': producto})


class CrearProductoView(TemplateView):
    template_name = 'tiendaonline/crear_producto.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductoForm()
        context['productos'] = Producto.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('crear_producto')
        else:
            context = self.get_context_data(form=form)
            return self.render_to_response(context)

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('crear_producto')

@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    # Obtener la cantidad deseada de productos del cuerpo de la solicitud
    cantidad = int(request.POST.get('cantidad', 1))

    if cantidad < 1:
        return HttpResponseBadRequest('La cantidad debe ser mayor o igual a 1')

    # Obtener el precio del producto o establecer un valor predeterminado si no se proporciona
    precio = producto.precio if producto.precio else 0

    # Verificar si el producto ya está en el carrito
    item = carrito.itemcarrito_set.filter(producto=producto).first()

    if item:
        # Si el producto ya existe en el carrito, se actualiza la cantidad
        item.cantidad += cantidad
        item.save()
    else:
        # Si el producto no está en el carrito, se crea un nuevo item
        item = ItemCarrito.objects.create(carrito=carrito, producto=producto, cantidad=cantidad, precio=precio)

    # Actualizar el total del carrito
    carrito.total = carrito.itemcarrito_set.aggregate(total=Sum(F('cantidad') * F('precio')))['total'] or 0
    carrito.save()

    return redirect('carrito')

@login_required
def quitar_del_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito = get_object_or_404(Carrito, usuario=request.user)

    carrito.productos.remove(producto)
    carrito.save()

    return redirect('carrito')


@login_required
def carrito(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    items = carrito.itemcarrito_set.all()
    total = 0

    for item in items:
        subtotal = item.precio * item.cantidad
        total += subtotal
        item.subtotal = subtotal

    return render(request, 'tiendaonline/carrito.html', {'carrito': carrito, 'items': items, 'total': total})

def realizar_pedido(request):
    carrito = get_object_or_404(Carrito, usuario=request.user)
    direcciones = Direccion.objects.filter(usuario=request.user)

    if request.method == 'POST':
        direccion_id = request.POST.get('direccion_id')

        if direccion_id:
            direccion = get_object_or_404(Direccion, id=direccion_id, usuario=request.user)
        else:
            form = DireccionForm(request.POST)

            if form.is_valid():
                direccion = form.save(commit=False)
                direccion.usuario = request.user
                direccion.save()
            else:
                return render(request, 'tiendaonline/realizar_pedido.html', {'form': form, 'direcciones': direcciones})

        pedido = Pedido.objects.create(cliente=request.user, direccion=direccion, total=carrito.total, creado_por=request.user)

        for item in carrito.itemcarrito_set.all():
            pedido.productos.add(item.producto, through_defaults={'cantidad': item.cantidad, 'precio': item.precio})

        carrito.productos.clear()
        carrito.save()

        return redirect('detalle_pedido', pedido_id=pedido.id)

    else:
        form = DireccionForm()

    return render(request, 'tiendaonline/realizar_pedido.html', {'form': form, 'direcciones': direcciones})


def agregar_direccion(request):
    if request.method == 'POST':
        form = DireccionForm(request.POST)

        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.usuario = request.user
            direccion.save()

            return redirect('realizar_pedido')
    else:
        form = DireccionForm()

    return render(request, 'tiendaonline/agregar_direccion.html', {'form': form})


def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    return render(request, 'tiendaonline/detalle_pedido.html', {'pedido': pedido})


    
##################################### GESTION ########################################
def gestion_productos(request):
    productos = Producto.objects.all()
    return render(request, 'tiendaonline/gestion_productos.html', {'productos': productos})

def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect('gestion_productos')

def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('gestion_productos')
    else:
        form = ProductoForm()
    return render(request, 'tiendaonline/agregar_producto.html', {'form': form})

################################## HISTORIAL PEDIDO ##################################

from .models import Pedido

def historial_pedidos(request):
    pedidos = Pedido.objects.all()
    return render(request, 'tiendaonline/historial_pedidos.html', {'pedidos': pedidos})

#######################################################################################
