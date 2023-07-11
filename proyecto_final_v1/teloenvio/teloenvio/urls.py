"""
URL configuration for teloenvio project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tiendaonline import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from tiendaonline.views import home,LoginUsuarioView,CrearProductoView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('login/', LoginUsuarioView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('productos/', views.lista_productos, name='lista_productos'),
    path('producto/<int:producto_id>/', views.detalle_producto, name='detalle_producto'),
    path('crear_producto/', CrearProductoView.as_view(), name='crear_producto'),
    path('agregar_al_carrito/<int:producto_id>/', views.agregar_al_carrito, name='agregar_al_carrito'),
    path('quitar_del_carrito/<int:producto_id>/', views.quitar_del_carrito, name='quitar_del_carrito'),
    path('carrito/', views.carrito, name='carrito'),
    path('realizar_pedido/', views.realizar_pedido, name='realizar_pedido'),
    path('pedido/<int:pedido_id>/', views.detalle_pedido, name='detalle_pedido'),
    path('agregar_direccion/',views.agregar_direccion, name='agregar_direccion'),
    path('historial_pedidos/', views.historial_pedidos, name='historial_pedidos'),
    path('gestion_productos/', views.gestion_productos, name='gestion_productos'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    # path('editar_producto/<int:producto_id>/', views.editar_producto, name='editar_producto'),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
