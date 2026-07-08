from django.urls import path
from . import views

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
]
