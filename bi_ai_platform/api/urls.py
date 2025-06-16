from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import DatabaseConnectionViewSet, UserCreateView, UserListView, TestDatabaseConnectionView, list_table_data, test_connection, list_connections, create_connection, update_connection, delete_connection, tabela_semantica_view, ImportarPbitView
router = DefaultRouter()
router.register(r'databases', DatabaseConnectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('test_connection/', TestDatabaseConnectionView.as_view(), name='test_connection'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateView.as_view(), name='user_register'),
    path('users/', UserListView.as_view(), name='user_list'),
    path('connections/', list_connections, name='list_connections'),
    path('connections/create/', create_connection, name = 'create_connection'),
    path('connections/update/', update_connection, name = 'update_connection'),
    path('connections/delete/', delete_connection, name = 'delete_connection'),
    path('connections/test/', test_connection, name='test_connection'),
    path("tables/<str:table_name>/", list_table_data, name="list_table_data"),
    path('tabelas-semanticas/', tabela_semantica_view, name='tabelas_semanticas'),
    path("importar-pbit/", ImportarPbitView.as_view(), name="importar-pbit"),
]
