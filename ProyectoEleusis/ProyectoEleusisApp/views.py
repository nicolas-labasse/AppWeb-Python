from collections import Counter
import datetime
from genericpath import exists
import io
from itertools import count
from operator import countOf
import os
from re import template
from unittest import result
from django.conf import settings
from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
import requests
from ProyectoEleusisApp.forms import *
from ProyectoEleusisApp.models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import FileResponse
from reportlab.pdfgen import canvas


# Create your views here.

def inicio(request):
    url = " /media/imagenes/f13.png"
    url_fondo  = " /media/imagenes/70.png"
    curso = Evento.objects.all().order_by('-id')[:3]
    data = Lugar.objects.filter().values('evento','fecha','hora','nombre')
    tab = "inicio"
    return render (request, 'ProyectoEleusisApp/index.html', {'url': url, 'url_fondo': url_fondo, 'curso': curso, 'data': data, 'tab': tab})

def cursos(request,numero):
    tab = "cursos"
    promocion = Evento.objects.get(propaganda=True)
    curso = Evento.objects.all().order_by('-id')
    data = Lugar.objects.filter().values('evento','fecha','hora','nombre')
    paginas = len(curso)/6
    paginas = int(paginas)
    if numero == 1:
        numero = numero + 1
        curso = curso[:6]
    elif numero > paginas:
        numero = numero
    else:
        curso = curso[:6*numero]
        numero = numero + 1
 
    return render (request, 'ProyectoEleusisApp/cursos.html', {'promocion': promocion, 'data': data, 'tab': tab, 'curso': curso, 'numero': numero,'paginas': paginas})

def formacion(request):
    materias = Materia.objects.all().order_by('posicion')
    tab = "formacion"
    if len(materias) > 4:
        materias3 = materias[8:12]
        materias2 = materias[4:8]
        materias1 = materias[:4]

          
    return render (request, 'ProyectoEleusisApp/formacion.html', {'materias1': materias1, 'materias2': materias2, 'materias3': materias3, 'tab': tab})


def escuela(request):
    tab = "escuela"
    url = " /media/imagenes/f14.png"
    url_escuela = " /media/imagenes/30.jpeg"
    return render (request, 'ProyectoEleusisApp/escuela.html', {'url': url, 'tab': tab, 'url_escuela': url_escuela})

def contacto(request):
    tab = "#contacto"
    return redirect('/'+tab)

def detalle_evento(request,evento_id):
    if request.method == "POST":
        form = InscripcionForm(request.POST, request.FILES)
        if form.is_valid():
         info_form = form.cleaned_data 
         inscripto = Inscripcion.objects.create(
            nombre = info_form['nombre'],
            email = info_form['email'],
            comprobante = info_form['comprobante'],
            fk_evento = Evento.objects.get(id=evento_id),
         )
         inscripto.save()
         messages.success(request, 'Gracias por inscribirte')
         return redirect('/')
    else:
        curso = Evento.objects.get(id=evento_id)
        espacio = Lugar.objects.filter(evento = curso).values()
        url = " /media/imagenes/paypal.png"
        form = InscripcionForm()
        anular = Evento.objects.filter(id=evento_id,fecha_inicio__gte=datetime.datetime.now())
        if len(anular) < 0:
         return render (request, 'ProyectoEleusisApp/detalle_evento.html', {'curso': curso, 'espacio': espacio, 'url': url, 'form': form})
        else:
            return render (request, 'ProyectoEleusisApp/detalle_evento.html', {'curso': curso, 'espacio': espacio, 'url': url, 'form': form, 'anular': anular})
   
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("inicio")
            else:
               return redirect("login")
        else:
            return redirect("login")

    form = AuthenticationForm()

    return render(request, 'ProyectoEleusisApp/login.html', {'form': form})

def logout_request(request):
    logout(request)
    return redirect("inicio")

@staff_member_required
def panel_admin(request,tab):
    if request.method == "POST":
            if 'enviar' in request.POST:
             form = MateriaForm(request.POST)
             if form.is_valid():
                 info_form = form.cleaned_data
                 mat = Materia(description = info_form['description'],posicion = info_form['posicion'],fecha = info_form['fecha'])
                 mat.save()
                 messages.add_message(request, messages.SUCCESS, 'La materia ha sido creado correctamente')
                 return redirect('/panel_admin/materias')
             else:
                messages.add_message(request, messages.ERROR, 'La materia no ha sido creado correctamente')
                return redirect('/panel_admin/materias')
            else:
                buscar = request.POST["buscar"]
                if buscar == "":
                    return redirect('/panel_admin/'+tab)
                else:
                    buscador = Materia.objects.filter(Q(description__icontains=buscar) | Q(posicion__icontains=buscar)).values()
                    return render(request, 'ProyectoEleusisApp/panel_admin.html', {'buscador': buscador, 'tab': tab})         
    else:
        if tab == "materias":
         mat = Materia.objects.all()
         form = MateriaForm()
         page = request.GET.get('page', 1)
         paginator = Paginator(mat, 6)
         mat = paginator.page(page)
         return render (request, 'ProyectoEleusisApp/panel_admin.html', {'mat': mat, 'tab': tab, 'paginator': paginator, 'form': form})
        elif tab == "inscriptos":
            buscar = request.GET.get('buscar')
            page = request.GET.get('page', 1)
            if buscar is not None and buscar is not "":
                buscador = Inscripcion.objects.filter(Q(nombre__icontains=buscar)  | Q(email__icontains=buscar) | Q(fk_evento__id__icontains=buscar) | Q(fecha_inscripcion__icontains=buscar) ).order_by('-id')
                paginator = Paginator(buscador, 6)
                buscador = paginator.page(page)
                return render(request, 'ProyectoEleusisApp/panel_admin.html', {'buscador': buscador, 'tab': tab, 'paginator': paginator, 'buscar': buscar})
            else:
                inscriptos = Inscripcion.objects.all().order_by('-id')
                paginator = Paginator(inscriptos, 6)
                inscriptos = paginator.page(page)
                return render (request, 'ProyectoEleusisApp/panel_admin.html', {'inscriptos': inscriptos, 'tab': tab, 'paginator': paginator})
                
        else:
            form = EventoForm()
            page = request.GET.get('page', 1)
            buscar = request.GET.get('buscar')
            if buscar is not None and buscar is not "":   
                buscador = Evento.objects.filter(Q(nombre__icontains=buscar) | Q(tema__icontains=buscar) | Q(descripcion__icontains=buscar) | Q(disertantes__icontains=buscar)  | Q(fecha_inicio__icontains=buscar) | Q(lugar_inicio__icontains=buscar))
                paginator = Paginator(buscador, 6)
                buscador = paginator.page(page)
                return render (request, 'ProyectoEleusisApp/panel_admin.html', { 'tab': tab, 'form': form,'buscador': buscador, 'paginator': paginator,'buscar': buscar})
            else:
                espacio = Lugar.objects.all()
                curso = Evento.objects.all().order_by('-id')
                paginator = Paginator(curso, 6)
                curso = paginator.page(page)
                return render(request, 'ProyectoEleusisApp/panel_admin.html', {'curso': curso, 'form': form, 'tab': tab, 'paginator': paginator,'espacio': espacio})
    
def contacto_email(request):
  if request.method == "POST":
    name = request.POST.get('name')
    email = request.POST.get('email')
    subject = request.POST.get('subject')
    message = request.POST.get('message')

    template = render_to_string('ProyectoEleusisApp/contacto_email.html', {
        'name': name,
        'email': email,
        'message': message
    })
    email = EmailMessage(
        subject,
        template,
        settings.EMAIL_HOST_USER,
        ['nicolaslabasse4@gmail.com']
    )
    email.fail_silently = False
    email.send()
    messages.success(request, 'Mensaje enviado correctamente.')
    return redirect('/index')

@staff_member_required
def eliminar_integrante(request, integrante_id):
    persona = Integrantes.objects.get(id=integrante_id)
    persona.delete()
    messages.add_message(request, messages.SUCCESS, 'El integrante ha sido eliminado correctamente')
    return redirect('/panel_admin/integrantes')

@staff_member_required
def editar_integrante(request, integrante_id):
    persona = Integrantes.objects.get(id=integrante_id)
    if request.method == 'POST':
        form_edit = IntegrantesForm(request.POST, request.FILES)
        if form_edit.is_valid():
            info_form = form_edit.cleaned_data
            
            persona.nombre = info_form['nombre']
            persona.cargo = info_form['cargo']
            persona.imagen = info_form['imagen']
            persona.save()
            messages.add_message(request, messages.SUCCESS, 'El integrante ha sido editado correctamente')
            return redirect('/panel_admin/integrantes')
        else:
            messages.add_message(request, messages.ERROR, 'El integrante no ha sido editado correctamente')
            return redirect('/panel_admin/integrantes')
    else:
        form_edit = IntegrantesForm(initial={"nombre": persona.nombre, "cargo": persona.cargo, "imagen": persona.imagen})
        return render(request, 'ProyectoEleusisApp/editar_integrante.html', {'form_edit': form_edit})


@staff_member_required
def eliminar_materia(request, materia_id):
    mat = Materia.objects.get(id=materia_id)
    mat.delete()
    messages.add_message(request, messages.SUCCESS, 'La materia ha sido eliminada correctamente')
    return redirect('/panel_admin/materias')


@staff_member_required
def editar_materia(request, materia_id):
    mat = Materia.objects.get(id=materia_id)
    if request.method == 'POST':
        form_edit = MateriaForm(request.POST)
        if form_edit.is_valid():
            info_form = form_edit.cleaned_data
            
            mat.description = info_form['description']
            mat.posicion = info_form['posicion']
            mat.fecha = info_form['fecha']
            mat.anio = info_form['anio']
            mat.save()
            messages.add_message(request, messages.SUCCESS, 'La materia ha sido editado correctamente')
            return redirect('/panel_admin/materias')
        else:
            messages.add_message(request, messages.ERROR, 'La materia no ha sido editado correctamente')
            return redirect('/panel_admin/materias')
    else:
        form_edit = MateriaForm(initial={"description": mat.description, "posicion": mat.posicion, "fecha": mat.fecha, "anio": mat.anio})
        return render(request, 'ProyectoEleusisApp/editar_materia.html', {'form_edit': form_edit})


@staff_member_required
def crear_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if form.is_valid():
            info_form = form.cleaned_data     
            evento = Evento.objects.create(
                nombre = info_form['nombre'],
                tema = info_form['tema'],
                descripcion = info_form['descripcion'],
                disertantes = info_form['disertantes'],
                precio = info_form['precio'],
                precio_dolar = info_form['precio_dolar'],
                imagen = info_form['imagen'],
                fecha_inicio = info_form['fecha_inicio'],
                hora_inicio = info_form['hora_inicio'],
                lugar_inicio = info_form['lugar_inicio'],
            )
            evento.save()
            messages.add_message(request, messages.SUCCESS, 'El evento ha sido creado correctamente')
            return redirect('/panel_admin/eventos')
        else:
            messages.add_message(request, messages.ERROR, 'El evento no ha sido creado correctamente')
            return redirect('/crear_evento')
    else:
        form = EventoForm()
        form_lugar = LugarForm()
    return render(request, 'ProyectoEleusisApp/crear_evento.html', {'form': form, 'form_lugar': form_lugar})

@staff_member_required
def eliminar_evento(request, evento_id):
    evento = Evento.objects.get(id=evento_id)
    evento.delete()
    messages.add_message(request, messages.SUCCESS, 'El evento ha sido eliminado correctamente')
    return redirect('/panel_admin/eventos')

@staff_member_required
def editar_evento(request, evento_id):
    eve = Evento.objects.get(id=evento_id)
    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES)
        if 'crear' in request.POST:
            if form.is_valid():
                info_form = form.cleaned_data 
                eve.nombre = info_form['nombre']
                eve.tema = info_form['tema']
                eve.descripcion = info_form['descripcion']
                eve.disertantes = info_form['disertantes']
                eve.precio = info_form['precio']
                eve.precio_dolar = info_form['precio_dolar']
                eve.imagen = info_form['imagen']
                eve.fecha_inicio = info_form['fecha_inicio']
                eve.hora_inicio = info_form['hora_inicio']
                eve.lugar_inicio = info_form['lugar_inicio']
                eve.save()
                messages.add_message(request, messages.SUCCESS, 'El evento ha sido editado correctamente')
                return redirect('/panel_admin/eventos')
            else:
                messages.add_message(request, messages.ERROR, 'El evento no ha sido editado correctamente')
                return redirect('/panel_admin/eventos')
       
    else:   
        form = EventoForm(initial={"nombre": eve.nombre, "tema": eve.tema, "descripcion": eve.descripcion, "disertantes": eve.disertantes, "precio": eve.precio, "imagen": eve.imagen, "fecha_inicio": eve.fecha_inicio, "hora_inicio": eve.hora_inicio, "lugar_inicio": eve.lugar_inicio})
        return render(request, 'ProyectoEleusisApp/editar_evento.html', {'form': form})

@staff_member_required
def editar_lugar(request, lugar_id):
    eve = Lugar.objects.get(id=lugar_id)
    if request.method == 'POST':
        form = LugarForm(request.POST)
        if form.is_valid():
            eve.nombre = form.cleaned_data['nombre']
            eve.fecha = form.cleaned_data['fecha']
            eve.hora = form.cleaned_data['hora']
            eve.save()
            messages.add_message(request, messages.SUCCESS, 'El lugar ha sido editado correctamente')
            return redirect('/panel_admin/eventos')
    else:
        form = LugarForm(initial={"nombre": eve.nombre, "fecha": eve.fecha, "hora": eve.hora})
        return render(request, 'ProyectoEleusisApp/editar_lugar.html', {'form': form})

@staff_member_required
def crear_lugar(request, evento_id):
    eventos = Evento.objects.get(id=evento_id)
    if request.method == 'POST':
        form = LugarForm(request.POST)
        if form.is_valid():
         info_form = form.cleaned_data
         lugar = Lugar.objects.create(
                nombre = info_form['nombre'],
                fecha = info_form['fecha'],
                hora = info_form['hora'],
                evento = eventos,
            )
         lugar.save()
         messages.add_message(request, messages.SUCCESS, 'El lugar ha sido creado correctamente')
         return redirect('/panel_admin/eventos')
    else:
        form = LugarForm()
        return render(request, 'ProyectoEleusisApp/crear_lugar.html', {'form': form})


@staff_member_required
def eliminar_lugar(request, lugar_id):
    lugar = Lugar.objects.get(id=lugar_id)
    lugar.delete()
    messages.add_message(request, messages.SUCCESS, 'El lugar ha sido eliminado correctamente')
    return redirect('/panel_admin/eventos')


@staff_member_required
def cambiar_estado(request,evento_id):
    eve = Evento.objects.all()
    for e in eve:
        e.propaganda = False
        e.save()
    eve = Evento.objects.get(id=evento_id)
    eve.propaganda = True
    eve.save()
    return redirect('/panel_admin/eventos')


@staff_member_required
def eliminar_inscripto(request,inscripto_id):
    inscripto = Inscripcion.objects.get(id=inscripto_id)
    inscripto.delete()
    messages.add_message(request, messages.SUCCESS, 'El lugar ha sido eliminado correctamente')
    return redirect('/panel_admin/inscriptos')
 
@staff_member_required
def cambiar_aprobado(request,inscripto_id):
    inscripto = Inscripcion.objects.get(id=inscripto_id)
    inscripto.aprobado = True
    inscripto.save()
    return redirect('/panel_admin/inscriptos')


@staff_member_required
def cambiar_desaprobado(request,inscripto_id):
    inscripto = Inscripcion.objects.get(id=inscripto_id)
    inscripto.aprobado = False
    inscripto.save()
    return redirect('/panel_admin/inscriptos')


def test(request):
    curso = Evento.objects.get(id=10)
    return render(request, 'ProyectoEleusisApp/test.html', {'curso': curso})


def ip(request):
    curso = Evento.objects.all()
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return render(request, 'ProyectoEleusisApp/test2.html', {'curso': curso, 'ip': ip})
        

              
   
         