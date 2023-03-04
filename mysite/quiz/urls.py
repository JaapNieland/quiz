from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('detail/<int:question_id>', views.detail, name='detail_specific_question'),
    path('detail/', views.detail_next_question, name='next_question'),
    path('vote/<int:question_id>/', views.vote, name='vote'),
    path('signup/', views.signup, name='signup'),
    path('signoff/', views.signoff, name='signoff'),
    path('score_board/', views.score_board, name='score_board'),
    path('results/<int:question_id>', views.question_results, name='question_results'),
    path('control_panel/', views.control_panel, name='control_panel'),
    path('switch_question_status/', views.switch_question_status, name='switch_question_status')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
