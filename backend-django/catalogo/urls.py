from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from . import seo, views
from .admin_views import (
    CategoriaServicioAdminViewSet, EventoAdminViewSet, EventoTipoAdminViewSet,
    FotoEventoAdminViewSet, PostAdminViewSet, ServicioAdminViewSet, TagAdminViewSet,
)

admin_router = SimpleRouter()
admin_router.register('categorias-servicio', CategoriaServicioAdminViewSet, basename='admin-categoria-servicio')
admin_router.register('servicios', ServicioAdminViewSet, basename='admin-servicio')
admin_router.register('evento-tipos', EventoTipoAdminViewSet, basename='admin-evento-tipo')
admin_router.register('eventos', EventoAdminViewSet, basename='admin-evento')
admin_router.register('fotos-evento', FotoEventoAdminViewSet, basename='admin-foto-evento')
admin_router.register('tags', TagAdminViewSet, basename='admin-tag')
admin_router.register('posts', PostAdminViewSet, basename='admin-post')

urlpatterns = [
    path('categorias-servicio/', views.CategoriaServicioList.as_view()),
    path('servicios/', views.ServicioList.as_view()),
    path('servicios/<uuid:pk>/', views.ServicioDetail.as_view()),
    path('evento-tipos/', views.EventoTipoList.as_view()),
    path('eventos/', views.EventoList.as_view()),
    path('eventos/<uuid:pk>/fotos/', views.FotoEventoList.as_view()),
    path('eventos/<slug:slug>/', views.EventoDetail.as_view()),
    path('posts/', views.PostList.as_view()),
    path('posts/<slug:slug>/', views.PostDetail.as_view()),
    path('tags/', views.TagList.as_view()),
    path('cotizaciones/', views.CotizacionCreate.as_view()),
    path('imagenes/<uuid:pk>/', views.imagen_archivo_raw),
    path('auth/token/', obtain_auth_token),
    path('robots.txt', seo.robots_txt),
    path('sitemap.xml', seo.sitemap_xml),
    path('admin/', include(admin_router.urls)),
]
