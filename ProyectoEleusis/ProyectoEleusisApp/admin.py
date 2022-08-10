from django.contrib import admin
from.models import *
# Register your models here.

class MateriaAdmin(admin.ModelAdmin):
    fields = ['posicion', 'description', 'fecha', 'anio']
    list_display = ('posicion', 'description', 'fecha', 'anio')


class EventoAdmin(admin.ModelAdmin):
    fields = ['nombre', 'tema', 'descripcion', 'disertantes', 'precio', 'precio_dolar', 'propaganda', 'imagen', 'lugar_inicio', 'fecha_inicio', 'hora_inicio']
    list_display = ('nombre', 'tema', 'descripcion', 'disertantes', 'precio', 'precio_dolar', 'propaganda', 'imagen', 'lugar_inicio', 'fecha_inicio', 'hora_inicio')

class LugarAdmin(admin.ModelAdmin):
    fields = ['nombre', 'fecha', 'hora', 'evento']
    list_display = ('nombre', 'fecha', 'hora', 'evento')

class InscripcionAdmin(admin.ModelAdmin):
    fields = ['nombre', 'email', 'comprobante', 'fk_evento']
    list_display = ('nombre', 'email', 'comprobante', 'fk_evento')




admin.site.register(Evento, EventoAdmin)
admin.site.register(Materia, MateriaAdmin)
admin.site.register(Lugar, LugarAdmin)
admin.site.register(Inscripcion, InscripcionAdmin)



