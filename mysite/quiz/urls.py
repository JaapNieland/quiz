from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/', views.detail_next_question, name='next_question'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
    path('signup/', views.signup, name='signup'),
    path('signoff/', views.signoff, name='signoff'),
    path('score_board/', views.score_board, name='score_board'),
    path('results/<int:question_id>', views.specific_question_results, name='question_results'),
    path('results/', views.active_question_results),
    path('control_panel/', views.control_panel, name='control_panel'),
    path('switch_question_status/', views.switch_question_status, name='switch_question_status'),
    path('current_active_question/', views.currently_active_question, name='current_active_question'),
    path('new_question/', views.create_new_question, name='new_question')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
