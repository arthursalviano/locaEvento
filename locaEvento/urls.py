from django.conf.urls import patterns, include, url
from evento.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Templates:
    url(r'^$', pgInicial),
    url(r'^cadastros/$', pgCadastros),
    url(r'novo/$', pgNovo),
    url(r'detalhes/$',pgDetalhes),
    url(r'deletar/(\d+)/$',deletar),
    url(r'editar/(\d+)/salvarAlteracoes/$',atualizar),
    url(r'editar/(\d+)/$',pgEditar),
    url(r'salvar/$', pgSalvar),
    

    url(r'filtrar/(.+)/(.+)/$',filtrar),
    url(r'pesquisar/(.+)/$',pesquisar),

    #### Acesso direto a metodos
   #url(r'pesquisar/(+w)/(+w)/$',pesquisar),
   



    #url(r'pdf/$', pdfHtmlPisa2),
    #url(r'contrato/$', contrato),

    
    #url(r'^DetalhesTipoEvento$',TrazerTiposDeEvento),
    # url(r'^$', 'locaEvento.views.home', name='home'),
    # url(r'^locaEvento/', include('locaEvento.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
