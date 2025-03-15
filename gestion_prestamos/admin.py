from django.contrib import admin
from .models import  cliente,prestamo,HistorialAbono,ruta
from django.contrib.admin.models import LogEntry
import io
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models import Sum
from xhtml2pdf import pisa

# Register your models here.
class Cliente(admin.ModelAdmin):
    list_display=('id', 'nombre', 'direccion', 'celular', 'ruta','fecha_actualizacion')
    list_filter = ('nombre', 'fecha_creacion')
    search_fields = ('id', 'nombre','cedula', 'direccion', 'celular', 'ruta')
admin.site.register(cliente, Cliente)

class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('action_flag', 'user')
    search_fields = ('object_repr', 'change_message')
admin.site.register(LogEntry, LogEntryAdmin)

class Prestamo(admin.ModelAdmin):
    list_display=('id', 'cliente', 'intereses', 'valorcredito', 'saldopendiente', 'cuotaactual', 'fecha_actualizacion')
    list_filter = ('cliente', 'fecha_creacion')
    search_fields = ('id', 'cliente')
admin.site.register(prestamo, Prestamo)

class historialAbono(admin.ModelAdmin):
    list_display=('prestamo', 'monto', 'saldo_pendiente', 'fecha_actualizacion')
    list_filter = ('prestamo', 'fecha_abono')
    search_fields = ('prestamo', 'fecha_abono')
admin.site.register(HistorialAbono, historialAbono)



def exportar_reporte_pdf(modeladmin, request, queryset):
    """
    Acción personalizada para exportar un reporte en PDF de los registros seleccionados.
    """
    # Opcional: si quieres usar todos los registros filtrados, puedes obtener el queryset
    # queryset = modeladmin.get_queryset(request)

    # Calcular el total de montos
    total = queryset.aggregate(total=Sum('monto'))['total'] or 0

    # Construir el contexto para la plantilla
    context = {
        'objects': queryset,
        'total': total,
    }

    # Renderizar la plantilla HTML con el contexto
    html = render_to_string('admin/ruta_report.html', context)

    # Crear un buffer para el PDF
    result = io.BytesIO()
    # Convertir el HTML a PDF usando pisa
    pdf = pisa.CreatePDF(io.StringIO(html), dest=result)
    if pdf.err:
        return HttpResponse('Ocurrió un error al generar el PDF: <pre>' + html + '</pre>')
    
    # Devolver la respuesta PDF
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_gastos_ruta.pdf"'
    return response

exportar_reporte_pdf.short_description = "Exportar reporte a PDF"

class RutaAdmin(admin.ModelAdmin):
    list_display = ('id', 'monto', 'concepto', 'fecha_actualizacion')
    list_filter = ('cliente', 'fecha_creacion')
    search_fields = ('cliente__nombre', 'fecha_creacion')
    actions = [exportar_reporte_pdf]  # Registrar la acción personalizada

admin.site.register(ruta, RutaAdmin)
