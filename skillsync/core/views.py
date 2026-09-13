from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile, Skill, Message, MessageRequest, Notification, Project
from django.db.models import Q


# HOME
def home(request):
    return render(request, 'home.html')


# SIGNUP
def signup(request):

    if request.method == 'POST':

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        # Password length
        if len(password) < 6:
            return render(request, 'signup.html', {
                'error': 'Password must be at least 6 characters long'
            })

        # Password confirmation
        if password != confirm_password:
            return render(request, 'signup.html', {
                'error': 'Passwords do not match'
            })

        # Username check
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {
                'error': 'Username already exists'
            })

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(request, 'signup.html')


# LOGIN
def user_login(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            return render(request, 'login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'login.html')


# LOGOUT
def user_logout(request):

    logout(request)

    return redirect('home')


# MY PROFILE
@login_required
def profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    teach_skills = Skill.objects.filter(
        user=request.user,
        skill_type='teach'
    )

    learn_skills = Skill.objects.filter(
        user=request.user,
        skill_type='learn'
    )

    return render(request, 'profile.html', {
        'profile': profile,
        'teach_skills': teach_skills,
        'learn_skills': learn_skills,
    })


# USER PROFILE
@login_required
def user_profile(request, username):

    profile_user = get_object_or_404(
        User,
        username=username
    )

    profile, created = Profile.objects.get_or_create(
        user=profile_user
    )

    teach_skills = Skill.objects.filter(
        user=profile_user,
        skill_type='teach'
    )

    learn_skills = Skill.objects.filter(
        user=profile_user,
        skill_type='learn'
    )

    connection_status = None
    connection_request = None

    # Don't show connection options on own profile
    if profile_user != request.user:

        # BLOCKED
        blocked_request = MessageRequest.objects.filter(
            Q(
                sender=request.user,
                receiver=profile_user
            )
            |
            Q(
                sender=profile_user,
                receiver=request.user
            ),
            status='blocked'
        ).first()

        if blocked_request:

            connection_status = 'blocked'
            connection_request = blocked_request

        else:

            # Request sent by current user
            sent_request = MessageRequest.objects.filter(
                sender=request.user,
                receiver=profile_user,
                status='pending'
            ).first()

            # Request received by current user
            received_request = MessageRequest.objects.filter(
                sender=profile_user,
                receiver=request.user,
                status='pending'
            ).first()

            # Accepted connection
            accepted_request = MessageRequest.objects.filter(
                Q(
                    sender=request.user,
                    receiver=profile_user
                )
                |
                Q(
                    sender=profile_user,
                    receiver=request.user
                ),
                status='accepted'
            ).first()

            if accepted_request:

                connection_status = 'connected'
                connection_request = accepted_request

            elif sent_request:

                connection_status = 'sent'
                connection_request = sent_request

            elif received_request:

                connection_status = 'received'
                connection_request = received_request

            else:

                connection_status = 'none'

    return render(request, 'user_profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'teach_skills': teach_skills,
        'learn_skills': learn_skills,
        'connection_status': connection_status,
        'connection_request': connection_request,
    })


# EDIT PROFILE
@login_required
def edit_profile(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    if request.method == 'POST':

        # About Me
        profile.bio = request.POST.get(
            'bio',
            ''
        )

        # Skills
        skills_to_teach = request.POST.get(
            'skills_to_teach',
            ''
        )

        skills_to_learn = request.POST.get(
            'skills_to_learn',
            ''
        )

        # Save skills in Profile
        profile.skills_to_teach = skills_to_teach
        profile.skills_to_learn = skills_to_learn

        # Profile picture
        if request.FILES.get('profile_image'):

            profile.profile_image = request.FILES[
                'profile_image'
            ]

        # Save Profile
        profile.save()

        # UPDATE TEACH SKILLS
        Skill.objects.filter(
            user=request.user,
            skill_type='teach'
        ).delete()

        teach_skills = skills_to_teach.split(',')

        for skill in teach_skills:

            skill = skill.strip()

            if skill:

                Skill.objects.create(
                    user=request.user,
                    name=skill,
                    skill_type='teach'
                )

        # UPDATE LEARN SKILLS
        Skill.objects.filter(
            user=request.user,
            skill_type='learn'
        ).delete()

        learn_skills = skills_to_learn.split(',')

        for skill in learn_skills:

            skill = skill.strip()

            if skill:

                Skill.objects.create(
                    user=request.user,
                    name=skill,
                    skill_type='learn'
                )

        return redirect('profile')

    return render(request, 'edit_profile.html', {
        'profile': profile
    })


# ADD SKILL
@login_required
def add_skill(request):

    if request.method == 'POST':

        skill_name = request.POST.get(
            'skill_name'
        )

        skill_type = request.POST.get(
            'skill_type'
        )

        if skill_name and skill_type:

            Skill.objects.create(
                user=request.user,
                name=skill_name,
                skill_type=skill_type
            )

        return redirect('dashboard')

    return render(request, 'add_skill.html')


# EDIT SKILL
@login_required
def edit_skill(request, skill_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    if request.method == 'POST':

        old_name = skill.name

        new_name = request.POST.get(
            'skill_name'
        )

        new_type = request.POST.get(
            'skill_type'
        )

        skill.name = new_name
        skill.skill_type = new_type
        skill.save()

        profile = Profile.objects.get(
            user=request.user
        )

        # TEACH SKILL
        if skill.skill_type == 'teach':

            skills = [
                s.strip()
                for s in profile.skills_to_teach.split(',')
                if s.strip()
            ]

            if old_name in skills:
                skills.remove(old_name)

            skills.append(new_name)

            profile.skills_to_teach = ', '.join(
                skills
            )

        # LEARN SKILL
        else:

            skills = [
                s.strip()
                for s in profile.skills_to_learn.split(',')
                if s.strip()
            ]

            if old_name in skills:
                skills.remove(old_name)

            skills.append(new_name)

            profile.skills_to_learn = ', '.join(
                skills
            )

        profile.save()

        return redirect('dashboard')

    return render(request, 'edit_skill.html', {
        'skill': skill
    })


# DELETE SKILL
@login_required
def delete_skill(request, skill_id):

    skill = get_object_or_404(
        Skill,
        id=skill_id,
        user=request.user
    )

    if request.method == 'POST':

        profile = Profile.objects.get(
            user=request.user
        )

        # DELETE TEACH SKILL
        if skill.skill_type == 'teach':

            skills = [
                s.strip()
                for s in profile.skills_to_teach.split(',')
                if s.strip()
            ]

            if skill.name in skills:
                skills.remove(skill.name)

            profile.skills_to_teach = ', '.join(
                skills
            )

        # DELETE LEARN SKILL
        else:

            skills = [
                s.strip()
                for s in profile.skills_to_learn.split(',')
                if s.strip()
            ]

            if skill.name in skills:
                skills.remove(skill.name)

            profile.skills_to_learn = ', '.join(
                skills
            )

        profile.save()

        skill.delete()

    return redirect('dashboard')


# DASHBOARD
@login_required
def dashboard(request):

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )

    teach_skills = Skill.objects.filter(
        user=request.user,
        skill_type='teach'
    )

    learn_skills = Skill.objects.filter(
        user=request.user,
        skill_type='learn'
    )

    return render(request, 'dashboard.html', {
        'profile': profile,
        'teach_skills': teach_skills,
        'learn_skills': learn_skills,
    })


# SEARCH USERS
@login_required
def search(request):

    query = request.GET.get(
        'q',
        ''
    ).strip()

    users = User.objects.none()

    if query:

        users = User.objects.filter(

            Q(
                username__icontains=query
            )

            |

            Q(
                profile__bio__icontains=query
            )

            |

            Q(
                skills__name__icontains=query
            )

        ).exclude(
            id=request.user.id
        ).distinct()

    return render(request, 'search_results.html', {
        'query': query,
        'users': users,
    })


# CHAT
@login_required
def chat(request, username):

    other_user = get_object_or_404(
        User,
        username=username
    )

    # Don't chat with yourself
    if other_user == request.user:

        return redirect('dashboard')

    # Check if users are blocked
    is_blocked = MessageRequest.objects.filter(

        Q(
            sender=request.user,
            receiver=other_user
        )

        |

        Q(
            sender=other_user,
            receiver=request.user
        ),

        status='blocked'

    ).exists()

    if is_blocked:

        return redirect(
            'user_profile',
            username=other_user.username
        )

    # Check accepted connection
    is_connected = MessageRequest.objects.filter(

        Q(
            sender=request.user,
            receiver=other_user
        )

        |

        Q(
            sender=other_user,
            receiver=request.user
        ),

        status='accepted'

    ).exists()

    # Only connected users can chat
    if not is_connected:

        return redirect(
            'user_profile',
            username=other_user.username
        )

    messages = Message.objects.filter(

        Q(
            sender=request.user,
            receiver=other_user
        )

        |

        Q(
            sender=other_user,
            receiver=request.user
        )

    ).order_by('created_at')

    # SEND MESSAGE
    if request.method == 'POST':

        content = request.POST.get(
            'content',
            ''
        ).strip()

        if content:

            # Save message
            new_message = Message.objects.create(
                sender=request.user,
                receiver=other_user,
                content=content
            )

            # Create notification
            Notification.objects.create(
                recipient=other_user,
                sender=request.user,
                message=new_message,
                notification_type='message'
            )

        return redirect(
            'chat',
            username=other_user.username
        )

    return render(request, 'chat.html', {
        'other_user': other_user,
        'messages': messages,
    })


# SEND MESSAGE REQUEST
@login_required
def send_message_request(request, username):

    receiver = get_object_or_404(
        User,
        username=username
    )

    # Don't send request to yourself
    if receiver == request.user:

        return redirect('search')

    # Check existing request
    existing_request = MessageRequest.objects.filter(

        Q(
            sender=request.user,
            receiver=receiver
        )

        |

        Q(
            sender=receiver,
            receiver=request.user
        )

    ).first()

    # Request already exists
    if existing_request:

        return redirect(
            'user_profile',
            username=username
        )

    # Create new connection request
    new_request = MessageRequest.objects.create(
        sender=request.user,
        receiver=receiver,
        status='pending'
    )

    # Create notification for receiver
    Notification.objects.create(
        recipient=receiver,
        sender=request.user,
        notification_type='connection_request'
    )

    return redirect(
        'user_profile',
        username=username
    )


# MESSAGE REQUESTS
@login_required
def message_requests(request):

    requests = MessageRequest.objects.filter(
        receiver=request.user,
        status='pending'
    ).order_by('-created_at')

    return render(request, 'message_requests.html', {
        'requests': requests
    })

# ACCEPT REQUEST
@login_required
def accept_message_request(request, request_id):

    message_request = get_object_or_404(
        MessageRequest,
        id=request_id,
        receiver=request.user
    )

    message_request.status = 'accepted'
    message_request.save()

    # Send notification to the person who sent the request
    Notification.objects.create(
        recipient=message_request.sender,
        sender=request.user,
        notification_type='connection_accepted'
    )

    return redirect('message_requests')


# REJECT REQUEST
@login_required
def reject_message_request(request, request_id):

    message_request = get_object_or_404(
        MessageRequest,
        id=request_id,
        receiver=request.user
    )

    message_request.delete()

    return redirect('message_requests')


# UNFRIEND
@login_required
def unfriend_user(request, username):

    user_to_unfriend = get_object_or_404(
        User,
        username=username
    )

    if user_to_unfriend == request.user:

        return redirect('dashboard')

    if request.method == 'POST':

        MessageRequest.objects.filter(

            Q(
                sender=request.user,
                receiver=user_to_unfriend
            )

            |

            Q(
                sender=user_to_unfriend,
                receiver=request.user
            ),

            status='accepted'

        ).delete()

    return redirect(
        'user_profile',
        username=user_to_unfriend.username
    )


# BLOCK USER
@login_required
def block_user(request, username):

    user_to_block = get_object_or_404(
        User,
        username=username
    )

    if user_to_block == request.user:

        return redirect('dashboard')

    if request.method == 'POST':

        connection = MessageRequest.objects.filter(

            Q(
                sender=request.user,
                receiver=user_to_block
            )

            |

            Q(
                sender=user_to_block,
                receiver=request.user
            )

        )

        if connection.exists():

            connection.update(
                status='blocked'
            )

        else:

            MessageRequest.objects.create(
                sender=request.user,
                receiver=user_to_block,
                status='blocked'
            )

    return redirect(
        'user_profile',
        username=user_to_block.username
    )

# UNBLOCK USER
@login_required
def unblock_user(request, username):

    user_to_unblock = get_object_or_404(
        User,
        username=username
    )

    if request.method == 'POST':

        MessageRequest.objects.filter(
            Q(
                sender=request.user,
                receiver=user_to_unblock
            )
            |
            Q(
                sender=user_to_unblock,
                receiver=request.user
            ),
            status='blocked'
        ).delete()

    return redirect(
        'user_profile',
        username=user_to_unblock.username
    )

# NOTIFICATIONS
@login_required
def notifications(request):

    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-created_at')

    return render(
        request,
        'notifications.html',
        {
            'notifications': notifications
        }
    )

# MY CONNECTIONS
@login_required
def connections(request):

    # Find all accepted connection requests involving
    # the currently logged-in user.
    accepted_requests = MessageRequest.objects.filter(
        Q(
            sender=request.user,
            status='accepted'
        )
        |
        Q(
            receiver=request.user,
            status='accepted'
        )
    ).select_related(
        'sender',
        'receiver'
    ).order_by('-created_at')

    # Convert requests into the actual connected users.
    connected_users = []

    for connection in accepted_requests:

        if connection.sender == request.user:
            connected_user = connection.receiver
        else:
            connected_user = connection.sender

        # Prevent duplicate users from appearing.
        if connected_user not in connected_users:
            connected_users.append(connected_user)

    return render(
        request,
        'connections.html',
        {
            'connections': connected_users,
        }
    )

# MESSAGES LIST
@login_required
def messages(request):

    accepted_requests = MessageRequest.objects.filter(
        Q(sender=request.user, status='accepted')
        |
        Q(receiver=request.user, status='accepted')
    ).select_related(
        'sender',
        'receiver'
    )

    conversation_users = []

    for connection in accepted_requests:

        if connection.sender_id == request.user.id:
            other_user = connection.receiver
        else:
            other_user = connection.sender

        if other_user not in conversation_users:
            conversation_users.append(other_user)

    return render(
        request,
        'messages.html',
        {
            'conversation_users': conversation_users,
        }
    )
# BUILD TOGETHER
@login_required
def build_together(request):

    accepted_requests = MessageRequest.objects.filter(
        Q(sender=request.user, status='accepted')
        |
        Q(receiver=request.user, status='accepted')
    ).select_related(
        'sender',
        'receiver'
    )

    connections = []

    for connection in accepted_requests:

        if connection.sender_id == request.user.id:
            connected_user = connection.receiver
        else:
            connected_user = connection.sender

        if connected_user not in connections:
            connections.append(connected_user)

    projects = Project.objects.filter(
        owner=request.user
    ).order_by('-created_at')

    return render(
        request,
        'build_together.html',
        {
            'connections': connections,
            'projects': projects,
        }
    )

# CREATE PROJECT
@login_required
def create_project(request):

    if request.method == 'POST':

        title = request.POST.get(
            'title',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        required_skills = request.POST.get(
            'required_skills',
            ''
        ).strip()

        if title:

            project = Project.objects.create(
                owner=request.user,
                title=title,
                description=description,
                required_skills=required_skills
            )

            # Project owner automatically becomes a member
            project.members.add(request.user)

            return redirect(
                'project_detail',
                project_id=project.id
            )

    return render(
        request,
        'create_project.html'
    )


# PROJECT DETAIL
@login_required
def project_detail(request, project_id):

    project = get_object_or_404(
        Project,
        id=project_id
    )

    return render(
        request,
        'project_detail.html',
        {
            'project': project,
        }
    )


# INVITE USER TO PROJECT
@login_required
def invite_to_project(request, project_id, username):

    project = get_object_or_404(
        Project,
        id=project_id,
        owner=request.user
    )

    invited_user = get_object_or_404(
        User,
        username=username
    )

    # Only connected users can be invited
    is_connected = MessageRequest.objects.filter(
        Q(
            sender=request.user,
            receiver=invited_user
        )
        |
        Q(
            sender=invited_user,
            receiver=request.user
        ),
        status='accepted'
    ).exists()

    if is_connected:

        project.members.add(
            invited_user
        )

    return redirect(
        'project_detail',
        project_id=project.id
    )
