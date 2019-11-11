from django.db import models


class Category(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, unique=True)

    def get_data(self) -> dict:
        """
            Return info about category and parent/children items.
        """
        return {
            'id': self.id,
            'name': self.name,
            'parents': [{'id': parent.id, 'name': parent.name} for parent in self.get_parents()],
            'children': list(self.get_children().values('id', 'name')),
            'siblings': list(self.get_siblings().values('id', 'name')),
        }

    def get_children(self):
        return Category.objects.filter(parent=self).order_by('id')

    def get_parents(self):
        if self.parent is None:
            return []
        parents = [self.parent]
        parents += self.parent.get_parents()
        return parents

    def get_siblings(self):
        return Category.objects.filter(parent=self.parent).exclude(id=self.id).order_by('id')
