from django.db import models


class ArticleModelQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='publish')

    def promoted(self):
        return self.published().filter(is_promote=True)

    def trending(self):
        return self.published().filter(is_trend=True)

    def author(self, username):
        return self.published().filter(author__username=username)

    def promotional(self):
        return self.published().filter(is_promotional=True)

    def opinion(self):
        return self.published().filter(is_opinion=True)