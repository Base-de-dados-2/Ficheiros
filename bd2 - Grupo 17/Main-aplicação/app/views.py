from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from django.contrib import admin
from django.urls import path, include

# Vistas
from .Vistas.utilizadores_views import *
from .Vistas.clientes_views import *
from .Vistas.veiculos_views import *
from .Vistas.stand_view import *
from .Vistas.fornecedor_views import *
from .Vistas.vendedor_views import *
from .Vistas.promoção_views import *
from .Vistas.historico_veiculos_views import *
from .Vistas.test_drive_views import *
from .Vistas.transação_views import *
from .Vistas.manutençao_views import *
from .Vistas.account_views import *

def home(request):
    return render(request, 'home.html')  # Agora, o template está diretamente em 'templates/'

def custom_404_view(request, exception):
    return render(request, 'error.html', status=404)

HANDLER404 = 'app.views.custom_404_view'
