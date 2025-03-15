from django.db import models
from gestion_prestamos.choices import formapago
# Create your models here.
class cliente(models.Model):
    id = models.AutoField(primary_key=True)  # ID autoincremental
    nombre = models.CharField(max_length=100, verbose_name="Nombre completo")  # Puede ser nulo
    cedula = models.BigIntegerField(null=True, blank=True)  # Clave primaria en base de datos
    direccion = models.CharField(max_length=100, null=True, blank=True, verbose_name="Direccion")
    celular = models.BigIntegerField(null=True, blank=True, verbose_name="Celular")
    ruta = models.CharField(max_length=40, null=True, blank=True, verbose_name="Nombre de la ruta")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre if self.nombre else str(self.cedula)
    

class prestamo(models.Model):
    id = models.AutoField(primary_key=True)  
    cliente = models.ForeignKey(cliente, null=True, blank=True, on_delete=models.CASCADE)
    valorprestado = models.BigIntegerField(verbose_name="Valor prestado")  
    intereses = models.IntegerField()  
    valorcredito = models.BigIntegerField(verbose_name="Valor del crédito", editable=False) 
    formapago = models.CharField(max_length=50, verbose_name='Forma de pago', choices=formapago)
    cuotaactual = models.IntegerField(verbose_name="Cuota actual")  
    abono = models.IntegerField(null=True, blank=True, default=0)  
    saldopendiente = models.BigIntegerField(verbose_name="Saldo pendiente") 
    cuotaspactadas = models.IntegerField(verbose_name="Cuotas pactadas")   
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para:
        1. Calcular el valor del crédito según los intereses.
        2. Restar el abono al saldo pendiente.
        3. Aumentar la cuota actual.
        4. Registrar el abono en el historial automáticamente.
        """
        # Calcular el valor del crédito con intereses
        self.valorcredito = int(self.valorprestado * (1 + (self.intereses / 100)))

        # Si hay un abono, actualizar la cuota actual, el saldo pendiente y registrar en historial
        if self.abono and self.abono > 0:
            self.saldopendiente = max(0, self.saldopendiente - self.abono)  # Evita saldo negativo
            self.cuotaactual += 1

            # Registrar el abono en el historial con saldo pendiente
            HistorialAbono.objects.create(prestamo=self, monto=self.abono, saldo_pendiente=self.saldopendiente)

        super().save(*args, **kwargs)

    def registrar_abono(self, monto):
        """
        Método para registrar un abono manualmente.
        """
        if monto > 0:
            self.saldopendiente = max(0, self.saldopendiente - monto)  # Evita saldo negativo
            self.cuotaactual += 1

            # Registrar el abono en el historial con saldo pendiente actualizado
            HistorialAbono.objects.create(prestamo=self, monto=monto, saldo_pendiente=self.saldopendiente)
            self.save()

    def __str__(self):
        return f"Préstamo {self.id} - Cliente {self.cliente}"
    

class HistorialAbono(models.Model):
    prestamo = models.ForeignKey(prestamo, on_delete=models.CASCADE, related_name="abonos")
    monto = models.IntegerField(verbose_name="Monto del abono")
    saldo_pendiente = models.BigIntegerField(verbose_name="Saldo pendiente")  # Nuevo campo
    fecha_abono = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Abono de {self.monto} en préstamo {self.prestamo.id} - Saldo pendiente: {self.saldo_pendiente}"


class ruta(models.Model):
    id = models.AutoField(primary_key=True)  
    cliente = models.ForeignKey(cliente, null=True, blank=True, on_delete=models.CASCADE, related_name="clientes")
    monto = models.BigIntegerField(verbose_name="Monto del abono")
    concepto = models.CharField(max_length=100, verbose_name="Concepto del gasto")   
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
