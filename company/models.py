from django.db import models
from userauth.models import User
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

class Company(models.Model):
    company_name = models.CharField(max_length=65, blank=False)
    company_website = models.URLField(unique = True)

    def __repr__(self):
        return "<(%s, %s)>" %(self.company_name, self.company_website)


class CompanyDetail(models.Model):
    INDUSTRY = (
        ('Accounting', 'Accounting'),
        ('Aviation', 'Aviation'),
        ('Animation', 'Animation'),
        ('Architecture', 'Architecture'),
        ('Arts and Craft', 'Arts and Craft'),
        ('Biotechnology', 'Biotechnology'),
        ('Civil Engineering', 'Civil Engineering'),
        ('Computer Network', 'Computer Network'),
        ('Computer Hardware', 'Computer Hardware'),
        ('Computer Software', 'Computer Software'),
        ('Education', 'Education'),
        ('Pharmaceutical', 'Pharmaceutical'),
    )
    SIZE = (
        ('10', '1-10'),
        ('50', '10-50'),
        ('100', '50-100'),
        ('500', '100-500'),
        ('1000', '500-1000'),
        ('5000', '1000-5000'),
        ('10000', '5000-10000'),
        ('10000', '10000+'),
    )
    TYPE = (
        ('Public', 'Public'),
        ('Government', 'Government'),
        ('Private', 'Private'),
        ('Nonprofit', 'Nonprofit'),
    )

    oganization = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='detail')
    organization_industry = models.CharField(choices=INDUSTRY, default=None, max_length=50)
    organization_size = models.CharField(choices=SIZE, default=None, max_length=50)
    organization_type = models.CharField(choices=TYPE, default=None, max_length=50)


class Company_Employee(models.Model):
    employee = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="userprofile")
    company = models.ManyToManyField(Company)

    # @receiver(post_save, sender=User)
    # def update_user_company(sender, instance, created, **kwargs):
    #         if created:
    #             Company_Employee.objects.create(user=instance)
    #         instance.profile.save()