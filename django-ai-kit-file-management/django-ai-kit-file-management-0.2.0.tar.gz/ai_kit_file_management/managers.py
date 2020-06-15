from django.db.models import Manager


class FileManager(Manager):
    def visible_for(self, user):
        return self.all()
