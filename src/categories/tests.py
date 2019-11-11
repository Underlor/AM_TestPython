import json
from django.test import TestCase, TransactionTestCase

from categories.models import Category


class CategoriesCreateTests(TestCase):
    def test_right_request(self):
        test_data = {
            "name": "Category 1",
            "children": [
                {
                    "name": "Category 1.1"
                },
                {
                    "name": "Category 1.1.1",
                    "children": [
                        {
                            "name": "Category 1.1.1.1"
                        },
                        {
                            "name": "Category 1.1.1.2"
                        }
                    ]
                }
            ]
        }
        response = self.client.post('/categories/', json.dumps(test_data), content_type='json')

        self.assertEqual(response.status_code, 200)

        self.assertEqual(Category.objects.filter(parent=None).count(), 1)
        self.assertEqual(Category.objects.exclude(parent=None).count(), 4)

        self.assertEqual(Category.objects.get(name='Category 1.1.1').get_children().count(), 2)

        self.assertEqual(Category.objects.get(name='Category 1.1.1.1').get_siblings().count(), 1)
        self.assertEqual(Category.objects.get(name='Category 1.1.1.1').get_siblings().first().name, 'Category 1.1.1.2')

    def test_empty_request(self):
        test_data = {}
        response = self.client.post('/categories/', json.dumps(test_data), content_type='json')

        self.assertEqual(response.status_code, 400)

    def test_bad_request(self):
        test_data = {"test": "case"}
        response = self.client.post('/categories/', json.dumps(test_data), content_type='json')
        self.assertEqual(response.status_code, 400)

    def test_unique_name(self):
        test_data = {"name": "Category 1.1"}
        response = self.client.post('/categories/', json.dumps(test_data), content_type='json')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/categories/', json.dumps(test_data), content_type='json')
        self.assertEqual(response.status_code, 400)


class CategoryGetTests(TestCase):
    def setUp(self):
        self.items = []

        self.items.append(Category.objects.create(name='Category 1'))

        self.items.append(Category.objects.create(name='Category 1.1', parent=self.items[0]))
        self.items.append(Category.objects.create(name='Category 1.2', parent=self.items[0]))
        self.items.append(Category.objects.create(name='Category 1.3', parent=self.items[0]))

        self.items.append(Category.objects.create(name='Category 1.2.1', parent=self.items[2]))
        self.items.append(Category.objects.create(name='Category 1.2.2', parent=self.items[2]))

    def test_not_exists_item(self):
        response = self.client.get(f'/categories/{0}/')
        self.assertEqual(response.status_code, 404)

    def test_success_root_item(self):
        root_category = self.items[0]

        response = self.client.get(f'/categories/{root_category.id}/')
        response_items = json.loads(response.content)

        self.assertEqual(response_items.get('name'), 'Category 1')
        self.assertEqual(len(response_items.get('children')), 3)

    def test_success_item_with_parent(self):
        category_item = self.items[1]

        response = self.client.get(f'/categories/{category_item.id}/')
        response_items = json.loads(response.content)

        self.assertEqual(response_items.get('name'), 'Category 1.1')
        self.assertEqual(response_items.get('children'), [])


class TaskTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        test_data = """{"name": "Category 1","children": [{"name": "Category 1.1","children": 
        [{"name": "Category 1.1.1", "children": [{"name": "Category 1.1.1.1"},
        {"name": "Category 1.1.1.2"},{"name": "Category 1.1.1.3"}]}, 
        {"name": "Category 1.1.2","children": [{"name": "Category 1.1.2.1"},{"name": "Category 1.1.2.2"}, 
        {"name": "Category 1.1.2.3"}]}]},{"name": "Category 1.2","children": [{"name": "Category 1.2.1"}, 
        {"name": "Category 1.2.2","children": [{"name": "Category 1.2.2.1"},{"name": "Category 1.2.2.2"}]}]}]} """
        response = self.client.post('/categories/', test_data, content_type='json')
        self.assertEqual(response.status_code, 200)

    def test_first_case(self):
        raw_check_data = """{"id": 2,"name": "Category 1.1","parents": [{"id": 1,"name": "Category 1"}],"children": [
        {"id": 3,"name": "Category 1.1.1"},{"id": 7,"name": "Category 1.1.2"}],"siblings": [{"id": 11,
        "name": "Category 1.2"}]} """
        check_data = json.loads(raw_check_data)

        response = self.client.get(f'/categories/{2}/')

        self.assertEqual(json.loads(response.content), check_data)

    def test_second_case(self):
        raw_check_data = """{"id": 8,"name": "Category 1.1.2.1","parents": [{"id": 7,"name": "Category 1.1.2"},
        {"id": 2,"name": "Category 1.1"},{"id": 1,"name": "Category 1"}],"children": [],"siblings": [{"id": 9,
        "name": "Category 1.1.2.2"},{"id": 10,"name": "Category 1.1.2.3"}]} """
        check_data = json.loads(raw_check_data)

        response = self.client.get(f'/categories/{8}/')

        self.assertEqual(json.loads(response.content), check_data)
