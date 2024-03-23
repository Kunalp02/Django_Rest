from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.gis.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

User = get_user_model()


class ChoiceList(models.Model):
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    class ChoiceType(models.TextChoices):
        SKILL_CATEGORY = "skill_category", _("skill_category")
        SKILL_SUB_CATEGORY = "skill_sub_category", _("skill_sub_category")
        SKILL = "skill", _("skill")

    choice_type = models.CharField(max_length=30, choices=ChoiceType.choices)

    name = models.CharField(max_length=50)

    class Meta:
        indexes = [
            models.Index(fields=["name", "choice_type"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["name", "choice_type"],
                name="name_choice_type_unique",
            ),
        ]


class People(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    nickname = models.CharField(max_length=50)

    class PreferredEmploymentType(models.TextChoices):
        FULL_TIME = "Full-Time", _("Full-Time")
        PART_TIME = "Part-Time", _("Part-Time")
        FREELANCER = "Freelancer", _("Freelancer")
        CONTRACT = "Contract", _("Contract")

    preferred_employment_type = models.CharField(
        max_length=30, choices=PreferredEmploymentType.choices
    )

    location = models.PointField(null=True, blank=True, srid=4326)

    other = models.JSONField(null=True, blank=True)


class PeopleChoice(models.Model):
    people = models.ForeignKey(People, on_delete=models.CASCADE)
    choice = models.ForeignKey(ChoiceList, on_delete=models.CASCADE)


@receiver(pre_save, sender=People)
def set_location(sender, instance, **kwargs):
    # Address: XGRX+FR5, Shraddha Colony Rd, Yashwant Nagar, Jalgaon, Maharashtra 425001, India
    # Location: 20.991135,75.549613

    # jalgaon maharashtra
    # 20.99104243283295, 75.54956320158519 # Home kp
    # 20.996706, 75.549995 #1 shree hospital gp
    # 20.982255, 75.5518 #2 mahabal
    # 21.014862, 75.502924 #3 college
    
    latitude = 20.99678499312419
    longitude = 75.55009023507328
    instance.location = Point(float(longitude), float(latitude), srid=4326)


# @receiver(pre_save, sender=People)
# def set_location(sender, instance, **kwargs):
#     if instance.city and instance.region:
#         # Replace 'your_api_key' with your actual Google Maps API key
#         API_KEY = 'your_api_key'
#         address = f"{instance.city}, {instance.region}"
#         url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"

#         response = requests.get(url)
#         data = response.json()

#         if data['status'] == 'OK':
#             latitude = data['results'][0]['geometry']['location']['lat']
#             longitude = data['results'][0]['geometry']['location']['lng']
#             instance.location = Point(longitude, latitude)