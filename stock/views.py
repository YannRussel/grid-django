from django.shortcuts import render, get_object_or_404, redirect
from datetime import date, datetime
from .models import LivraisonMensuelle, UtilisationJournal, Produit
from relotagrid.models import Site  # adapte selon ton projet
from django.contrib import messages
from django.db.models import Sum
from django.utils.timezone import now
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

@login_required
def livraisons_par_site(request, slug_site):
    site = get_object_or_404(Site, slug=slug_site)

    # Valeur par défaut : mois actuel
    today = date.today()
    mois_selectionne = request.GET.get('mois')
    
    if mois_selectionne:
        # mois au format "YYYY-MM"
        try:
            annee, mois = map(int, mois_selectionne.split("-"))
            mois_date = date(annee, mois, 1)
        except ValueError:
            annee, mois = today.year, today.month
            mois_date = date(annee, mois, 1)
    else:
        annee, mois = today.year, today.month
        mois_date = date(annee, mois, 1)

    livraisons = LivraisonMensuelle.objects.filter(
        site=site,
        mois__year=annee,
        mois__month=mois
    ).select_related('produit')

    context = {
        'site': site,
        'mois': mois_date,
        'mois_selectionne': mois_selectionne or f"{today.year}-{today.month:02}",
        'livraisons': livraisons
    }

    return render(request, 'stock/tableau_livraison.html', context)


@login_required
def enregistrer_utilisation(request, slug):
    site = get_object_or_404(Site, slug=slug)
    mois_str = request.GET.get('mois')

    # Mois sélectionné ou courant
    if mois_str:
        try:
            mois = datetime.strptime(mois_str, "%Y-%m")
        except ValueError:
            mois = now().replace(day=1)
    else:
        mois = now().replace(day=1)

    # Produits livrés pour ce site et mois
    livraisons = LivraisonMensuelle.objects.filter(
        site=site,
        mois__month=mois.month,
        mois__year=mois.year
    )
    produits = Produit.objects.filter(
        livraisons__in=livraisons
    ).distinct()

    # Traitement du formulaire
    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        date_utilisation = request.POST.get('date_utilisation')
        quantite_utilisee = request.POST.get('quantite_utilisee')

        if produit_id and date_utilisation and quantite_utilisee:
            try:
                produit = Produit.objects.get(id=produit_id)
                quantite_utilisee = int(quantite_utilisee)
                date_utilisation = datetime.strptime(date_utilisation, "%Y-%m-%d").date()

                UtilisationJournal.objects.create(
                    produit=produit,
                    date_utilisation=date_utilisation,
                    quantite_utilisee=quantite_utilisee
                )
                messages.success(request, "Utilisation enregistrée avec succès.")
                return redirect('gestion_stock:enregistrer_utilisation', slug=slug)

            except Exception as e:
                messages.error(request, f"Erreur lors de l'enregistrement : {e}")
        else:
            messages.error(request, "Veuillez remplir tous les champs.")

    # Données du tableau comparatif
    utilisations = UtilisationJournal.objects.filter(
        date_utilisation__month=mois.month,
        date_utilisation__year=mois.year,
        produit__in=livraisons.values_list('produit', flat=True)
    )

    # Agrégation
    livraisons_dict = {}
    for l in livraisons:
        livraisons_dict[l.produit.id] = {
            'produit': l.produit,
            'quantite_livree': l.quantite_livree,
            'quantite_utilisee': 0,
        }

    for u in utilisations:
        if u.produit.id in livraisons_dict:
            livraisons_dict[u.produit.id]['quantite_utilisee'] += u.quantite_utilisee

    # Calcul de la régression (livré - utilisé)
    for v in livraisons_dict.values():
        v['regression'] = v['quantite_livree'] - v['quantite_utilisee']

    comparaison = list(livraisons_dict.values())

    context = {
        'site': site,
        'produits': produits,
        'mois_selectionne': mois.strftime('%Y-%m'),
        'comparaison': comparaison,
    }

    return render(request, 'stock/enregistrer_utilisation.html', context)

# CRUD sur les produits 


@login_required
def produit_create(request):
    produit_modifie = None
    modifier_id = request.GET.get("modifier")

    if modifier_id:
        produit_modifie = Produit.objects.filter(id=modifier_id).first()

    if request.method == "POST":
        if request.POST.get("produit_id"):  # modification
            produit = Produit.objects.get(id=request.POST["produit_id"])
            produit.nom = request.POST["nom"]
            produit.conditionnement = request.POST["conditionnement"]
            produit.quantite_limite = request.POST["quantite_limite"]
            produit.save()
        else:  # création
            Produit.objects.create(
                nom=request.POST["nom"],
                conditionnement=request.POST["conditionnement"],
                quantite_limite=request.POST["quantite_limite"],
            )
        return redirect("gestion_stock:enregistrer_produit")

    produits_list = Produit.objects.all().order_by('id')  # optionnel: tri par id

    paginator = Paginator(produits_list, 10)  # 10 produits par page
    page_number = request.GET.get('page')
    produits = paginator.get_page(page_number)

    return render(request, "stock/produit_form.html", {
        "produits": produits,
        "produit_modifie": produit_modifie,
    })


# Supprimer un produit
@login_required
def produit_delete(request, pk):
    produit = get_object_or_404(Produit, id=pk)
    nom = produit.nom  # Pour affichage dans le message
    produit.delete()
    messages.success(request, f"Le produit '{nom}' a été supprimé avec succès.")
    return redirect('gestion_stock:enregistrer_produit')

# Gestion des livraisons mensuelles

@login_required
def enregistrer_livraison(request, slug):
    site = get_object_or_404(Site, slug=slug)
    livraison_modifiee = None

    # Si on édite une livraison existante
    if 'modifier' in request.GET:
        livraison_id = request.GET.get('modifier')
        livraison_modifiee = get_object_or_404(LivraisonMensuelle, id=livraison_id, site=site)

    if request.method == 'POST':
        produit_id = request.POST.get('produit')
        quantite = request.POST.get('quantite')
        date_livraison_str = request.POST.get('date_livraison')
        livraison_id = request.POST.get('livraison_id')

        if not date_livraison_str:
            messages.error(request, "La date de livraison est obligatoire.")
            return redirect('gestion_stock:enregistrer_livraison', slug=slug)

        try:
            # On récupère YYYY-MM venant du input type="month"
            annee, mois_int = map(int, date_livraison_str.split('-'))
            mois = date(annee, mois_int, 1)
        except Exception:
            messages.error(request, "Format de date invalide.")
            return redirect('gestion_stock:enregistrer_livraison', slug=slug)

        produit = get_object_or_404(Produit, id=produit_id)

        if livraison_id:
            # Modification d'une livraison
            livraison = get_object_or_404(LivraisonMensuelle, id=livraison_id, site=site)
            livraison.produit = produit
            livraison.quantite_livree = quantite
            livraison.mois = mois
            messages.success(request, "La livraison a été modifiée avec succès.")
        else:
            # Nouvelle livraison
            livraison = LivraisonMensuelle.objects.create(
                produit=produit,
                site=site,
                quantite_livree=quantite,
                mois=mois
            )
            messages.success(request, "Nouvelle livraison enregistrée avec succès.")

        livraison.save()
        return redirect('gestion_stock:enregistrer_livraison', slug=slug)

    # Liste des livraisons du site
    livraisons = LivraisonMensuelle.objects.filter(site=site).order_by('-mois')

    # Filtrage par mois depuis le GET ou la livraison en édition
    mois_selectionne_str = request.GET.get('mois') or (livraison_modifiee.mois.strftime("%Y-%m") if livraison_modifiee else now().strftime("%Y-%m"))

    try:
        annee, mois_int = map(int, mois_selectionne_str.split('-'))
        mois_filtre = date(annee, mois_int, 1)
    except ValueError:
        mois_filtre = now().date().replace(day=1)

    # Filtrage des livraisons pour le mois sélectionné
    livraisons = livraisons.filter(mois__year=mois_filtre.year, mois__month=mois_filtre.month)

    # Exclure les produits déjà livrés ce mois-ci (sauf si on modifie)
    produits_deja_livres_ids = LivraisonMensuelle.objects.filter(
        site=site,
        mois=mois_filtre
    ).values_list('produit_id', flat=True)

    if livraison_modifiee:
        produits = Produit.objects.exclude(
            ~Q(id=livraison_modifiee.produit.id),
            id__in=produits_deja_livres_ids
        )
    else:
        produits = Produit.objects.exclude(id__in=produits_deja_livres_ids)

    # Pagination
    paginator = Paginator(livraisons, 10)
    page = request.GET.get('page')
    livraisons = paginator.get_page(page)

    context = {
        'site': site,
        'produits': produits,
        'livraison_modifiee': livraison_modifiee,
        'livraisons': livraisons,
        'now': now(),
        'mois_selectionne': mois_filtre.strftime('%Y-%m'),
    }

    return render(request, 'stock/livraisons.html', context)

@login_required
def supprimer_livraison(request, livraison_id):
    livraison = get_object_or_404(LivraisonMensuelle, id=livraison_id)
    slug = livraison.site.slug
    livraison.delete()
    messages.success(request, "Livraison supprimée avec succès.")
    return redirect('gestion_stock:enregistrer_livraison', slug=slug)

