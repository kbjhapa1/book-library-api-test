from django.conf import settings
from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    published_year = models.PositiveSmallIntegerField(null=True, blank=True)
    # Phase 3: every new book remembers who added it.
    # null=True because books created in Phase 2 have no owner.
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="books",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.title} by {self.author}"