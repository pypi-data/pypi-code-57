from django.db.models import Lookup
from django.db.models.fields import Field


class NoCase(Lookup):
    lookup_name = "lcontains"

    def as_sql(self, compiler, connection):
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        params = lhs_params + rhs_params
        params = [f"%{param}%" for param in params]
        return "%s like Lower(%s)" % (f"Lower({lhs})", rhs), params

    @staticmethod
    def register():
        Field.register_lookup(NoCase)
