from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from djstripe.models import Customer, Subscription
class Plan(models.Model):
    """
    Plan model to manage different subscription plans.
    """
    name = models.CharField(max_length=255)
    max_num_links = models.IntegerField()
    max_num_tag = models.IntegerField()
    max_num_category = models.IntegerField()

    def __str__(self):
        return self.name

class User(AbstractUser):
    plan = models.ForeignKey(Plan, related_name='users', default=1, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.SET_NULL)
    subscription = models.ForeignKey(Subscription, null=True, blank=True,on_delete=models.SET_NULL)


    def save(self, *args, **kwargs):
        if not self.plan_id:
            default_plan, created = Plan.objects.get_or_create(
                name="Default Plan",
                max_num_links=10,
                max_num_tag=5,
                max_num_category=3
            )
            self.plan = default_plan
        try:
            self.full_clean()
        except ValidationError as e:
            raise e
        super().save(*args, **kwargs)
