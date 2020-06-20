import logging

from bbfcapi.apis import top_search_result
from django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView

from films.clients import omdb
from films.core import types
from films.models import Film

logger = logging.getLogger(__name__)


class FilmCreate(SuccessMessageMixin, CreateView):
    model = Film
    fields = ["imdb", "is_available"]
    success_message = "You have added a new film."

    def form_valid(self, form):
        self.object = form.save(commit=False)
        film = omdb.get_film(settings.OMDB_API_KEY, self.object.imdb)
        try:
            bbfc_age = top_search_result(film.title, film.year).age_rating
            bbfc_age = types.AgeRating(bbfc_age.value)
        except:
            logger.exception("Failed to get BBFC age rating.")
            bbfc_age = None

        self.object.title = film.title
        self.object.year = film.year
        self.object.imdb_age = film.imdb_age.value if film.imdb_age else None
        self.object.bbfc_age = bbfc_age.value if bbfc_age else None
        self.object.imdb_rating = film.imdb_rating
        self.object.genre = film.genre
        self.object.runtime_mins = film.runtime_mins
        self.object.plot = film.plot
        self.object.poster_url = film.poster_url

        try:
            return super().form_valid(form)
        except IntegrityError:
            # We cannot determine which constraint failed as the err text varies
            # depending on the database backend, so we will rely on the get query.
            self.object = Film.objects.get(title=film.title, year=film.year)
            return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        if "_save" in self.request.POST:
            return reverse("votes:vote-create")
        elif "_edit" in self.request.POST:
            return super().get_success_url()
        elif "_addanother" in self.request.POST:
            return reverse("films:film-create")


class FilmUpdate(SuccessMessageMixin, UpdateView):
    model = Film
    fields = [
        "title",
        "imdb",
        "year",
        "imdb_age",
        "bbfc_age",
        "imdb_rating",
        "genre",
        "runtime_mins",
        "plot",
        "poster_url",
        "trailer",
        "is_available",
        "is_watched",
    ]
    success_message = "You have updated the film %(title)s."

    def get_success_url(self):
        if "_save" in self.request.POST:
            return reverse("votes:vote-aggregate")
        elif "_edit" in self.request.POST:
            return super().get_success_url()
        elif "_addanother" in self.request.POST:
            return reverse("films:film-create")
