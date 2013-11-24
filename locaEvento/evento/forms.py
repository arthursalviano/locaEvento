#!/usr/bin/python
 # -*- coding: utf-8 -*-
import os, sys

from django import forms
from locaEvento.evento.models import *
from django.forms.widgets import *
from django.forms.extras.widgets import *
from django.contrib.auth.models import User
from bootstrap_toolkit.widgets import BootstrapDateInput,  BootstrapTextInput,BootstrapUneditableInput


NASCIMENTO_ANO_OPCOES = []
EVENTO_ANO_OPCOES = []
ESTADOS = (("AC","ACRE"),
		   ("AL","ALAGOAS"),
		   ("AP","AMAPÁ"),
		   ("AM","AMAZONAS"),
		   ("BA","BAHIA"),
		   ("CE","CEARÁ"),
		   ("DF","DISTRITO FEDERAL"),
		   ("ES","ESPIRÍTO SANTO"),
		   ("GO","GOIÁS"),
		   ("MA","MARANHÃO"),
		   ("MT","MATO GROSSO"),
		   ("MS","MATO GROSSO DO SUL"),
		   ("MG","MINAS GERAIS"),
		   ("PA","PARÁ"),
		   ("PB","PARAÍBA"),
		   ("PR","PARANÁ"),
		   ("PE","PERNAMBUCO"),
		   ("PI","PIAUÍ"),
		   ("RJ","RIO DE JANEIRO"),
		   ("RN","RIO GRANDE DO NORTE"),
		   ("RS","RIO GRANDE DO SUL"),
		   ("RO","RONDÔNIA"),
		   ("RR","RORAIMA"),
		   ("SC","SANTA CATARINA"),
		   ("SP","SÃO PAULO"),
		   ("SE","SERGIPE"),
		   ("TO","TOCANTINS")
		)

for i in range(2013,1900,-1):
	NASCIMENTO_ANO_OPCOES.append(i)

for i in range(2000,2030,1):
	EVENTO_ANO_OPCOES.append(i)


class TipoEventoForm(forms.Form):
	descricao = forms.CharField(max_length=50,label="Descrição")

class ClienteForm(forms.Form):
	nome           = forms.CharField(max_length=100,label="Nome",widget=BootstrapTextInput())
	logradouro     = forms.CharField(max_length=200,label="logradouro")
	numero         = forms.CharField(max_length=10,label="Número")
	cidade 		   = forms.ModelChoiceField(queryset=Cidade.objects.all(),label="Cidade")
	email          = forms.EmailField(required=False)
	RG             = forms.CharField(label="RG")
	CPF            = forms.CharField(label="CPF")
	dataNascimento = forms.DateField(label="Data de Nascimento",required=False, widget=BootstrapDateInput())
	comoConheceu   = forms.CharField(max_length=30,label="Como Conheceu?",required=False)
	eventoAnterior = forms.BooleanField(label="Participou de evento anterior")

class ContatoForm(forms.Form):
	contato = forms.CharField(max_length=15,label="Contato")
	cliente = forms.ModelChoiceField(queryset = Cliente.objects.all(),label="Cliente")

class CorForm(forms.Form):
	descricao = forms.CharField(max_length=20,label="Descrição")

class EventoForm(forms.Form):
	data          = forms.DateField(label="Data do Evento",widget=SelectDateWidget(years=EVENTO_ANO_OPCOES))
	tipoEvento    = forms.ModelChoiceField(queryset = TipoEvento.objects.all(),label="Tipo de evento")
	cliente       = forms.ModelChoiceField(queryset = Cliente.objects.all(),label="Cliente")
	pagaraLimpeza = forms.BooleanField(label="Pagará a limpeza?")
	valorTotal    = forms.FloatField(max_value=9999,label="Valor total")
	objetos       = forms.ModelMultipleChoiceField(queryset = ObjetosEvento.objects.all(),label="Objetos",widget=SelectMultiple())
	horaInicio    = forms.TimeField(label="Horário de início")
	horaTermino   = forms.TimeField(label="Horário de término")
	numCobertas   = forms.IntegerField(label="Número de cobertas")
	corCoberta    = forms.ModelChoiceField(queryset=Cor.objects.all(),label="Cor da coberta")

class ObjetosEventoForm(forms.Form):
	descricao = forms.CharField(max_length=30,label="Descrição")

class CidadeForm(forms.Form):
	descricao = forms.CharField(max_length=30,label="Descrição")
	UF    	  = forms.ChoiceField(choices=ESTADOS,label="UF")
	