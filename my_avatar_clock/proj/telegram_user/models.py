from django.db import models


class TelegramUser(models.Model):
    phone = models.CharField(max_length=20)

    secret_tg_key = models.CharField(max_length=20)

    secret_app_key = models.CharField(max_length=50)

    api_id = models.CharField(max_length=50)

    api_hash = models.CharField(max_length=50)

    objects = models.Manager()

    def __str__(self):
        return self.phone

    def save(self, *args, **kwargs):
        """
        Save object to the database. Removes all other entries if there
        are any.
        """
        self.__class__.objects.exclude(id=self.id).delete()
        super(TelegramUser, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        Load object from the database. Failing that, create a new empty
        (default) instance of the object and return it (without saving it
        to the database).
        """

        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()
