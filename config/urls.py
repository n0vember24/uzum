from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

schema_view = get_schema_view(Info('Uzum Copy', 'V1'), public=True, permission_classes=[AllowAny])

token_urls = [
	path('', TokenObtainPairView.as_view()),
	path('refresh/', TokenRefreshView.as_view()),
	path('verify/', TokenVerifyView.as_view()),
]

urlpatterns = [
	path('', schema_view.with_ui('swagger', cache_timeout=0)),
	path('', include('uzum.urls')),
	path('', include('rest_framework.urls')),
	path('accounts/', include('accounts.urls')),
	path('token/', include(token_urls)),
	path('admin/', admin.site.urls),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
