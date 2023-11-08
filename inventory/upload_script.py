import csv
from io import StringIO
from typing import List

from django.db import transaction

from inventory.models.item import Item

# from typing import List

# HTML template for å laste opp csv
# Link til html siden
# Form for å laste opp csvfil
# View tar imot form og verdier fra csv filen
# Sender verdier til run_script
# View sender success tilbake
# Behandle at idioter sender feil data (som de absolutt kommer til å gjøre)


@transaction.atomic
def upload(input):
    input = input.decode("latin-1")

    delimiter = {}
    for line in input.split("\n"):
        if ";" in line:
            delimiter[";"] = delimiter.get(";", 0) + 1
        if "," in line:
            delimiter[","] = delimiter.get(",", 0) + 1

    csv_file = csv.reader(StringIO(input), delimiter=max(delimiter, key=delimiter.get))

    items = []
    for i, row in enumerate(csv_file):
        if i == 0:
            continue
        items.append(
            {
                "location": row[0],
                "name": row[1],
                "stock": row[2],
                "unknown_stock": True if row[2] == "" else False,
                "can_loan": row[4],
                "max_loan_duration": row[5],
                "description": row[6],
            }
        )

    for item in items:
        print(item)

    run_script(items)


@transaction.atomic
def run_script(list_items: List[dict]):
    # items: List[Item] = []
    for item in list_items:
        item = Item(
            location=item["location"],
            name=item["name"],
            stock=item["stock"],
            unknown_stock=item["unknown_stock"],
            can_loan=item["can_loan"],
            max_loan_duration=item["max_loan_duration"],
            description=item["description"],
        )
        """ Item.objects.update_or_create(
            name=item["name"], defaults={"stock": item["stock"]}
        ) """
