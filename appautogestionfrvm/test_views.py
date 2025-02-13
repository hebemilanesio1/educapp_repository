import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Curso, Alumno

@pytest.mark.django_db
def test_inicio_view(client):
    response = client.get(reverse('inicio'))
    assert response.status_code == 200
    assert 'paginas/inicio.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_cursos_view(client):
    curso = Curso.objects.create(titulo="Curso de prueba")
    response = client.get(reverse('cursos'))
    assert response.status_code == 200
    assert 'cursos/index.html' in [t.name for t in response.templates]
    assert curso in response.context['cursos']

@pytest.mark.django_db
def test_crear_view_post(client):
    response = client.post(reverse('crear'), {'titulo': 'Nuevo Curso'})
    assert response.status_code == 302  # Redirige después de guardar
    assert Curso.objects.filter(titulo='Nuevo Curso').exists()

@pytest.mark.django_db
def test_editar_view_get(client):
    curso = Curso.objects.create(titulo="Curso a editar")
    response = client.get(reverse('editar', args=[curso.id]))
    assert response.status_code == 200
    assert 'cursos/editar.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_eliminar_view(client):
    curso = Curso.objects.create(titulo="Curso a eliminar")
    response = client.post(reverse('eliminar', args=[curso.id]))
    assert response.status_code == 302  # Redirige después de eliminar
    assert not Curso.objects.filter(id=curso.id).exists()

@pytest.mark.django_db
def test_crear_alumno_view_post(client):
    curso = Curso.objects.create(titulo="Curso para alumno")
    alumno_data = {
        'curso': curso.id,
        'apellido': 'García',
        'nombre': 'Luis',
        'tipo_documento': 'DNI',
        'numero_documento': '12345678',
        'direccion': 'Calle Falsa 123',
        'localidad': 'Springfield',
        'telefono_fijo': '5551234',
        'telefono_celular': '15551234',
        'email': 'luis.garcia@example.com'
    }
    response = client.post(reverse('crear_alumno'), alumno_data)
    assert response.status_code == 302  # Debe redirigir después de la creación
    assert Alumno.objects.filter(numero_documento='12345678').exists()

@pytest.mark.django_db
def test_editar_alumno_view_get(client):
    curso = Curso.objects.create(titulo="Curso para alumno")
    alumno = Alumno.objects.create(
        curso=curso,
        apellido="García",
        nombre="Luis",
        tipo_documento="DNI",
        numero_documento="12345678",
        direccion="Calle Falsa 123",
        localidad="Springfield",
        telefono_fijo="5551234",
        telefono_celular="15551234",
        email="luis.garcia@example.com"
    )
    response = client.get(reverse('editar_alumno', args=[alumno.id]))
    assert response.status_code == 200
    assert 'alumnos/editar.html' in [t.name for t in response.templates]

@pytest.mark.django_db
def test_eliminar_alumno_view(client):
    curso = Curso.objects.create(titulo="Curso para alumno")
    alumno = Alumno.objects.create(
        curso=curso,
        apellido="García",
        nombre="Luis",
        tipo_documento="DNI",
        numero_documento="12345678",
        direccion="Calle Falsa 123",
        localidad="Springfield",
        telefono_fijo="5551234",
        telefono_celular="15551234",
        email="luis.garcia@example.com"
    )
    response = client.post(reverse('eliminar_alumno', args=[alumno.id]))
    assert response.status_code == 302  # Redirige después de la eliminación
    assert not Alumno.objects.filter(id=alumno.id).exists()


@pytest.mark.django_db
def test_confirmacion_inscripcion_view(client):
    alumno = Alumno.objects.create(numero_documento="123456", nombre="Juan Pérez")
    response = client.get(reverse('confirmacion_inscripcion', args=[alumno.numero_documento]))
    assert response.status_code == 200
    assert 'alumnos/confirmacion_inscripcion.html' in [t.name for t in response.templates]
    assert 'Juan Pérez' in response.content.decode()