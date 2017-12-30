from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import ProjectForm, TicketForm, UserForm
from .models import Project, Ticket


def create_project(request):
    if not request.user.is_authenticated():
        return render(request, 'board/login.html')
    else:
        form = ProjectForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            project = form.save(commit=False)
            # project.name = request.name
            # project.description = request.description
            project.save()
            return render(request, 'board/detail.html', {'project': project})
        context = {
            "form": form,
        }
        return render(request, 'board/create_project.html', context)


def create_ticket(request, project_id):
    form = TicketForm(request.POST or None, request.FILES or None)
    project = get_object_or_404(Project, pk=project_id)
    if form.is_valid():
        project_tickets = project.ticket_set.all()
        for t in project_tickets:
            if t.name == form.cleaned_data.get("name"):
                context = {
                    'project': project,
                    'form': form,
                    'error_message': 'You already added that ticket',
                }
                return render(request, 'board/create_ticket.html', context)
        ticket = form.save(commit=False)
        ticket.project = project
        ticket.save()
        return render(request, 'board/detail.html', {'project': project})
    context = {
        'project': project,
        'form': form,
    }
    return render(request, 'board/create_ticket.html', context)


def delete_project(request, project_id):
    project = Project.objects.get(pk=project_id)
    project.delete()
    projects = Project.objects.all()
    return render(request, 'board/index.html', {'projects': projects})


# def update_project(request, project_id):
#     project = Project.objects.get(pk=project_id)
#     form = ProjectForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         project = form.save(commit=False)
#         # project.name = request.name
#         # project.description = request.description
#         project.save()
#     return render(request, 'board/index.html', {'project': project})

def update_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    form = ProjectForm(request.POST or None,
                        request.FILES or None, instance=project)
    if request.method == 'POST':
        if form.is_valid():
           form.save()
           return render(request, 'board/detail.html', {'project': project})
    return render(request, 'board/create_project.html', {'form': form})


def update_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    form = TicketForm(request.POST or None,
                      request.FILES or None, instance=ticket)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return render(request, 'board/ticket_detail.html', {'ticket': ticket})
    return render(request, 'board/create_project.html', {'form': form})


def delete_ticket(request, project_id, ticket_id):
    project = get_object_or_404(Project, pk=project_id)
    ticket = Ticket.objects.get(pk=ticket_id)
    ticket.delete()
    return render(request, 'board/detail.html', {'project': project})


def detail(request, project_id):
    if not request.user.is_authenticated():
        return render(request, 'board/login.html')
    else:
        user = request.user
        project = get_object_or_404(Project, pk=project_id)
        return render(request, 'board/detail.html', {'project': project, 'user': user})


def ticket_detail(request, ticket_id):
    if not request.user.is_authenticated():
        return render(request, 'board/login.html')
    else:
        ticket = get_object_or_404(Ticket, pk=ticket_id)
        return render(request, 'board/ticket_detail.html', {'ticket': ticket})


# def favorite(request, ticket_id):
#     ticket = get_object_or_404(ticket, pk=ticket_id)
#     try:
#         if ticket.is_favorite:
#             ticket.is_favorite = False
#         else:
#             ticket.is_favorite = True
#         ticket.save()
#     except (KeyError, ticket.DoesNotExist):
#         return JsonResponse({'success': False})
#     else:
#         return JsonResponse({'success': True})


# def favorite_project(request, project_id):
#     project = get_object_or_404(project, pk=project_id)
#     try:
#         if project.is_favorite:
#             project.is_favorite = False
#         else:
#             project.is_favorite = True
#         project.save()
#     except (KeyError, project.DoesNotExist):
#         return JsonResponse({'success': False})
#     else:
#         return JsonResponse({'success': True})


def index(request):
    if not request.user.is_authenticated():
        return render(request, 'board/login.html')
    else:
        projects = Project.objects.all()
        ticket_results = Ticket.objects.all()
        return render(request, 'board/index.html', {'projects': projects})


def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'board/login.html', context)


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                projects = Project.objects.all()
                return render(request, 'board/welcome.html', {'projects': projects})
            else:
                return render(request, 'board/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'board/login.html', {'error_message': 'Invalid login'})
    return render(request, 'board/login.html')


def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        # if user is not None:
        #     if user.is_active:
        #         login(request, user)
        #         projects = Project.objects.filter(user=request.user)
        #         return render(request, 'board/index.html', {'projects': projects})
    context = {
        "form": form,
    }
    return render(request, 'board/register.html', context)


def tickets(request, filter_by):
    if not request.user.is_authenticated():
        return render(request, 'board/login.html')
    else:
        try:
            ticket_ids = []
            for project in Project.objects.all():
                for ticket in project.ticket_set.all():
                    ticket_ids.append(ticket.pk)
            users_tickets = Ticket.objects.filter(pk__in=ticket_ids)
            # if filter_by == 'favorites':
            #     users_tickets = users_tickets.filter(is_favorite=True)
        except Project.DoesNotExist:
            users_tickets = []
        return render(request, 'board/tickets.html', {
            'ticket_list': users_tickets,
            'filter_by': filter_by,
        })
