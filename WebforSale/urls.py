"""
URL configuration for WebforSale project.

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
from django.contrib import admin, auth
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
import Webtote.views
import Checkout.views
urlpatterns = [
    path("accounts/profile/", Webtote.views.user_profile, name="profile"),
    path("accounts/", include(("django.contrib.auth.urls", "auth"),namespace="accounts")),
    path('profile/edit/', Webtote.views.edit_profile, name='edit_profile'),

    # path("accounts/password_reset/done/",auth.views.PasswordResetDoneView.as_view(),name="password_reset_done",),
    # path("accounts/reset/done/",auth.views.PasswordResetCompleteView.as_view(),name="password_reset_complete",),

    path('admin/', admin.site.urls),
    path("", include("Webtote.urls")),
    path("product/", include("product.urls")),
    path("cart/", include("Cart.urls")),
    path("checkout/", include("Checkout.urls")),
    path('check-discount/', Checkout.views.check_discount, name='check_discount'),
    path("", include("OrderManagement.urls")),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
