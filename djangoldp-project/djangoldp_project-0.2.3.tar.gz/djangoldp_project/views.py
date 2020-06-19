from djangoldp.filters import LocalObjectFilterBackend
from djangoldp.views import LDPViewSet


class ProjectMembersViewset(LDPViewSet):

    def is_safe_create(self, user, validated_data, *args, **kwargs):
        from djangoldp_project.models import Project

        try:
            project = Project.objects.get(urlid=validated_data['project']['urlid'])

            # public circles any user can add
            if project.status == 'Public':
                return True

            # other circles any circle member can add a user
            if project.members.filter(user=user).exists():
                return True
        except Project.DoesNotExist:
            return True

        return False


class ProjectsJoinableViewset(LDPViewSet):

    filter_backends = [LocalObjectFilterBackend]

    def get_queryset(self):
        return super().get_queryset().exclude(team__id=self.request.user.id)\
            .exclude(status="Private")\
            .exclude(status="Archived")
