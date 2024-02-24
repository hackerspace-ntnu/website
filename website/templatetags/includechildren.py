from django import template
from django.template.library import token_kwargs
from django.template.loader_tags import IncludeNode, construct_relative_path

register = template.Library()


class NewIncludeNode(IncludeNode):
    def __init__(self, nodelist, file_name, context, *args, **kwargs):
        super().__init__(file_name, *args, extra_context=context, **kwargs)
        self.nodelist = nodelist

    def render(self, context):
        context["children"] = self.nodelist.render(context)
        return super().render(context)


@register.tag("includechildren")
def include_children(parser, token):
    bits = token.split_contents()
    if len(bits) < 2:
        raise template.TemplateSyntaxError(
            "'%s' takes at least one argument (name of the template to be included)"
            % bits[0]
        )

    file_name = bits[1]

    nodelist = parser.parse(("endincludechildren",))
    parser.delete_first_token()

    remaining_bits = bits[2:]
    arguments = {}
    while remaining_bits:
        key = remaining_bits.pop(0)
        if key == "with":
            arguments = token_kwargs(remaining_bits, parser)

    file_name = construct_relative_path(parser.origin.template_name, file_name)
    print(arguments)
    return NewIncludeNode(
        nodelist,
        parser.compile_filter(file_name),
        arguments,
    )
