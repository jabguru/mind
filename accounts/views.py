from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import Team
from django.contrib.auth.models import User
from django.contrib import messages
from projects.models import Project, Issue

#YEMI
import re 
from django.shortcuts import render, redirect, Http404
from .forms import UserRegisterForm, UserUpdateForm #ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from accounts.models import EmailConfirmed, UserProfile
from django.urls import reverse

# Create your views here.
def dashboard(request):
    all_teams = Team.objects.all()
    all_issues = Issue.objects.all().order_by("-post_date")
    all_projects = Project.objects.all()[:5]
    projects = Project.objects.all()

    completed_projects = Project.objects.filter(is_accepted=True)

    projects_counter = 0
    for project in projects:
        projects_counter+=1

    completed_counter = 0
    for project in completed_projects:
        completed_counter+=1

    # projects = len(projects)
    # completed_projects = len(projects)

    if not projects_counter == 0:
        completed_percent = int((completed_counter/projects_counter)*100)
        ongoing_percent = int(100 - completed_percent)
    else:
        completed_percent = 0
        ongoing_percent = 0

    ongoing_counter = projects_counter - completed_counter

    context = {   
        'all_teams':all_teams, 'all_projects':all_projects,
        'all_issues': all_issues,
        'completed_percent': completed_percent,
        'ongoing_percent': ongoing_percent,
        'completed_counter': completed_counter,
        'ongoing_counter': ongoing_counter,
     }
    return render(request, 'accounts/dashboard.html', context)

def create_team(request):
    users = User.objects.all()
    if request.POST:
        name = request.POST['name']
        members = request.POST.getlist('members')
        program_manager = request.POST['manager']

        program_manager = User.objects.get(username=program_manager)

        team = Team.objects.create(name=name, program_manager=program_manager)

        for member in members:
            user = User.objects.get(username=member)
            team.members.add(user)

        team.save()

        user = User.objects.get(username=program_manager)
        user.userprofile.is_program_manager = True
        user.save()
        
        messages.success(request, 'Team successfully created!')
        return redirect("dashboard")

    context = {'users':users,}
    return render(request, 'accounts/create-team.html', context)

def manage_teams(request):
    context ={

    }
    return render(request, 'accounts/manage-teams.html', context)

def delete_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)

    if request.POST:
        team.delete()
        messages.success(request, 'Team successfully deleted!')
        return redirect('dashboard')

    context = {
        'team': team,
    }
    return render(request, 'accounts/delete-team.html', context)

def team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    projects = Project.objects.filter(team=team)
    completed_projects = projects.filter(is_accepted=True)

    teams = Team.objects.all().order_by('-totalPoints')
    length = len(teams)
    n = range(1, length+1)

    dictionary = {}
    position = []

    for x in n:
        position.append(x)

    for key,val in zip(position,teams):
        dictionary[key] = val

    for key, val in dictionary.items():
        the_team = Team.objects.get(id=val.id)
        the_team.position = key
        the_team.save()

    projects_counter = 0
    for project in projects:
        projects_counter+=1

    completed_counter = 0
    for project in completed_projects:
        completed_counter+=1

    # projects = len(projects)
    # completed_projects = len(projects)

    if not projects_counter == 0:
        completed_percent = int((completed_counter/projects_counter)*100)
        ongoing_percent = int(100 - completed_percent)
    else:
        completed_percent = 0
        ongoing_percent = 0

    ongoing_counter = projects_counter - completed_counter

    context = {
        "team":team,
        "projects":projects,
        "completed_percent":completed_percent,
        "ongoing_percent":ongoing_percent,
        'completed_counter': completed_counter,
        'ongoing_counter': ongoing_counter,
    }
    return render(request, 'accounts/team.html', context)

def update_team(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    users = User.objects.all()

    if request.POST:
        for member in team.members.all():
            user = User.objects.get(username=member)
            team.members.remove(user)

        user = team.program_manager
        user.userprofile.is_program_manager = False
        user.save()
        
        team.name = request.POST['name']
        members = request.POST.getlist('members')
        program_manager = request.POST['manager']

        team.program_manager = User.objects.get(username=program_manager)

        for member in members:
            user = User.objects.get(username=member)
            team.members.add(user)

        team.save()

        user = User.objects.get(username=program_manager)
        user.userprofile.is_program_manager = True
        user.save()
        
        messages.success(request, 'Team successfully Updated!')
        return redirect('dashboard')

    context = {
        'team':team, 'users': users,
    }
    return render(request, 'accounts/update-team.html', context)

#YEMI
def register(request):
	if request.method=='POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			print('VALID')
			username = form.cleaned_data.get('username')
			position = form.cleaned_data.get('position')
			user = User.objects.get(username=username)
			profile = UserProfile.objects.create(position=position, user=user)
			profile.save()
			messages.success(request, f'Account created for {username}! Check your email to confirm your email address.')
			return redirect('register')

	else:
		form = UserRegisterForm()
	return render(request, 'accounts/register.html', {'form':form})

SHA1_RE = re.compile('^[a-f0-9]{40}$')
def activation_view(request, activation_key):
	if SHA1_RE.search(activation_key):
		print ('activation key is valid')
		try:
			user_confirmed = EmailConfirmed.objects.get(activation_key=activation_key)
		except EmailConfirmed.DoesNotExist:
			user_confirmed = None
			messages.success(request, 'There was an error with your request')
			return redirect('register')
		if user_confirmed is not None and not user_confirmed.confirmed:
			message = 'Confirmation Successful!!'
			user_confirmed.confirmed = True
			#user_confirmed.activation_key = 'confirmed'
			user_confirmed.save()
			messages.success(request, 'Your account has been activated! You can now <a href={}>Login</a>'.format(reverse("login")), extra_tags='safe')
		
		elif user_confirmed is not None and user_confirmed.confirmed:
			message = 'Already confirmed'
			messages.success(request, 'Your account has already been activated! <a href={}>Login</a>'.format(reverse("login")), extra_tags='safe')
		
		
		else:
			message = ''
		context = {'message':message}
		return render(request, 'accounts/activation.html', context)
	else:
		raise Http404