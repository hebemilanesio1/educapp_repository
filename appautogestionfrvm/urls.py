from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.urls import include, path
from django.contrib.auth.views import LoginView
from .views import generar_pdf, confirmacion_inscripcion, listado_alumnos_por_curso, faq_query, chatbot_response, generar_cuota, generar_cuota_procesar
from .views import AdminDashboardView, emitir_certificado
from .views import pago_exitoso, descargar_comprobante_pago

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('institucional/', views.institucional, name='institucional'),
    path('cursos/', views.lista_cursos, name='cursos'),  # Ruta correcta para la vista de cursos
    path('cursos/crear/', views.crear, name='crear'),
    path('cursos/editar/<int:id>/', views.editar, name='editar'),
    path('eliminar/<int:id>/', views.eliminar, name='eliminar'),
    path('login/', LoginView.as_view(template_name='paginas/login.html'), name='login'),
    path('programas/', LoginView.as_view(template_name='paginas/programas.html'), name='programas'),
    path('complemento/', LoginView.as_view(template_name='paginas/complemento.html'), name='complemento'),
    path('cursosoficio/', LoginView.as_view(template_name='paginas/cursosoficio.html'), name='cursosoficio'),
    path('main/', LoginView.as_view(template_name='paginas/main.html'), name='main'),
    path('contacto/', views.contacto, name='contacto'),
    path('buscar/', views.buscar_alumno, name='buscar_alumno'),
    path('gestionar-alumno/<str:numero_documento>/', views.gestion_alumno, name='gestion_alumno'),
    path('generar-pdf/<int:numero_documento>/', generar_pdf, name='generar_pdf'),
    path('confirmacion-inscripcion/<str:numero_documento>/', confirmacion_inscripcion, name='confirmacion_inscripcion'),
    path('listado-alumnos/', listado_alumnos_por_curso, name='listado_alumnos_por_curso'),
    path('documentos/', LoginView.as_view(template_name='documentos/index.html'), name='documentos'),
    path('faq-query/', faq_query, name='faq-query'),
    path('chatbot/', chatbot_response, name='chatbot_response'),
    path('tomar-asistencia/', views.tomar_asistencia, name='tomar_asistencia'),
    path('pago_exitoso/', pago_exitoso, name='pago_exitoso'),
    path('descargar-comprobante/<str:numero_documento>/', descargar_comprobante_pago, name='descargar_comprobante_pago'),
    path('pago_fallido/', views.pago_fallido, name='pago_fallido'),
    path('pago_pendiente/', views.pago_pendiente, name='pago_pendiente'),
    path('administrar_alumno/', views.administrar_alumno , name='administrar_alumno'),
    path('generar_cuota/', generar_cuota, name='generar_cuota'),
    path('generar_cuota/procesar/', generar_cuota_procesar, name='generar_cuota_procesar'),
    path('checkout/', views.checkout, name='checkout'),
    path('obtener-conceptos/<int:curso_id>/', views.obtener_conceptos, name='obtener_conceptos'),
    path('admin-dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('emitir_certificado/', emitir_certificado, name='emitir_certificado'),
    path('consultar_asistencias/', views.consultar_asistencias, name='consultar_asistencias'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [path('_debug_/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)