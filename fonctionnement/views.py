from itertools import chain

from django.shortcuts import render, redirect, get_object_or_404

from fonctionnement.forms import TicketForm, ReviewForm, PhotoForm
from fonctionnement.models import Ticket, Review, Photo
from django.contrib.auth.decorators import login_required
from django.db.models import CharField, Value


# ----- TICKET ----- #
@login_required
def ticket_create(request):
    if request.method == "POST":
        ticket_form = TicketForm(request.POST)
        photo_form = PhotoForm(
            request.POST, request.FILES
        )  # Prend en charge les fichiers téléchargés

        if ticket_form.is_valid() and photo_form.is_valid():
            # Enregistrez d'abord la photo
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()

            # Ensuite, enregistrez le ticket en référençant la photo nouvellement créée
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.image = photo
            ticket.save()

            return redirect("flux")

    else:
        ticket_form = TicketForm()
        photo_form = PhotoForm()

    context = {"ticket_form": ticket_form, "photo_form": photo_form}
    return render(
        request,
        template_name="fonctionnement/ticket_create.html",
        context=context,
    )


@login_required
def ticket_update(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    photo = ticket.image  # Récupérer l'image associée au ticket

    if request.user != ticket.user:
        return render(
            request,
            "error.html",
            {"message": "Vous n'êtes pas autorisé à supprimer ce ticket."},
            status=403,
        )

    if request.method == "POST":
        ticket_form = TicketForm(request.POST, instance=ticket)
        photo_form = PhotoForm(request.POST, request.FILES, instance=photo)

        if ticket_form.is_valid() and photo_form.is_valid():
            photo_form.save()
            return redirect("flux")
    else:
        ticket_form = TicketForm(instance=ticket)
        photo_form = PhotoForm(instance=photo)

    context = {"ticket_form": ticket_form, "photo_form": photo_form}

    return render(request, "fonctionnement/ticket_update.html", context)


@login_required
def ticket_delete(request, id):
    ticket = get_object_or_404(Ticket, id=id)

    if request.user != ticket.user:
        return render(
            request,
            "error.html",
            {"message": "Vous n'êtes pas autorisé à supprimer ce ticket."},
            status=403,
        )

    if request.method == "POST":
        ticket.delete()
        return redirect("flux")

    return render(request, "fonctionnement/ticket_delete.html", {"ticket": ticket})


@login_required
def ticket_detail(request, id):
    ticket = Ticket.objects.get(id=id)
    return render(
        request,
        template_name="fonctionnement/ticket_detail.html",
        context={"ticket": ticket},
    )


# ----- Review ----- #
@login_required
def review_create(request):
    if request.method == "POST":
        formTicket = TicketForm(request.POST)
        formReview = ReviewForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if formReview.is_valid() and formTicket.is_valid():
            photo = photo_form.save(commit=False)
            photo.uploader = request.user
            photo.save()

            # Ensuite, enregistrez le ticket en référençant la photo nouvellement créée
            ticket = formTicket.save(commit=False)
            ticket.user = request.user
            ticket.image = photo
            ticket.save()

            review = formReview.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect("flux")

    else:
        formReview = ReviewForm()
        formTicket = TicketForm()
        photo_form = PhotoForm()

    context = {
        "formReview": formReview,
        "formTicket": formTicket,
        "photo_form": photo_form,
    }

    return render(
        request, template_name="fonctionnement/review_create.html", context=context
    )


@login_required
def review_response_create(request, id):
    ticket = Ticket.objects.get(id=id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect("flux")

    else:
        form = ReviewForm()

    context = {"form": form, "ticket": ticket}

    return render(
        request,
        template_name="fonctionnement/review_create.html",
        context=context,
    )


@login_required
def review_update(request, id):
    review = get_object_or_404(Review, id=id)

    if request.user != review.user:
        return render(
            request,
            "error.html",
            {"message": "Vous n'êtes pas autorisé à supprimer cette critique."},
            status=403,
        )

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("flux")
    else:
        form = ReviewForm(instance=review)

    return render(request, "fonctionnement/review_update.html", {"formReview": form})


@login_required
def review_delete(request, id):
    # Récupérer la critique à supprimer
    review = get_object_or_404(Review, id=id)

    # Vérifier si l'utilisateur connecté est le propriétaire de la critique
    if request.user != review.user:
        # Si ce n'est pas le cas, renvoyer une réponse d'erreur ou rediriger
        # par exemple, vous pouvez renvoyer une réponse HTTP 403 Forbidden
        return render(
            request,
            "error.html",
            {"message": "Vous n'êtes pas autorisé à supprimer cette critique."},
            status=403,
        )

    if request.method == "POST":
        # Si la méthode est POST, supprimer la critique de la base de données
        review.delete()
        # Rediriger vers une page de confirmation ou une autre vue
        return redirect("flux")

    # Si la méthode n'est pas POST, rendre le template de confirmation de suppression
    return render(request, "fonctionnement/review_delete.html", {"review": review})


@login_required
def review_detail(request, id):
    review = Review.objects.get(id=id)
    return render(
        request,
        template_name="fonctionnement/review_detail.html",
        context={"review": review},
    )


@login_required
def feed(request):
    # Récupérer tous les avis
    reviews = Review.objects.all()
    # Ajouter une annotation au queryset de reviews pour indiquer le type de contenu
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    # Récupérer tous les tickets
    tickets = Ticket.objects.all()
    # Ajouter une annotation au queryset de tickets pour indiquer le type de contenu
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    # Combiner les deux types de publications (avis et tickets)
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )

    return render(request, "fonctionnement/flux.html", {"posts": posts})


@login_required
def user_tickets_and_reviews(request):
    # Récupérer tous les tickets de l'utilisateur connecté
    user_tickets = Ticket.objects.filter(user=request.user)
    user_tickets = user_tickets.annotate(content_type=Value("TICKET", CharField()))

    # Récupérer tous les avis de l'utilisateur connecté
    user_reviews = Review.objects.filter(user=request.user)
    user_reviews = user_reviews.annotate(content_type=Value("REVIEW", CharField()))

    posts = sorted(
        chain(user_reviews, user_tickets),
        key=lambda post: post.time_created,
        reverse=True,
    )

    return render(
        request,
        "fonctionnement/user_tickets_and_reviews.html",
        {"posts": posts, "from_posts": True},
    )
