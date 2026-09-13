from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'signup/',
        views.signup,
        name='signup'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'profile/',
        views.profile,
        name='profile'
    ),

    path(
        'profile/edit/',
        views.edit_profile,
        name='edit_profile'
    ),

    path(
        'skills/add/',
        views.add_skill,
        name='add_skill'
    ),

    path(
        'skills/edit/<int:skill_id>/',
        views.edit_skill,
        name='edit_skill'
    ),

    path(
        'skills/delete/<int:skill_id>/',
        views.delete_skill,
        name='delete_skill'
    ),

    path(
        'search/',
        views.search,
        name='search'
    ),

    path(
        'user/<str:username>/',
        views.user_profile,
        name='user_profile'
    ),

    path(
        'chat/<str:username>/',
        views.chat,
        name='chat'
    ),

    # MESSAGE REQUEST

    path(
        'message-request/<str:username>/',
        views.send_message_request,
        name='send_message_request'
    ),

    path(
        'message-requests/',
        views.message_requests,
        name='message_requests'
    ),

    path(
        'message-request/accept/<int:request_id>/',
        views.accept_message_request,
        name='accept_message_request'
    ),

    path(
        'message-request/reject/<int:request_id>/',
        views.reject_message_request,
        name='reject_message_request'
    ),

    path(
       'unfriend/<str:username>/',
        views.unfriend_user,
        name='unfriend_user'
    ),

    path(
      'block/<str:username>/',
       views.block_user,
       name='block_user'
    ),

    path(
    'unblock/<str:username>/',
    views.unblock_user,
    name='unblock_user'
),

    path(
    'notifications/',
    views.notifications,
    name='notifications'
),

path(
    'connections/',
    views.connections,
    name='connections'
),

path(
    'messages/',
    views.messages,
    name='messages'
),

path(
    'build-together/',
    views.build_together,
    name='build_together'
),

path(
    'build-together/create/',
    views.create_project,
    name='create_project'
),

path(
    'build-together/<int:project_id>/',
    views.project_detail,
    name='project_detail'
),

path(
    'build-together/<int:project_id>/invite/<str:username>/',
    views.invite_to_project,
    name='invite_to_project'
),

   

]