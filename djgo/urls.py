from django.contrib import admin
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from django.urls import path, include
from pay.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('convert/', include("guest_user.urls")),
    path('', home, name="home"),
    path('create-prod/', create_prod, name="create-prod"),
    path('delete-prod/<int:id>', delete, name="delete-prod"),
    path('edit-prod/<int:id>', edit, name="edit-prod"),
    path('detail-prod/<int:id>', detail, name="detail-prod"),
    path('cart/', cart, name="cart"),
    path('cart/purchase/', purchase_int, name="purchase"),
    path('add-cart/', add_cart, name="add-cart"),
    path('cart/quantity-cart/', quantity_cart, name="quantity-cart"),
    path('del-cart/', delete_cart, name="del-cart"),
    path('success', complete, name="success"),
    path('session-stat', session_stat, name="session-stat"),
    path('logout/', logout_view, name="logout"),
    path('plan/', plan, name="plan"),
    path('profile/', profile, name="profile"),
    path('profile/refund/', refund, name="refund"),
]
