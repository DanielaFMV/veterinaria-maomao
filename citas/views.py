from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from .models import Cita, Servicio
from .forms import CitaForm


def inicio(request):
    servicios = Servicio.objects.all()
    return render(request, 'citas/inicio.html', {'servicios': servicios})


def agendar(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save()

            # Armar el link de confirmación con el token único de la cita
            link = request.build_absolute_uri(f'/confirmar/{cita.token}/')

            # Enviar email de confirmación
            send_mail(
                subject='Confirma tu cita — Veterinaria Maomao',
                message=f"""
Hola {cita.nombre},

Recibimos tu solicitud de cita en Veterinaria Maomao.

Detalles:
- Servicio: {cita.servicio}
- Fecha: {cita.fecha}
- Hora: {cita.hora}

Para confirmar tu cita haz clic en el siguiente enlace:
{link}

Si no agendaste esta cita, ignora este mensaje.

Veterinaria Maomao
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[cita.email],
            )

            return redirect('citas:cita_pendiente')
    else:
        form = CitaForm()

    return render(request, 'citas/agendar.html', {'form': form})


def cita_pendiente(request):
    # Página que se muestra luego de agendar, pidiendo al cliente que revise su email
    return render(request, 'citas/pendiente.html')


def confirmar_cita(request, token):
    cita = get_object_or_404(Cita, token=token)

    if cita.estado == 'pendiente':
        cita.estado = 'confirmada'
        cita.save()

    return render(request, 'citas/confirmada.html', {'cita': cita})


def lista_citas(request):
    citas = Cita.objects.all()
    return render(request, 'citas/lista_citas.html', {'citas': citas})
