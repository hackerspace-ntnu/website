from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase

from json import dumps

from inventory.models import Tag
from inventory.forms import TagForm

"""
TAG
- skjekke at man ikke kan opprette en rekursiv løkke i formen.
- skjekke at evt rekursive løkker oppløses ved å endre et item som har en av disse taggene.
- skjekke at evt rekursive løkker oppløses ved å endre en tag i denne løkken.
- skjekke at alle items beslektet til en tag får sine tags endret som forventet når man endrer parent tag .

"""


def create_user(number):
    name = 'test' + str(number)
    user = User.objects.create(username=name, password=name, email=name + "@test.com")
    return user


def give_permissions(user: User):
    permissions = []
    for perm_name in ['add_item', 'change_item', 'delete_item', 'add_loan', 'change_loan', 'delete_loan',
                      'add_loanitem', 'change_loanitem', 'delete_loanitem', 'add_tag', 'change_tag', 'delete_tag']:
        permission = Permission.objects.get(codename=perm_name)
        user.user_permissions.add(permission)


class TagTest(TestCase):
    def setUp(self):
        # User with all permissions
        self.perm_user = create_user(0)
        give_permissions(self.perm_user)

        # User without permissions
        self.regular_user = create_user(1)

    def test_two_hundred_get(self):
        self.client.force_login(self.perm_user)
        response = self.client.get(reverse('inventory:add_tag'))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_get(self):
        response = self.client.get(reverse('inventory:add_tag'))
        self.assertEqual(response.status_code, 200)

    def test_unique_tag_name(self):
        """ Tester at man ikke kan lage en ny tag med samme navn som en eksisterende tag, og at man får en feilmelding """
        self.client.force_login(self.perm_user)
        tag1 = Tag.objects.create(name='tag1')
        response = self.client.post(reverse('inventory:add_tag', args=(0,)),
                                    {'name': 'tag1', 'parent_tag_ids': dumps(['0', 0])})
        self.assertEqual(response.status_code, 200)

        # Skjekker at det ikke ble opprettet noen tag
        self.assertEqual(len(Tag.objects.all()), 1)

        # Skjeker at man får riktig feilmelding i formen.
        self.assertFormError(response, 'form', "name", TagForm.EXISTING_NAME)

    def test_set_parent_tag(self):
        """ Tester at parent tag blir korrekt satt, og at siden redirecter riktig. """
        self.client.force_login(self.perm_user)
        tag1 = Tag.objects.create(name='tag1')
        response = self.client.post(reverse('inventory:add_tag', args=(0,)),
                                    {'name': 'tag2', 'parent_tag_ids': dumps(['0', tag1.id])}, follow=True)

        self.assertEqual(response.status_code, 200)

        # Test that page redirects after post.
        self.assertEqual(response.redirect_chain, [('/inventory/', 302)])

        # Test that parent tag is correctly set.
        new_tag = Tag.objects.get(name='tag2')
        self.assertEqual(tag1.id, new_tag.parent_tag.id)

    def test_recursive_tag_cirle_not_possible_1(self):
        """ Tester at man ikke kan lage en rekursiv løkke med tags i formen. """
        self.client.force_login(self.perm_user)
        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2', parent_tag=tag1)

        response = self.client.post(reverse('inventory:add_tag', args=(tag1.id,)),
                                    {'name': 'tag1', 'parent_tag_ids': dumps([tag1.id, tag2.id])})
        self.assertEqual(response.status_code, 200)

        # Skjekker at det ikke ble opprettet noen tag
        self.assertEqual(tag1.parent_tag, None)

        # Skjeker at man får riktig feilmelding i formen.
        self.assertFormError(response, 'form', "parent_tag", TagForm.RECURSIVE_PARENT.format(tag2))

    def test_recursive_tag_cirle_not_possible_2(self):
        """ Tester at man ikke kan lage en rekursiv løkke med tags i formen (tester for to lag) """
        self.client.force_login(self.perm_user)
        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2', parent_tag=tag1)
        tag3 = Tag.objects.create(name='tag3', parent_tag=tag2)

        response = self.client.post(reverse('inventory:add_tag', args=(tag1.id,)),
                                    {'name': 'tag1', 'parent_tag_ids': dumps([tag1.id, tag3.id])})
        self.assertEqual(response.status_code, 200)

        # Skjekker at det ikke ble opprettet noen tag
        self.assertEqual(tag1.parent_tag, None)

        # Skjeker at man får riktig feilmelding i formen.
        self.assertFormError(response, 'form', "parent_tag", TagForm.RECURSIVE_PARENT.format(tag3))

    def test_itself_as_parent(self):
        """ Tester at man ikke kan endre en tag til å sette seg selv som parent. """
        self.client.force_login(self.perm_user)
        tag1 = Tag.objects.create(name='tag1')

        response = self.client.post(reverse('inventory:add_tag', args=(tag1.id,)),
                                    {'name': 'tag1', 'parent_tag_ids': dumps([tag1.id, tag1.id])})
        self.assertEqual(response.status_code, 200)

        # Skjekker at det ikke ble opprettet noen tag
        self.assertEqual(tag1.parent_tag, None)

        # Skjeker at man får riktig feilmelding i formen.
        self.assertFormError(response, 'form', "parent_tag", TagForm.SELF_AS_PARENT)


    # Test message og button_message ved alle tilfellene.

class ItemTest(TestCase):
    def setUp(self):
        # User with all permissions
        self.perm_user = create_user(0)
        give_permissions(self.perm_user)

        # User without permissions
        self.regular_user = create_user(1)

    def test_two_hundred_get(self):
        self.client.force_login(self.perm_user)
        response = self.client.get(reverse('inventory:add_item'))
        self.assertEqual(response.status_code, 200)


class IndexView(TestCase):
    def setUp(self):
        # User with all permissions
        self.perm_user = create_user(0)
        give_permissions(self.perm_user)

        # User without permissions
        self.regular_user = create_user(1)

    def test_two_hundred(self):
        self.client.force_login(self.perm_user)
        response = self.client.get(reverse('inventory:index'))
        self.assertEqual(response.status_code, 200)
