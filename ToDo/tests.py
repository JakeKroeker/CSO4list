from django.test import TestCase
from django.test import Client
from django.test.utils import setup_test_environment
from .models.ToDoItem import ToDoItem
from .models.ToDoList import ToDoList

class TodoTest(TestCase):

    #ToDo: refactor this whole test setup. It's bad last minute setup.
    def test_main(self):
        """
        Logging into our list.
        """
        client = Client()
        response = client.post('/login_create', {'username': 'imatestuser', 'password': 'imatestuser'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ToDo Item Name")


        """
        Creating list items.
        """
        #ToDo: test injection
        names = ['test1', 'this is test 2', '; DROP TABLE auth_user;']
        item_descriptions = ['', 'test1', 'test2', '; DROP TABLE auth_user;']
        due_dates = ['', '2025-11-01T12:12', '1111-11-01T12:12']
        for name in names:
            for desc in item_descriptions:
                for date in due_dates:
                    response = client.post('/create', {'item_name': name,
                                            'item_description': desc,
                                            'due_date': date}, follow=True)
                    self.assertEqual(response.status_code, 200)
                    self.assertContains(response, name)
                    self.assertContains(response, desc)
                    self.assertContains(response, date.replace("T", " "))

        desc = 'this should fail because no name'
        client.post('/create', {'name': '',
                                'description': desc,
                                'due_date': ''}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, desc)

        desc = 'this should fail because no name'
        client.post('/create', {'name': '',
                                'description': desc,
                                'due_date': '2025-11-01T12:12'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, desc)


        """
        Updating list items.
        """ 
        lists = ToDoList.objects.all()

        list = lists[0]

        entries = list.todoitem_set.all()

        for item in entries:

            response = client.get(f'/item/{item.id}')
            self.assertEqual(response.status_code, 200)
            
            response = client.post(f'/update/{item.id}', {
                                    'item_name': 'new name',
                                    'item_description': 'new description',
                                    'due_date': '',
                                    'complete': True}, follow=True)
            
        for item in entries:
            item.refresh_from_db()
            self.assertEqual(item.name, 'new name')
            self.assertEqual(item.description, 'new description')
            self.assertEqual(item.complete, True)
            #How do I check times again? Todo: put in time test

        """
        Updating list items.
        """ 
        list.refresh_from_db()

        entries = list.todoitem_set.all()

        for item in entries:
            response = client.get(f'/item/{item.id}')
            self.assertEqual(response.status_code, 200)
            client.post(f'/delete/{item.id}', {}, follow=True)
            
        entries = list.todoitem_set.all()
        self.assertFalse(entries.count(), 0)

