from django.conf.urls import url
from django.urls import path
from chat.consumers import *

channel_routing = [
      # url(r'^', ChatConsumer),
      path("chat/<str:room>/", ChatConsumerA),
      path("chat/<str:room>/<str:user>/", ChatConsumerA)

]