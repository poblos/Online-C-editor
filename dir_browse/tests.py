from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse
from django.contrib import auth
from .models import *
from .forms import *

user_test_name = 'testuser'
user_test_password = '12345'
too_long_name = 'test_name_name_test_name_name_test_name_name_test_name_nametest_name_nametest_name_nametest_name_nametest_name_nametest_name_nametest_name_nametest_natest_name_nametest_name_nametest_name_nametest_name'

def standard_setup():
    standard = Standard.objects.create(name="c89")
    processor = Processor.objects.create(name="STM8")
    CompilationSettings.objects.create(standard = standard, processor = processor)

def register_and_login(self):
    self.user = User.objects.create_user(username=user_test_name, password=user_test_password)
    self.client.login(username=user_test_name, password=user_test_password)

def login(self):
    self.client.login(username=user_test_name, password=user_test_password)

def logout(self):
    self.client.logout()

def access_only_for_logged_in(self, url, proper):
    response = self.client.get(reverse(url))
    self.assertRedirects(response, proper)
    register_and_login(self)
    response = self.client.get(reverse(url))
    self.assertEqual(response.status_code, 200)

def access_only_for_logged_in_pk(self, url, pk, proper):
    response = self.client.get(reverse(url, kwargs={'pk':pk}))
    self.assertRedirects(response, proper)
    login(self)
    response = self.client.get(reverse(url, kwargs={'pk':pk}))
    self.assertEqual(response.status_code, 200)

def create_file(self, name="test_name", desc="test_desc", text="test_text"):
    return File.objects.create(name=name, desc=desc, text=text, owner=self.user)

def create_directory(self, name="test_name", desc="test_desc"):
    return Directory.objects.create(name=name, desc=desc, owner=self.user)

#####################
##### View Tests ####
#####################
class LoginViewTests(TestCase):
    def setUp(self):
        standard_setup()

    def test_logged_in_redirected(self):
        register_and_login(self)
        response = self.client.get(reverse('dir_browse:login'))
        self.assertRedirects(response,reverse('dir_browse:index'))
    
    def test_logged_out_not_redirected(self):
        response = self.client.get(reverse('dir_browse:login'))
        self.assertEqual(response.status_code, 200)

    def test_bad_login(self):
        login(self)
        user = auth.get_user(self.client)
        self.assertFalse(user.is_authenticated)


class IndexViewTests(TestCase):
    def setUp(self):
        standard_setup()

    def test_access_only_for_logged_in(self):
        access_only_for_logged_in(self, 'dir_browse:index','/dir_browse/login/?next=/dir_browse/')

    def test_delete_file(self):
        register_and_login(self)
        file = create_file(self)
        response = self.client.get(reverse('dir_browse:delete_file',kwargs={'pk':file.pk}))
        file = File.objects.get(id = file.pk)
        self.assertFalse(file.alive)

    def test_delete_dir(self):
        register_and_login(self)
        dir = create_directory(self)
        response = self.client.get(reverse('dir_browse:delete_dir',kwargs={'pk':dir.pk}))
        dir = Directory.objects.get(id = dir.pk)
        self.assertFalse(dir.alive)

    def test_compile(self):
        register_and_login(self)
        file = create_file(self,"test_name", "test_desc","int main() {return 0;}")
        response = self.client.get(reverse('dir_browse:compile',kwargs={'pk':file.pk}))
        self.assertTrue(file.alive)

class FileDetailViewTests(TestCase):
    def setUp(self):
        standard_setup()

    def test_access_only_for_logged_in(self):
        register_and_login(self)
        file = File.objects.create(name="TestFile", owner = self.user)
        logout(self)
        access_only_for_logged_in_pk(self, 'dir_browse:file_detail', file.id, '/dir_browse/login/?next=/dir_browse/file_detail/1/')

class DirectoryDetailViewTests(TestCase):
    def setUp(self):
        standard_setup()

    def test_access_only_for_logged_in(self):
        register_and_login(self)
        dir = Directory.objects.create(name="TestDirectory", owner = self.user)
        logout(self)
        access_only_for_logged_in_pk(self, 'dir_browse:dir_detail', dir.id, '/dir_browse/login/?next=/dir_browse/dir_detail/1/')


#####################
#### Model Tests ####
#####################

class FileModelTest(TestCase):
    def test_file_creation(self):
        register_and_login(self)
        file = create_file(self)
        self.assertTrue(isinstance(file,File))
        self.assertEqual(file.__str__(), file.name)

    def test_file_creation_no_user(self):
        try:
            File.objects.create(name="test_name")
            self.fail("File without owner succesfully added to database")
        except DatabaseError:
            pass

    def test_file_creation_too_long_name(self):
        try:
            File.objects.create(name=too_long_name)
            self.fail("File with too long name succesfully added to database")
        except DatabaseError:
            pass

class DirectoryModelTest(TestCase):
    def test_directory_creation(self):
        register_and_login(self)
        directory = create_directory(self)
        self.assertTrue(isinstance(directory,Directory))
        self.assertEqual(directory.__str__(), directory.name)

    def test_directory_creation_no_user(self):
        try:
            Directory.objects.create(name="test_name")
            self.fail("Directory without owner succesfully added to database")
        except DatabaseError as e:
            pass

    def test_directory_creation_too_long_name(self):
        try:
            Directory.objects.create(name=too_long_name)
            self.fail("Directory with too long name succesfully added to database")
        except DatabaseError:
            pass

#####################
#### Forms Tests ####
#####################
class FileFormTest(TestCase):
    def test_valid_file_form_only_name(self):
        data = {'name': "test_name"}
        form = FileForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_file_form_all(self):
        data = {'name': "test_name", 'desc': "test_desc", 'text': "test_text"}
        form = FileForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_file_form_no_name(self):
        data = {'desc': "test_desc", 'text': "test_text"}
        form = FileForm(data=data)
        self.assertFalse(form.is_valid())
    
    def test_invalid_file_form_too_long_name(self):
        data = {'name': too_long_name}
        form = FileForm(data=data)
        self.assertFalse(form.is_valid())


class DirectoryFormTest(TestCase):
    def test_valid_directory_form_only_name(self):
        data = {'name': "test_name"}
        form = DirectoryForm(data=data)
        self.assertTrue(form.is_valid())

    def test_valid_directory_form_all(self):
        data = {'name': "test_name", 'desc': "test_desc"}
        form = DirectoryForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_invalid_directory_form_no_name(self):
        data = {'desc': "test_desc", 'text': "test_text"}
        form = DirectoryForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_directory_form_too_long_name(self):
        data = {'name': too_long_name}
        form = DirectoryForm(data=data)
        self.assertFalse(form.is_valid())

class EditorFormTest(TestCase):
    def test_editor_form_empty(self):
        data = {}
        form = EditorForm(data=data)
        self.assertTrue(form.is_valid())

    def test_editor_form_not_empty(self):
        data = {"text": "test_text"}
        form = EditorForm(data=data)
        self.assertTrue(form.is_valid())

class OptimizationFormTest(TestCase):
    def setUp(self):
        Optimization.objects.create(name="--allow-unsafe-read")
        Optimization.objects.create(name="--peep-return")

    def test_optimization_form_valid_one_choice(self):
        data = {"options": ["--allow-unsafe-read"]}
        form = OptimizationsForm(data=data)
        self.assertTrue(form.is_valid())

    def test_optimization_form_valid_multiple_choice(self):
        data = {"options": ["--allow-unsafe-read", "--peep-return"]}
        form = OptimizationsForm(data=data)
        self.assertTrue(form.is_valid())
    
    def test_optimization_form_valid_no_choice(self):
        data = {"options": []}
        form = OptimizationsForm(data=data)
        self.assertTrue(form.is_valid())

    def test_optimization_form_invalid_wrong_choice(self):
        data = {"options": ["--kaczka"]}
        form = OptimizationsForm(data=data)
        self.assertFalse(form.is_valid())

class DependantFormTest(TestCase):
    def setUp(self):
        proc1 = Processor.objects.create(name="proc1")
        DependantOption.objects.create(name="proc1_opt1", active="False", processor=proc1)
        DependantOption.objects.create(name="proc1_opt2", active="False", processor=proc1)

    def test_dependant_form_valid_one_choice(self):
        data = {"options": ["proc1_opt1"]}
        form = DependantForm(data=data)
        self.assertTrue(form.is_valid())

    def test_dependant_form_valid_multiple_choice(self):
        data = {"options": ["proc1_opt1","proc1_opt2"]}
        form = DependantForm(data=data)
        self.assertTrue(form.is_valid())

    def test_dependant_form_invalid_one_good_one_bad_choice(self):
        data = {"options": ["proc1_opt1","bad_opt"]}
        form = DependantForm(data=data)
        self.assertFalse(form.is_valid()) 
