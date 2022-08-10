from django.urls import path

from .views import *


urlpatterns = [
    # URLS de ProyectoEleusisApp
path('', inicio, name='inicio'),
path('cursos/<int:numero>', cursos, name='cursos'),
path('formacion/', formacion, name='formacion'),
path('escuela/', escuela, name='escuela'),
path('contacto/', contacto, name='contacto'),
path('contacto_email/', contacto_email, name='contacto_email'),

# URLS de ProyectoEleusisApp para eventos
path('crear_evento/', crear_evento, name='crear_evento'),
path('eliminar_evento/<evento_id>/', eliminar_evento, name='eliminar_evento'),
path('editar_evento/<evento_id>/', editar_evento, name='editar_evento'),
path('detalle_evento/<evento_id>/', detalle_evento, name='detalle_evento'),
path('cambiar_estado/<evento_id>/', cambiar_estado, name='cambiar_estado'),

# URLS de ProyectoEleusisApp para agregar lugares
path('editar_lugar/<lugar_id>/', editar_lugar, name='editar_lugar'),
path('crear_lugar/<evento_id>', crear_lugar, name='crear_lugar'),
path('eliminar_lugar/<lugar_id>/', eliminar_lugar, name='eliminar_lugar'),

# URLS de ProyectoEleusisApp para integrantes
path('eleminar_integrante/<integrante_id>/', eliminar_integrante, name='eleminar_integrante'),
path('editar_integrante/<integrante_id>/', editar_integrante, name='editar_integrante'),

# URLS de ProyectoEleusisApp para materias
path('eliminar_materia/<materia_id>/', eliminar_materia, name='eliminar_materia'),
path('editar_materia/<materia_id>/', editar_materia, name='editar_materia'),

# URLS de ProyectoEleusisApp para inscriptos
path('eliminar_inscripto/<inscripto_id>/', eliminar_inscripto, name='eliminar_inscripto'),
path('cambiar_aprobado/<inscripto_id>/', cambiar_aprobado, name='cambiar_aprobado'),
path('cambiar_desaprobado/<inscripto_id>/', cambiar_desaprobado, name='cambiar_desaprobado'),

# URLS de ProyectoEleusisApp para login
path('login/', login_request, name='login'),
path('logout/', logout_request, name='logout_request'),

# URLS de ProyectoEleusisApp para panel de control
path('panel_admin/<str:tab>/', panel_admin, name='panel_admin'),




# URLS de ProyectoEleusisApp para test
path('test/', test, name='test'),
path('test2/', ip, name='test2'),
]