from django import template
from django.template.loader_tags import IncludeNode, do_include

register = template.Library()


class ChildrenIncludedNode(IncludeNode):
    def __init__(self, nodelist, include_node):
        self.nodelist = nodelist
        self.template = include_node.template
        self.extra_context = include_node.extra_context
        self.isolated_context = include_node.isolated_context

    def render(self, context):
        context["children"] = self.nodelist.render(context)
        return super().render(context)


@register.tag("includechildren")
def include_children(parser, token):
    """Extends the include tag to add children to the context.
    Any HTML between `includechildren` and `endincludechildren` are
    inserted in the `children` context variable.

    Usage:
    ```html
    <!-- page.html -->
        {% includechildren "template.html" %}
            <h1>Children</h1>
        {% endincludechildren %}

    <!-- template.html -->
        <div>
            {{ children }}
        </div>
    ```
    """
    nodelist = parser.parse(("endincludechildren",))
    parser.delete_first_token()

    include_node = do_include(parser, token)

    return ChildrenIncludedNode(
        nodelist,
        include_node,
    )
