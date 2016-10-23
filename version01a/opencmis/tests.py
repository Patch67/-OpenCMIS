from django.test import TestCase
from django.test import Client
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType

from .models import Student, Title, Ethnicity, Status, BaselineEntry, BaselineValue, Qualification, StudentQualification
from .views import make_alert


class StudentTestAdd(TestCase):
    """
    Test to see if we can add a student via simulated form post
    """
    def setUp(self):
        self.c = Client()

    def test_create(self):
        response = self.c.post('/opencmis/student/add/', {
            'status': 14,
            'title': 1,
            'first_name': 'Jacob',
            'last_name': 'Green',
            'date_of_birth': '12/03/1996',
            'gender': 'U',
            'ethnicity': 31,
            }
        )
        # TODO: This test isn't good enough. It passes invalid data!
        self.assertEqual(response.status_code, 200)


class StudentTestRead(TestCase):
    """
    Test to see if we can create and then read the student
    """
    user = User

    def setUp(self):
        self.c = Client()

        # Create a user
        user = User.objects.create_user(username='user', password='pass')

        # Create a title to use in Student
        title = Title()
        title.title = 'Mr'
        title.save()

        ethnicity = Ethnicity()
        ethnicity.value = "White"
        ethnicity.save()

        status = Status()
        status.status = "Test Data"
        status.save()

        # Create a student
        student = Student()
        student.title = Title.objects.first()
        student.first_name = 'Jacob'
        student.last_name = 'Percival'
        student.date_of_birth = '1995-01-01'
        student.gender = 'M'
        student.ethnicity = Ethnicity.objects.first()
        student.status = Status.objects.first()
        student.save()

        be = BaselineEntry()
        be.heading = "Testing"
        be.blurb = "Write some proper tests so you can prove it works."
        be.save()

        bv = BaselineValue()
        bv.student = Student.objects.first()
        bv.baseline = BaselineEntry.objects.first()
        bv.week = 1
        bv.text = "Here is some text"
        bv.save()

        qual = Qualification()
        qual.title = "O Level Maths"
        qual.LAR = '1234567890'
        qual.save()

        sq = StudentQualification()
        sq.student = Student.objects.first()
        sq.qualification = Qualification.objects.first()
        sq.start = '2016-09-01'
        sq.expected_end = '2017-07-21'
        sq.save()

    def test_create(self):
        url = '/opencmis/student/'

        # User not logged in (guest)
        response = self.client.get(url)
        self.assertRedirects(response, '/login/?redirect_to=/opencmis/student/')

        # User logged in but without permission
        self.c.login(username='user', password='pass')
        # TODO: If logged in but without permission redirect to a you don't have permission for that page
        self.assertRedirects(response, '/login/?redirect_to=/opencmis/student/')

        # User logged in with permission
        content_type = ContentType.objects.get_for_model(Student)
        permissions = Permission.objects.filter(content_type=content_type)
        for perm in permissions:
            print(perm)
        permission = Permission.objects.get(content_type=content_type, codename='student_reader')
        self.user.user_permissions.add(permission)

        self.client.login(username='user', password='pass')
        response = self.client.get(url)
        self.assertContains(response, "What to look for")

        self.assertEqual(Student.objects.count(), 1)
        self.assertEqual(Title.objects.first().title, 'Mr')
        self.assertEqual(Ethnicity.objects.first().value, 'White')
        self.assertEqual(Status.objects.first().status, 'Test Data')
        self.assertEqual(Student.objects.first().first_name, 'Jacob')
        self.assertEqual(BaselineEntry.objects.first().heading, 'Testing')
        self.assertEqual(BaselineValue.objects.first().text, 'Here is some text')
        self.assertEqual(Qualification.objects.first().title, 'O Level Maths')
        self.assertEqual(StudentQualification.objects.first().student.first_name, 'Jacob')

        sid = Student.objects.first().id
        items = [
                 ['/opencmis/student/', 200],
                 ['/opencmis/student/{0}/'.format(sid), 200],
                 ['/opencmis/student/99/', 404],
                 ['/opencmis/student/{0}/baseline/'.format(sid), 200],
                 ['/opencmis/student/99/baseline/'.format(sid), 404],
                 ['/opencmis/student/{0}/qualification/'.format(sid), 200],
                 ['/opencmis/student/99/qualification/'.format(sid), 404],
                 ['/opencmis/student/{0}/qualification/add'.format(sid), 200],
                 ['/opencmis/student/99/qualification/add'.format(sid), 404],
            ]
        for item in items:
            # print('{0} {1}'.format(item[0], item[1]))
            response = self.client.get(item[0], follow=True)
            self.assertEqual(response.status_code, item[1], item[0])
        response = self.client.get('/opencmis/dashboard/', follow=True)
        self.assertEqual(response.status_code, 404, "Should not allow access as user not logged in")


class MakeAlertTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_create(self):
        self.assertEqual(make_alert(25, 50, 75, 0), 'danger')
        self.assertEqual(make_alert(25, 50, 75, 25), 'warning')
        self.assertEqual(make_alert(25, 50, 75, 50), 'info')
        self.assertEqual(make_alert(25, 50, 75, 75), 'success')

