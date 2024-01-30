from django.urls import path
from . import views
urlpatterns = [
    path('buy_ticket/<int:id>/', views.buy_ticket.as_view(), name='buy_ticket'),
    path('buy/<int:tid>/<int:sid>/', views.buy, name='buy'),
    path('edit_schedule/<int:id>/', views.EditScheduleView.as_view(), name='edit_schedule'),
    path('add_schedule/<int:id>/', views.add_schedule, name='add_schedule'),
    path('add_train/', views.addTrain, name='addTrain'),
]