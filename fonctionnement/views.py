from django.shortcuts import render, redirect, get_object_or_404

from fonctionnement.forms import TicketForm, ReviewForm, PhotoForm
from fonctionnement.models import Ticket, Review, Photo
from django.contrib.auth.decorators import login_required


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

    return render(
        request,
        template_name="fonctionnement/ticket_create.html",
        context={"ticket_form": ticket_form, "photo_form": photo_form},
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

    return render(request, "fonctionnement/ticket_update.html", {"ticket_form": ticket_form, "photo_form": photo_form})


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

    return render(
        request,
        template_name="fonctionnement/review_create.html",
        context={
            "formReview": formReview,
            "formTicket": formTicket,
            "photo_form": photo_form,
        },
    )


@login_required
def review_response_create(request, id):
    ticket = Ticket.objects.get(id=id)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("flux")

    else:
        form = ReviewForm()

    return render(
        request,
        template_name="fonctionnement/review_create.html",
        context={"form": form, "ticket": ticket},
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
def flux_detail(request):
    return render(request, "fonctionnement/flux.html")
