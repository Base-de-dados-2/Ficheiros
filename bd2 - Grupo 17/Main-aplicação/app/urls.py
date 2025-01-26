from django.contrib import admin
from django.urls import path, include  # Corrigir a importação de 'include'
from . import views


urlpatterns = [
    # Página inicial
    path('', views.home, name='pagina_inicial'),

    # Utilizadores
    path('utilizadores/listar', views.utilizadores_listar, name='utilizadores_listar'),
    path('utilizadores/<int:id_utilizador>/', views.utilizadores_listar_id, name='utilizadores_listar_id'),
    path('utilizadores/registar/', views.utilizadores_registar, name='utilizadores_registar'),
    path('utilizadores/editar/<int:id>/', views.utilizadores_atualizar, name='utilizadores_atualizar'),
    path('utilizadores/remover/<int:id>/', views.utilizadores_remover, name='utilizadores_remover'),

    # Clientes
    path('clientes/listar', views.cliente_listar, name='clientes_listar'),
    path('clientes/registar/', views.cliente_registar, name='clientes_registar'),
    path('clientes/<int:id>/', views.cliente_listar_id, name='clientes_listar_id'),
    path('clientes/<int:id>/editar/', views.cliente_atualizar, name='clientes_atualizar'),
    path('clientes/remover/<int:id>/', views.cliente_remover, name='clientes_remover'),


    # Veículos
    path('veiculos/listar', views.veiculos_listar, name='veiculos_listar'),
    path('veiculos/registar', views.veiculos_registar, name='veiculos_registar'),
    path('veiculos/usados', views.veiculos_usados, name='veiculos_usados'),
    path('veiculos/listar/id/<int:id>', views.veiculos_listar_id, name='veiculos_listar_id'),
    path('veiculos/atualizar/<int:id>', views.veiculos_atualizar, name='veiculos_atualizar'),
    path('remover/<int:id>/', views.veiculos_remover, name='veiculos_remover'),


    # Stands
    path('stands/listar', views.stand_listar, name='stand_listar'),
    path('stands/registar', views.stand_registar, name='stand_registar'),
    path('stands/listar/id/<int:id>', views.stand_listar_id, name='stand_listar_id'),
    path('stands/editar/<int:id>', views.stand_atualizar, name='stand_atualizar'),
    path('stand/remover/<int:id>', views.stand_remover, name='stand_remover'),

    # Fornecedor
    path('fornecedor/listar', views.fornecedor_listar, name='fornecedor_listar'),
    path('fornecedor/registar', views.fornecedor_registar, name='fornecedor_registar'),
    path('fornecedor/listar/id/<int:id>', views.fornecedor_listar_id, name='fornecedor_listar_id'),
    path('fornecedor/editar/<int:id>', views.fornecedor_atualizar, name='fornecedor_atualizar'),
    path('fornecedor/remover/<int:id>', views.fornecedor_remover, name='fornecedor_remover'),

    # Vendedor
    path('vendedores/listar', views.vendedor_listar, name='vendedor_listar'),
    path('vendedores/<int:id>/editar/', views.vendedor_atualizar, name='vendedor_atualizar'),
    path('vendedores/<int:id>/', views.vendedor_listar_id, name='vendedor_listar_id'),
    path('vendedores/registar/', views.vendedor_registar, name='vendedor_registar'),
    path('vendedores/<int:id>/remover/', views.vendedor_remover, name='vendedor_remover'),

    # Promoção
    path('promocoes/listar', views.promocao_listar, name='promocao_listar'),
    path('promocoes/<int:id>/', views.promocao_detalhes, name='promocao_detalhes'),
    path('promocoes/registar/', views.promocao_registar, name='promocao_registar'),
    path('promocoes/<int:id>/editar/', views.promocao_atualizar, name='promocao_atualizar'),
    path('promocoes/<int:id>/remover/', views.promocao_remover, name='promocao_remover'),

    # test_drive
    path('testdrive/listar', views.testdrive_listar, name='testdrive_listar'),
    path('testdrive/detalhes/<int:id_testdrive>/', views.testdrive_detalhes, name='testdrive_detalhes'),
    path('testdrive/registar/', views.testdrive_registrar, name='testdrive_registrar'),
    path('testdrive/editar/<int:id_testdrive>/', views.testdrive_atualizar, name='testdrive_atualizar'),
    path('testdrive/remover/<int:id_testdrive>/', views.testdrive_remover, name='testdrive_remover'),

    # Transação
    path('transacoes/listar', views.transacaovenda_listar, name='transacaovenda_listar'),
    path('transacoes/detalhes/<int:id_transacao>/', views.transacaovenda_detalhes, name='transacaovenda_detalhes'),
    path('transacoes/registrar/', views.transacaovenda_registrar, name='transacaovenda_registrar'),
    path('transacoes/atualizar/<int:id_transacao>/', views.transacaovenda_atualizar, name='transacaovenda_atualizar'),
    path('transacoes/remover/<int:id_transacao>/', views.transacaovenda_remover, name='transacaovenda_remover'),

    # manutenção
    path('manutencoes/listar', views.manutencao_listar, name='manutencao_listar'),
    path('manutencoes/<int:id>/', views.manutencao_listar_id, name='manutencao_listar_id'),
    path('manutencoes/registar/', views.manutencao_registar, name='manutencao_registar'),
    path('manutencoes/<int:id>/editar/', views.manutencao_atualizar, name='manutencao_atualizar'),
    path('manutencoes/<int:id>/remover/', views.manutencao_remover, name='manutencao_remover'),

    # Historico de veiculos
    path('historico/listar/', views.historicoveiculo_listar, name='historico_listar'),
    path('historico/registrar/', views.historicoveiculo_registar, name='historico_registrar'),
    path('historico/editar/<str:id_historico>/', views.historicoveiculo_atualizar, name='historico_editar'),
    path('historico/excluir/<str:id_historico>/', views.historicoveiculo_remover, name='historico_excluir'),
    path('detalhes/<str:id_historico>/', views.historicoveiculo_detalhes, name='historico_detalhes'),

   
    # Login
    path('login/', views.login_view, name='login'),  # Página de login
    path('logout/', views.logout_view, name='logout'),  # Página de logout
    path('admin/', admin.site.urls),  # Admin do Django
    path('registar/', views.register_view, name='register'),
    path('perfil/', views.perfil, name='perfil'),


]
