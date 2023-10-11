from typing import List

import pandas as pd
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
def run_script(list_items: List[dict]):
    items: List[Item] = []
    print(items)
    for item in list_items:
        item = Item(name=item["name"], stock=item["stock"])
        Item.objects.update_or_create(
            name=item["name"], defaults={"stock": item["stock"]}
        )


columnnames = [
    "name",
    "stock",
    "unknown_stock",
    "can_loan",
    "description",
    "thumbnail",
    "location",
    "max_loan_duration",
    "views",
]
data = pd.read_csv("inventory/data.csv", names=columnnames, header=None, sep=";")

items = [dict]

for i in range(len(data)):
    items.append(
        {
            "name": data.loc[i, "name"],
            "stock": data.loc[i, "stock"],
            "unknown_stock": data.loc[i, "unknown_stock"],
            "can_loan": data.loc[i, "can_loan"],
            "description": data.loc[i, "description"],
            "thumbnail": data.loc[i, "thumbnail"],
            "location": data.loc[i, "location"],
            "max_loan_duration": data.loc[i, "max_loan_duration"],
            "views": data.loc[i, "views"],
        }
    )
