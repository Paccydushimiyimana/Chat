
from django.urls import path
from .views import *

urlpatterns = [
    path('<str:room_name>/',my_simple_view, name='my_simple'),
    path('<str:room_name>/pass_message/',passing_msg_view, name='passing_msg'),
    path('<str:room_name>/<str:user_name>/', my_db_temp_view, name='my_db_temp'),
    path('<str:room_name>/<str:user_name>/', my_db_text_view, name='my_db_text'),
    path('<str:room_name>/<str:user_name>/', my_temp_view, name='my_temp'),
    path('<str:room_name>/<str:user_name>/', my_text_view, name='my_text'),
]