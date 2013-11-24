from django.db import models

#Tabela Cidade

class Cidade(models.Model):
	descricao     = models.CharField(max_length=50)
	estado		  = models.CharField(max_length=10)

	def __unicode__(self):
		return self.descricao

	class Meta:
		ordering=['descricao']

class Bairro(models.Model):
	descricao 	   = models.CharField(max_length=50)
	cidade         = models.ForeignKey(Cidade,on_delete=models.PROTECT)

	def __unicode__(self):
		return self.descricao

	class Meta:
		ordering=['descricao']

# Tabela Cliente

class Cliente(models.Model):
	nome           = models.CharField(max_length=100)
	logradouro     = models.CharField(max_length=200)
	numero         = models.CharField(max_length=10)
	cidade         = models.ForeignKey(Cidade,on_delete=models.PROTECT)
	bairro 		   = models.ForeignKey(Bairro,on_delete=models.PROTECT) 
	email          = models.EmailField()
	RG             = models.CharField(max_length=15)
	CPF            = models.CharField(max_length=11)
	dataNascimento = models.DateField()
	comoConheceu   = models.CharField(max_length=30)
	eventoAnterior = models.BooleanField()

	def __unicode__(self):
		return self.nome

	class Meta:
		ordering=['nome']

# Tabela 
class ObjetosEvento(models.Model):
	descricao = models.CharField(max_length=30)

	def __unicode__(self):
		return self.descricao

	class Meta:
		ordering =['descricao']

# Tabela Contato
class Contato(models.Model):
	contato = models.CharField(max_length=15)
	cliente = models.ForeignKey(Cliente,on_delete=models.PROTECT)

	def __unicode__(self):
		return self.contato

	class Meta:
		ordering=['contato']

#tabela Tipo de evento
class TipoEvento(models.Model):
	descricao = models.CharField(max_length=40)

	def __unicode__(self):
		return self.descricao
	
	class Meta:
		ordering=['descricao']

# Tabela Cor
class Cor(models.Model):
	descricao = models.CharField(max_length=20)

	def __unicode__(self):
		return self.descricao

	class Meta:
		ordering = ['descricao']

# Tabela Evento
class Evento(models.Model):
	data          = models.DateField()
	tipoEvento    = models.ForeignKey(TipoEvento,on_delete=models.PROTECT)
	cliente       = models.ForeignKey(Cliente,on_delete=models.PROTECT)
	pagaraLimpeza = models.BooleanField()
	valorTotal    = models.FloatField(max_length=5)
	objetos       = models.ManyToManyField(ObjetosEvento)
	horaInicio    = models.TimeField()
	horaTermino   = models.TimeField()
	numCobertas   = models.SmallIntegerField(blank=True,null=True)
	corCoberta    = models.ForeignKey(Cor,on_delete=models.PROTECT)

	def __unicode__(self):
		return self.data

	class meta:
		ordering = ['data'] 



