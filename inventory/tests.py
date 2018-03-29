from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from datetime import timedelta
from json import dumps

from inventory.models import Item, Loan, Tag


