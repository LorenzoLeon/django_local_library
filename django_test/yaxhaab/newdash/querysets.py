from django.db.models import Manager
from django.db.models.query import QuerySet



class PublishableQuerySet(QuerySet):
    def published(self):
        from django.utils import timezone
        return self.filter(~models.Q(publish_date=None)).filter(publish_date__lte=timezone.now())


class AuthorableQuerySet(QuerySet):
    def authored_by(self, author):
        return self.filter(author__username=author)