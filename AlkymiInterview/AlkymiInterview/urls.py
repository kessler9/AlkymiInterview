from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from django.contrib import admin
from AlkymiInterview.user import UserViewSet
from TemporalProcessor.views import FileApiView, FileViewSet, RowViewSet, TemporalViewSet, FileApiDetailView
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('files', FileViewSet)
router.register('rows', RowViewSet)
router.register('temporals', TemporalViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('v1/table', FileApiView.as_view()),
    path('v1/table/<str:uid>', FileApiDetailView.as_view()),
    path('docs/', include_docs_urls(title='Temporal Processor', permission_classes=[])),
    path('api-token-auth/', obtain_auth_token)
]
