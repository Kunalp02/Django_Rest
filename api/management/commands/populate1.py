import json

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import ChoiceList


def create_choice_list(data: dict):
    choice_list_bulk_create = []

    for key, value in data.items():
        choice_list_bulk_create.append(
            ChoiceList(
                name=key,
                choice_type=ChoiceList.ChoiceType.SKILL_CATEGORY,
                parent=None,
            )
        )

    ChoiceList.objects.bulk_create(choice_list_bulk_create, ignore_conflicts=True)


    choice_list_objs = ChoiceList.objects.filter(
        name__in=[
            choice_list_create_obj.name
            for choice_list_create_obj in choice_list_bulk_create
        ]
    )

    print(choice_list_objs)

    choice_name_to_obj_map = {}
    for choice_obj in choice_list_objs:
        choice_name_to_obj_map[choice_obj.name] = choice_obj

    next_data = []

    for item_name, item_child in data.items():
        for child in item_child:
            child_data = {**child, "parent": choice_name_to_obj_map.get(item_name)}
            next_data.append(child_data)


    if next_data:
        create_choice_list(data=next_data)


class Command(BaseCommand):
    help = "Populate ChoiceList model"

    def handle(self, *args, **options):
        with open(settings.BASE_DIR / "skills__.json") as json_file:
            json_data = json.load(json_file)
            print(json_data)

            create_choice_list(data=json_data)