from djangoldp.filters import LocalObjectFilterBackend
from djangoldp.views import LDPViewSet
from djangoldp.models import Model


class CircleMembersViewset(LDPViewSet):

    def is_safe_create(self, user, validated_data, *args, **kwargs):
        from djangoldp_circle.models import Circle, CircleMember

        try:
            circle = Circle.objects.get(urlid=validated_data['circle']['urlid'])

            # public circles any user can add
            if circle.status == 'Public':
                return True

            # other circles any circle member can add a user
            if circle.members.filter(user=user).exists():
                return True
        except Circle.DoesNotExist:
            return True

        return False


class CirclesJoinableViewset(LDPViewSet):

    filter_backends = [LocalObjectFilterBackend]

    def get_queryset(self):
        return super().get_queryset().exclude(team__id=self.request.user.id)\
            .exclude(status="Private")\
            .exclude(status="Archived")
