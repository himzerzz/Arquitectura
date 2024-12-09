from django.db import models

# Create your models here.
class Persona(models.Model):
    rut = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    correo = models.EmailField()
    telefono = models.IntegerField()

    def __str__(self):
        return self.nombre + ' ' + self.apellido

class Torre(models.Model):
    letra = models.CharField(max_length=1, primary_key=True, unique=True)

    def __str__(self):
        return self.letra
    
class Departamento(models.Model):
    torre = models.ForeignKey(Torre, on_delete=models.PROTECT)
    numero = models.IntegerField()

    def __str__(self):
        return self.torre + ' ' + self.numero
    
class Residente(models.Model):
    persona = models.ForeignKey(Persona,on_delete=models.CASCADE)
    departamento = models.ForeignKey(Departamento,on_delete=models.PROTECT)
    fechainicio = models.DateTimeField()
    fechatermino = models.DateTimeField(null=True)
    TIPOS = [
        ('P', 'Propietario'),
        ('A', 'Arrendatario')
    ]
    tiporesidente = models.CharField(choices=TIPOS,max_length=1, default='A')

    def __str__(self):
        return self.departamento.torre.letra + ' ' + self.departamento.numero + ' ' + self.persona.rut
    
class Pago(models.Model):
    residente = models.ForeignKey(Residente, on_delete=models.PROTECT)
    monto = models.IntegerField()
    fechapago = models.DateTimeField(null=True)
    fechaTermino = models.DateField()
    TIPOSPAGO = [
        ('D', 'Debito'),
        ('C', 'Credito'),
        ('E', 'Efectivo')
    ]
    tipopago = models.CharField(choices=TIPOSPAGO, max_length=1, default='D')

    def __str__(self):
        return self.residente.persona.rut + ' ' + self.fechapago
    
class Deuda(models.Model):
    pago = models.ForeignKey(Pago, on_delete=models.PROTECT)
    monto = models.IntegerField()
    fechadeuda = models.DateTimeField() #fecha de la creacion de la deuda
    fechavencimiento = models.DateTimeField() #fecha de cuando la deuda se vence

    montodeuda = models.IntegerField()

    def __str__(self):
        return self.pago.residente.persona.rut + ' ' + self.fechadeuda
    

    
