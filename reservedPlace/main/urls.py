from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('add-post', views.CreatePostView.as_view()),
    path('main', views.Main.as_view(), name='main_g'),
    path('post_id/<int:pk>', views.comments),
    path('tasks/reset_game', views.reset_game, name='reset'),

    path('tasks', views.HomeTasks.as_view(), name='tasks'),
    path('tasks/1', views.TasksOne, name='auth'),
    path('tasks/2', views.TasksTwo, name='setting'),
    path('del_cookies', views.del_cookies),
    path('del_session', views.del_session),
    path('tasks/2', views.TasksTwo),
    path('exit', views.exit_cookies),
    path('tasks/3', views.TasksThree, name='game'),
    path('tasks/3&reset', views.RESET),
    path('tasks/5', views.TasksFive),
    path('tasks/8', views.TasksEight.as_view()),
    path('tasks/9', views.TasksNine.as_view()),
    path('tasks/11', views.Tasks11),
    path('tasks/12', views.TasksTwelve.as_view()),
    path('tasks/13', views.TasksThirteen.as_view()),
    path('tasks/14', views.TasksFourteen),
    path('tasks/15', views.TasksFifteen),
    path('tasks/17', views.TasksSaventeen),
    path('tasks/18', views.Tasks18),
    path('tasks/19', views.taskNineteen, name='game_city'),
    path('tasks/20', views.TasksTwenty.as_view()),

]
