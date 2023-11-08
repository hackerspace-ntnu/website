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
def upload(string):
    string = string.decode("latin-1")
    data = []
    lines = string.split("\\r\\n")
    for line in lines:
        if line == "":
            continue
        dataline = []
        parts = line.split(";")
        for part in parts:
            dataline.append(part)
        data.append(dataline)

    print(data, "\n\n", data[1])

    items = []

    for i in range(len(data)):
        items.append(
            {
                "name": data[i][0],
                "stock": data[i][1],
                "unknown_stock": data[i][2],
                "can_loan": data[i][3],
                "description": data[i][4],
                "thumbnail": data[i][5],
                "location": data[i][6],
                "max_loan_duration": data[i][7],
                "views": data[i][8],
            }
        )

    print(items)

    run_script(items)


@transaction.atomic
def run_script(list_items: List[dict]):
    # items: List[Item] = []
    for item in list_items:
        item = Item(
            name=item["name"],
            stock=item["stock"],
            unknown_stock=item["unknown_stock"],
            can_loan=item["can_loan"],
            description=item["description"],
            location=item["location"],
            max_loan_duration=item["max_loan_duration"],
            views=item["views"],
        )
        """ Item.objects.update_or_create(
            name=item["name"], defaults={"stock": item["stock"]}
        ) """
