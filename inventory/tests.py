from django.contrib.auth.models import User, Permission
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils import timezone

from datetime import timedelta
from json import dumps

from inventory.models import Item, Loan, Tag
from inventory.forms import TagForm
from inventory.views import AddTag


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
        response = self.client.get(reverse('inventory:add_tag'), follow=True)
        self.assertEqual(response.redirect_chain, [('/authentication/login/?next=/inventory/add_tag/', 302)])
        self.assertEqual(response.status_code, 200)

        # TODO må skjekke at en bruker som ikke er logget inn blir redirectet til login.

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

    def test_set_parent_tag_new_tag(self):
        """ Tester at parent tag blir korrekt satt, og at siden redirecter riktig. """
        self.client.force_login(self.perm_user)
        tag1 = Tag.objects.create(name='tag1')
        response = self.client.post(reverse('inventory:add_tag', args=(0,)),
                                    {'name': 'tag2', 'parent_tag_ids': dumps(['0', tag1.id])}, follow=True)

        # Test that page redirects after post.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/inventory/', 302)])

        # Test that parent tag is correctly set.
        new_tag = Tag.objects.get(name='tag2')
        self.assertEqual(tag1.id, new_tag.parent_tag.id)

    def test_set_parent_tag_on_existing_tag(self):
        """ Tester at parent tag blir registrert når man endrer en eksisterende tag. """
        self.client.force_login(self.perm_user)
        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2')
        response = self.client.post(reverse('inventory:add_tag', args=(tag2.id,)),
                                    {'name': 'tag2', 'parent_tag_ids': dumps([tag2.id, tag1.id])}, follow=True)

        # Test that page redirects after post.
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [('/inventory/', 302)])

        # Test that parent tag is correctly set.
        changed_tag = Tag.objects.get(name='tag2')
        self.assertEqual(tag1.id, changed_tag.parent_tag.id)

    def test_change_parent_tag_on_existing_tag_affect_related_items(self):
        """ Tester at items som har en tag, får endret tagger hvis man endrer parent_tag til denne taggen. """
        self.client.force_login(self.perm_user)
        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2')

        item1 = Item.objects.create(name='item1')
        item1.tags.add(tag2)

        response = self.client.post(reverse('inventory:add_tag', args=(tag2.id,)),
                                    {'name': 'tag2', 'parent_tag_ids': dumps([tag2.id, tag1.id])}, follow=True)

        # Test that item1 get both tag1 and tag2 as tags, when tag1 is set as parent tag to tag2.
        tags = item1.tags.all()
        self.assertEqual(2, len(tags))
        self.assertTrue(tag1 in tags and tag2 in tags)

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

    def test_context_new_tag_get(self):
        """ Tester at overskrift og knappetekst er riktig når man oppretter en ny tag. """
        self.client.force_login(self.perm_user)
        response = self.client.get(reverse('inventory:add_tag'))
        self.assertEqual(AddTag.message_new, response.context['message'])
        self.assertEqual(AddTag.button_message_new, response.context['button_message'])

    def test_context_change_tag_get(self):
        """ Tester at overskrift og knappetekst er riktig når man endrer en tag. """
        self.client.force_login(self.perm_user)
        tag = Tag.objects.create(name="tag")
        response = self.client.get(reverse('inventory:add_tag', args=(tag.id,)))
        self.assertEqual(AddTag.message_change, response.context['message'])
        self.assertEqual(AddTag.button_message_change, response.context['button_message'])

    def test_context_new_tag_post_error(self):
        """ Tester context når man oppretter ny tag, og får feilmeldinger. """
        self.client.force_login(self.perm_user)
        tag = Tag.objects.create(name="tag")
        response = self.client.get(reverse('inventory:add_tag'), {'name': 'tag'})
        self.assertEqual(AddTag.message_new, response.context['message'])
        self.assertEqual(AddTag.button_message_new, response.context['button_message'])

    def test_context_change_tag_post_error(self):
        """ Tester context når man endrer en tag, og får feilmeldinger. """
        self.client.force_login(self.perm_user)
        tag1 = Tag.objects.create(name="tag1")
        tag2 = Tag.objects.create(name="tag2")
        response = self.client.get(reverse('inventory:add_tag', args=(tag1.id,)), {'name': 'tag2'})
        self.assertEqual(AddTag.message_change, response.context['message'])
        self.assertEqual(AddTag.button_message_change, response.context['button_message'])

    # TODO:
    """
    TAG
    - skjekke at evt rekursive løkker oppløses ved å endre et item som har en av disse taggene.
    - skjekke at evt rekursive løkker oppløses ved å endre en tag i denne løkken.
    - skjekke at alle items beslektet til en tag får sine tags endret som forventet når man endrer parent tag.
    - kan teste at eksisterende parent tag kommer opp i context.

    """


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


class LoanTest(TestCase):
    def setUp(self):
        # User with all permissions
        self.perm_user = create_user(number=0)
        give_permissions(self.perm_user)

        # User without permissions
        self.regular_user = create_user(number=1)

    def test_all_loans_in_context(self):
        # TODO lag fake database for å skjekke dette, her er det ingen Loan-objekter
        past = timezone.now() - timedelta(days=1)
        paster = timezone.now() - timedelta(days=2)
        future = timezone.now() + timedelta(days=1)

        Loan.objects.create(loan_date=past, return_date=future)
        Loan.objects.create(loan_date=paster, return_date=past)
        Loan.objects.create(loan_date=past, return_date=future, date_returned=future)
        Loan.objects.create(loan_date=paster, return_date=future, date_returned=past)

        self.client.force_login(self.perm_user)
        response = self.client.get(reverse('inventory:administrate_loans'))

        active_loans = response.context['active_loans']
        late_loans = response.context['late_loans']
        old_loans = response.context['old_loans']

        self.assertEqual(len(Loan.objects.all()), len(active_loans | late_loans | old_loans),
                         "Ikke alle lån-objekter sendes inn til template.")
