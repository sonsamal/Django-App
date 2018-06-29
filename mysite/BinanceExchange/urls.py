from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='index'),
    path('\checkBalances',views.checkBalances,name='checkBalances'),
    path('marketPlace',views.marketPlace,name='marketPlace'),
    path('finalsell',views.finalsell,name="finalsell"),
]