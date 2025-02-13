from typing import Any
from django.db import models


class Curso(models.Model):
    nombre = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    periodo = models.CharField(max_length=100)
    nombre_docente = models.CharField(max_length=255)
    precio_cuota = models.DecimalField(max_digits=10, decimal_places=2)
    precio_total = models.DecimalField(max_digits=10, decimal_places=2)
    dia_hora_cursado = models.CharField(max_length=255)

    def __str__(self):
        return self.nombre
    
    class Meta:
        db_table = 'appautogestionfrvm_curso'

class Concepto(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=50)
    descripcion = models.TextField()
    orden = models.IntegerField()
    plan = models.CharField(max_length=50)
    fechavto = models.DateField()
    estado = models.BooleanField(default=False)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Concepto {self.codigo} - {self.descripcion} ({self.curso.nombre})"
    class Meta:
        db_table = 'appautogestionfrvm_concepto'

class Institucional(models.Model):
    titulo = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='pdfs/')

    def __str__(self):
        return self.titulo
    


class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

class Alumno(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ('CDI', 'CDI'),
        ('DNI', 'DNI'),
        ('Pasaporte', 'Pasaporte'),
    ]
    
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    concepto = models.ForeignKey('Concepto', on_delete=models.CASCADE, null=True)
    apellido = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOCUMENTO_CHOICES)
    numero_documento = models.CharField(max_length=20)
    direccion = models.CharField(max_length=255)
    localidad = models.CharField(max_length=100)
    telefono_fijo = models.CharField(max_length=20, blank=True, null=True)
    telefono_celular = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"


class Inscripcion(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateTimeField(auto_now_add=True)


class Asistencia(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    fecha = models.DateField()
    presente = models.BooleanField(default=False)

    def _str_(self):
        return f'{self.alumno.nombre} - {self.curso.nombre} - {self.fecha}'
    

from django.db import models
from django.utils import timezone

class Pago(models.Model):
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('rechazado', 'Rechazado'),
    ]
    
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE)
    concepto = models.ForeignKey(Concepto, on_delete=models.CASCADE)
    fecha_pago = models.DateField(default=timezone.now)  # Asegúrate de que esto esté en tu modelo
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    id_transaccion = models.CharField(max_length=100, unique=True)  # ID de la transacción de Mercado Pago
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente')

    def __str__(self):
        return f"{self.alumno.nombre} - {self.concepto.descripcion} - {self.get_estado_pago_display()}"

