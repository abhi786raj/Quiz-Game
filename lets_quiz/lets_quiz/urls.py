from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

schema_view = get_schema_view(
    openapi.Info(
        title="Let's Quiz API",
        default_version='v1',
        description="API documentation for the Let's Quiz Web App",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Configure JWT Authorization
schema_view.security = [
    {
        'Bearer': []
    }
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('api/', include('quiz.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
#     path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
