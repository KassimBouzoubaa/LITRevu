from django import forms
from .models import Ticket, Review, Photo


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image"]
        labels = {"image": "Image"}


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["title", "description"]
        labels = {"title": "Titre", "description": "Description"}
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        label="Note",
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    headline = forms.CharField(label="Titre")
    body = forms.CharField(
        label="Commentaire", widget=forms.Textarea(attrs={"rows": 4})
    )

    class Meta:
        model = Review
        fields = ["headline", "rating", "body"]
        labels = {"headline": "Titre", "body": "Commentaire"}
