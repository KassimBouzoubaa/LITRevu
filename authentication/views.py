from django.contrib.auth import logout, authenticate, login
from django.shortcuts import redirect, render
from django.views import View
from django.conf import settings
from . import forms


# Vue pour déconnecter l'utilisateur
def logout_user(request):
    logout(request)
    return redirect("login")


# Vue pour la page de connexion
class LoginPageView(View):
    template_name = "authentication/login.html"
    form_class = forms.LoginForm

    # Méthode GET pour afficher le formulaire de connexion
    def get(self, request):
        form = self.form_class()
        message = ""
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )

    # Méthode POST pour traiter le formulaire de connexion
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("flux")
        message = "Identifiants invalides."
        return render(
            request, self.template_name, context={"form": form, "message": message}
        )


# Vue pour la page d'inscription
def signup_page(request):
    form = forms.SignupForm()
    if request.method == "POST":
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Connexion automatique de l'utilisateur après inscription
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "authentication/signup.html", context={"form": form})
