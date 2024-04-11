from dataclasses import dataclass
from typing import List

from django import template
from django.template.loader_tags import IncludeNode, do_include

register = template.Library()


@dataclass
class SlotNode:
    name: str
    nodelist: template.NodeList


class SlotsIncludedNode(IncludeNode):
    def __init__(self, slots: List[SlotNode], include_node: IncludeNode):
        self.slots = slots

        self.template = include_node.template
        self.extra_context = include_node.extra_context
        self.isolated_context = include_node.isolated_context

    def render(self, context):
        for slot in self.slots:
            context[slot.name] = slot.nodelist.render(context)
        return super().render(context)


END_SLOTS = "endslots"
SLOT = "slot"


@register.tag("includeslots")
def include_slots(parser, token):
    """Extends the include tag to add slots to the context.
    Any HTML between `includeslots` and the next `slot` or
    `endslots` are inserted in the context variable as the
    slot argument.

    Usage:
    ```html
    <!-- page.html -->
        {% includeslots "template.html" %}
        {% slot firstslot %}
            <h1>Children</h1>
        {% slot second_one %}
            <button>Click me</button>
        {% endslots %}

    <!-- template.html -->
        <div>
            {{ firstslot }}
            <span>{{ second_one }}</span>
        </div>
    ```
    """

    nodelist = parser.parse((SLOT, END_SLOTS))
    first_token = token
    token = parser.next_token()

    slots: List[SlotNode] = []
    while token.contents.startswith(SLOT):
        bits = token.split_contents()
        if len(bits) != 2:
            raise template.TemplateSyntaxError(
                f"Requires one argument, got {len(bits) - 1} for {token.contents}"
            )
        nodelist = parser.parse((SLOT, END_SLOTS))
        slots.append(SlotNode(bits[1], nodelist))
        token = parser.next_token()

    include_node = do_include(parser, first_token)

    return SlotsIncludedNode(
        slots,
        include_node,
    )
