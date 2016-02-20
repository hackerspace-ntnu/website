from django.contrib.admin.models import LogEntry, ADDITION, CHANGE
from django.contrib.contenttypes.models import ContentType


def change(request, news_object):
    LogEntry.objects.log_action(
            user_id=request.user.id,
            content_type_id=ContentType.objects.get_for_model(news_object).pk,
            object_id=news_object.id,
            object_repr=news_object.title,
            action_flag=CHANGE,
            change_message="Changed")

