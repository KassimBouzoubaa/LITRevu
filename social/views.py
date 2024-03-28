from django.shortcuts import render, redirect, get_object_or_404
from .forms import FollowUserForm
from django.contrib.auth.decorators import login_required
from authentication.models import User
from django.contrib import messages


@login_required
def follow_user(request):
    # Récupérer les utilisateurs suivis par 'current_user'
    user_following = request.user.following.all()

    # Récupérer les utilisateurs qui suivent 'current_user'
    following_by = request.user.followed_by.all()

    if request.method == "POST":
        username_to_follow = request.POST.get("username_to_follow")
        user_to_follow = User.objects.filter(username=username_to_follow).first()
        if user_to_follow:
            if not request.user.following.filter(followed_user=user_to_follow).exists():
                request.user.following.create(followed_user=user_to_follow)
                messages.success(
                    request, f"Vous suivez désormais {username_to_follow}."
                )
            else:
                messages.info(request, f"Vous suivez déjà {username_to_follow}.")
        else:
            messages.error(
                request, f"L'utilisateur '{username_to_follow}' n'existe pas."
            )

    form = FollowUserForm()

    context = {
        "form": form,
        "message": messages,
        "user_following": user_following,
        "following_by": following_by,
    }
    print("User Following:", list(user_following.values()))
    print("Following By:", list(following_by.values()))
    return render(request, "social/follow.html", context)


@login_required
def unfollow_user(request, id):
    # Vérifier si l'utilisateur à ne plus suivre existe
    user_to_unfollow = get_object_or_404(User, id=id)

    if request.method == "POST":
        # Vérifier si l'utilisateur est actuellement suivi par l'utilisateur connecté
        if request.user.following.filter(followed_user=user_to_unfollow).exists():
            # Si oui, le désabonner
            request.user.following.filter(followed_user=user_to_unfollow).delete()
            messages.success(
                request, f"Vous avez arrêté de suivre {user_to_unfollow.username}."
            )
        else:
            # Sinon, afficher un message d'erreur
            messages.error(request, f"Vous ne suivez pas {user_to_unfollow.username}.")

        # Rediriger vers une page ou rafraîchir la page actuelle
        return redirect("follow_user")

    # Si la méthode de la requête n'est pas POST, rediriger vers une page ou rafraîchir la page actuelle
    return render(
        request, "social/unfollow.html", {"user_to_unfollow": user_to_unfollow}
    )
