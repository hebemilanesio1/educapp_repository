from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Curso, Alumno, Institucional, Concepto
from django.contrib.auth.models import User

class LoginViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_login_page_access(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/login.html')

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('main'))

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200) 
        

class ViewsTestCase(TestCase):

    def setUp(self):
        self.curso = Curso.objects.create(
            nombre="Curso de prueba",
            tipo="Tipo de prueba",
            fecha_inicio="2024-01-01",
            periodo="Primer semestre",
            nombre_docente="Docente de prueba",
            precio_cuota=100.00,
            precio_total=1000.00,
            dia_hora_cursado="Lunes y Miércoles a las 10:00"
        )

        self.concepto = Concepto.objects.create(
            curso=self.curso,
            codigo="COD123",
            descripcion="Concepto de prueba",
            orden=1,
            plan="Plan de prueba",
            fechavto="2024-12-31",
            estado=True,
            monto=1000.00
        )


    def test_inicio_view(self):
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/inicio.html')

    def test_editar_view_get(self):
        response = self.client.get(reverse('editar', args=[self.curso.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cursos/editar.html')

    def test_crear_alumno_view_post(self):
        alumno_data = {
            'curso': self.curso.id,
            'concepto': self.concepto.id,
            'apellido': 'Nuevo Apellido',
            'nombre': 'Nuevo Nombre',
            'tipo_documento': 'DNI',
            'numero_documento': '87654321',
            'direccion': 'Nueva Dirección',
            'localidad': 'Nueva Localidad',
            'telefono_fijo': '123456780',
            'telefono_celular': '987654320',
            'email': 'nuevoalumno@prueba.com'
        }
        response = self.client.post(reverse('gestion_alumno', args=[alumno_data['numero_documento']]), alumno_data)
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(Alumno.objects.filter(numero_documento='87654321').exists())


class CursoDeleteViewTestCase(TestCase):

    def setUp(self):
        self.curso = Curso.objects.create(
            nombre="Curso a eliminar",
            tipo="Tipo de prueba",
            fecha_inicio="2024-01-01",
            periodo="Primer semestre",
            nombre_docente="Docente de prueba",
            precio_cuota=100.00,
            precio_total=1000.00,
            dia_hora_cursado="Lunes y Miércoles a las 10:00",
        )

    def test_eliminar_view(self):
        response = self.client.post(reverse('eliminar', args=[self.curso.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/cursos/')
        self.assertFalse(Curso.objects.filter(id=self.curso.id).exists())

class InstitucionalViewTestCase(TestCase):

    def test_institucional_view_get(self):
        response = self.client.get(reverse('institucional'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/institucional.html')
        self.assertContains(response, "Políticas de Extensión")

class CursosDeOficioViewTestCase(TestCase):

    def test_cursosdeoficio_view_get(self):
        response = self.client.get(reverse('cursosoficio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/cursosoficio.html')
        self.assertContains(response, "Listado de cursos")

class ComplementoViewTestCase(TestCase):

    def test_cursosdeoficio_view_get(self):
        response = self.client.get(reverse('complemento'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/complemento.html')
        self.assertContains(response, "Complemento y Asistencia")

class PracticasViewTestCase(TestCase):

    def test_cursosdeoficio_view_get(self):
        response = self.client.get(reverse('practicas'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/practicas.html')
        self.assertContains(response, "Descargar PDF de Carreras")

class ContactoViewTestCase(TestCase):

    def test_cursosdeoficio_view_get(self):
        response = self.client.get(reverse('contacto'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'paginas/contacto.html')
        self.assertContains(response, "Datos de contacto")