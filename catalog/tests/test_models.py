from django.test import TestCase
from catalog.models import Autor

# Create your tests here.

class YourTestClass(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        print("setUpTestData: Run once to set up non-modified data for all class methods.")
        pass

    def setUp(self):
        print("setUp: Run once for every test method to setup clean data.")
        pass

    def test_false_is_false(self):
        print("Method: test_false_is_false.")
        self.assertFalse(False)

    def test_false_is_true(self):
        print("Method: test_false_is_true.")
        self.assertTrue(False)

    def test_one_plus_one_equals_two(self):
        print("Method: test_one_plus_one_equals_two.")
        self.assertEqual(1 + 1, 2)

class AuthorModelTest(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        #Set up non-modified objects used by all test methods
        Autor.objects.create(nombre='Big', apellido='Bob')

    def test_nombre_label(self):
        autor=Autor.objects.get(id=1)
        field_label = autor._meta.get_field('nombre').verbose_name
        self.assertEquals(field_label,'nombre')

    def test_fecha_muerte_label(self):
        autor=Autor.objects.get(id=1)
        field_label = autor._meta.get_field('fecha_muerte').verbose_name
        self.assertEquals(field_label,'died')

    def test_nombre_max_length(self):
        autor=Autor.objects.get(id=1)
        max_length = autor._meta.get_field('nombre').max_length
        self.assertEquals(max_length,100)

    def test_object_name_is_last_name_comma_first_name(self):
        autor=Autor.objects.get(id=1)
        expected_object_name = '%s, %s' % (autor.apellido, autor.nombre)
        self.assertEquals(expected_object_name,str(autor))

    def test_get_absolute_url(self):
        autor=Autor.objects.get(id=1)
        #This will also fail if the urlconf is not defined.
        self.assertEquals(autor.get_absolute_url(),'/catalog/autor/1')   