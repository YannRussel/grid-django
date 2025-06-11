from django.shortcuts import render, redirect, get_object_or_404
from .models import RetardJournalier
from relotagrid.models import Agent, Site
from django.contrib import messages
from django.utils.dateparse import parse_date, parse_time
from datetime import date, timedelta, datetime, time, datetime as dt

from django.http import JsonResponse
from datetime import datetime, time, date as dt_date
from django.contrib.auth.decorators import login_required
from calendar import monthrange

@login_required
def control_retard(request, slug):  # <== ajoute slug ici
    today = date.today()

    # Récupération du site correspondant au slug
    site = get_object_or_404(Site, slug=slug)

    if request.method == 'POST':
        agent_id = request.POST.get('agent_id')
        date_str = request.POST.get('date')
        heure_str = request.POST.get('heure_arrivee')

        if agent_id and date_str and heure_str:
            date_val = parse_date(date_str)
            heure = parse_time(heure_str)

            if not RetardJournalier.objects.filter(agent_id=agent_id, date=date_val).exists():
                RetardJournalier.objects.create(agent_id=agent_id, date=date_val, heure_arrivee=heure)
                messages.success(request, "Retard enregistré avec succès.")
            else:
                messages.warning(request, "Ce retard a déjà été enregistré pour cet agent à cette date.")

        return redirect('gestion_personnel:control_retard', slug=slug)  # utilise le slug dans la redirection

    # Filtrer les agents pour ce site
    agents = Agent.objects.filter(site=site)
    agents_avec_retard = RetardJournalier.objects.filter(date=today, agent__site=site).values_list('agent_id', flat=True)

    context = {
        'agents': agents,
        'agents_avec_retard': agents_avec_retard,
        'today': today.strftime('%Y-%m-%d'),
        'site': site,  # si besoin de l'afficher
    }
    return render(request, 'gestion_personnel/control_abscence.html', context)

# Recuperation de la liste par date 

@login_required
def liste_retards_par_date(request, slug):
    retard_de_base = time(6, 0, 0)
    selected_date = request.GET.get('date')

    if selected_date:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    else:
        selected_date = datetime.today().date()

    site = get_object_or_404(Site, slug=slug)
    date_a_venir = selected_date > datetime.today().date()
    agents = Agent.objects.filter(site=site)

    retards_du_jour = RetardJournalier.objects.filter(date=selected_date, agent__site=site).select_related('agent')
    retards_dict = {r.agent.id: r for r in retards_du_jour}

    liste = []
    for agent in agents:
        if agent.id in retards_dict:
            r = retards_dict[agent.id]
            h_arrivee = datetime.combine(r.date, r.heure_arrivee)
            h_base = datetime.combine(r.date, retard_de_base)
            diff = max(0, (h_arrivee - h_base).total_seconds() / 60)
            liste.append({
                'agent': agent,
                'heure_arrivee': r.heure_arrivee.strftime("%H:%M"),
                'retard_min': int(diff),
                'present': True
            })
        else:
            if selected_date.weekday() != 6:  # 6 = dimanche
                # Absent un jour ouvré
                liste.append({
                    'agent': agent,
                    'heure_arrivee': None,
                    'retard_min': 420,  # 7h x 60
                    'present': False
                })
            else:
                # Jour non travaillé (dimanche)
                liste.append({
                    'agent': agent,
                    'heure_arrivee': None,
                    'retard_min': None,
                    'present': False
                })

    return render(request, 'gestion_personnel/tableau_retard.html', {
        'retards': liste,
        'date_affichee': selected_date,
        'date_a_venir': date_a_venir,
        'site': site,
    })
# Graphe de retard des agents 
@login_required
def afficher_graphe_retards(request, slug):
    date_str = request.GET.get('date')
    if date_str:
        date_selectionnee = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date_selectionnee = datetime.today().date()

    site = get_object_or_404(Site, slug=slug)

    return render(request, 'gestion_personnel/graphe_retard.html', {
        'date_selectionnee': date_selectionnee.strftime('%Y-%m-%d'),
        'site': site,
    })

@login_required
def donnees_retards_par_mois(request, slug):
    date_str = request.GET.get('date')
    if date_str:
        try:
            date_reference = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Date invalide'}, status=400)
    else:
        date_reference = datetime.today().date()

    site = get_object_or_404(Site, slug=slug)
    heure_base = time(6, 0, 0)

    # Début et fin du mois
    first_day = date_reference.replace(day=1)
    last_day = date_reference.replace(day=monthrange(date_reference.year, date_reference.month)[1])

    agents = Agent.objects.filter(site=site)
    retards = RetardJournalier.objects.filter(
        date__range=(first_day, last_day),
        agent__site=site
    ).select_related('agent')

    retard_par_agent = {f"{agent.prenom} {agent.nom}": 0 for agent in agents}

    for r in retards:
        h_base = datetime.combine(r.date, heure_base)
        h_arrivee = datetime.combine(r.date, r.heure_arrivee)
        minutes = max(0, int((h_arrivee - h_base).total_seconds() / 60))
        nom = f"{r.agent.prenom} {r.agent.nom}"
        retard_par_agent[nom] += minutes  # accumulation mensuelle

    return JsonResponse({
        'labels': list(retard_par_agent.keys()),
        'data': list(retard_par_agent.values()),
        'mois': date_reference.strftime('%B %Y')  # Exemple : "Mai 2025"
    })
