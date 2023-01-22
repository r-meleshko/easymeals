from django.urls import path

from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.index, name='index'),
    path('choose', views.choose, name='choose'),
    path('active', views.active, name='active'),
    path('shopping', views.shopping, name='shopping'),
    path('favorite', views.favorite, name='favorite'),
    path('recipe/<int:recipe_id>/', views.recipe, name='recipe'),
    path('favorite_active_update', views.favorite_active_update, name='favorite_active_update'),
    path('shopping_update', views.shopping_update, name='shopping_update')
]
