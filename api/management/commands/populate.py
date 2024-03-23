# import json

# from django.conf import settings
# from django.core.management.base import BaseCommand

# from ...models import ChoiceList


# def create_choice_list(data: list):
#     choice_list_bulk_create = []

#     for item in data:
#         choice_list_bulk_create.append(
#             ChoiceList(
#                 name=item.get("name"),
#                 choice_type=item.get("choice_type"),
#                 parent=item.get("parent", None),
#             )
#         )

#     ChoiceList.objects.bulk_create(choice_list_bulk_create, ignore_conflicts=True)
#     choice_list_objs = ChoiceList.objects.filter(
#         name__in=[
#             choice_list_create_obj.name
#             for choice_list_create_obj in choice_list_bulk_create
#         ]
#     )

#     choice_name_to_obj_map = {}
#     for choice_obj in choice_list_objs:
#         choice_name_to_obj_map[choice_obj.name] = choice_obj

#     next_data = []
#     for item in data:
#         item_name = item.get("name")
#         item_child = item.get("child", [])

#         for child in item_child:
#             child_data = {**child, "parent": choice_name_to_obj_map.get(item_name)}
#             next_data.append(child_data)

#         next_data += [child for child in item.get("child", [])]

#     if next_data:
#         create_choice_list(data=next_data)


# class Command(BaseCommand):
#     help = "Populate ChoiceList model"

#     def handle(self, *args, **options):
#         with open(settings.BASE_DIR / "skills.json") as json_file:
#             json_data = json.load(json_file)
#             print(json_data)

#             create_choice_list(data=json_data)

import json

from django.conf import settings
from django.core.management.base import BaseCommand

from ...models import ChoiceList


def create_choice_list(data: list):
    choice_list_bulk_create = []

    for item in data:
        choice_list_bulk_create.append(
            ChoiceList(
                name=item.get("name"),
                choice_type=item.get("choice_type"),
                parent=item.get("parent", None),
            )
        )

    ChoiceList.objects.bulk_create(choice_list_bulk_create, ignore_conflicts=True)
    choice_list_objs = ChoiceList.objects.filter(
        name__in=[
            choice_list_create_obj.name
            for choice_list_create_obj in choice_list_bulk_create
        ]
    )

    choice_name_to_obj_map = {}
    for choice_obj in choice_list_objs:
        choice_name_to_obj_map[choice_obj.name] = choice_obj

    # for key, value in choice_name_to_obj_map.items():
    #     print(f"{key}: {value}")
    

    next_data = []
    for item in data:
        item_name = item.get("name")
        item_child = item.get("child", []) # list of dictionary

        for child in item_child:
            child_data = {**child, "parent": choice_name_to_obj_map.get(item_name)}
            # print(f"child_data: {child_data}")
            next_data.append(child_data)

        next_data += [child for child in item.get("child", [])]

    if next_data:
        print("\n\n\nnext_data: ", next_data)
        create_choice_list(data=next_data)


class Command(BaseCommand):
    help = "Populate ChoiceList model"

    def handle(self, *args, **options):
        try:
            with open(settings.BASE_DIR / "skills.json") as json_file:
                json_data = json.load(json_file)

            create_choice_list(data=json_data)

            self.stdout.write(self.style.SUCCESS('Successfully populated ChoiceList model.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An error occurred while populating ChoiceList model: {str(e)}'))