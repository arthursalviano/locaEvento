 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import os, sys

from django import http
from locaEvento.evento.models import *
from django.db.models import Q
from django.template.loader import get_template
from django.template import RequestContext, Context
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import render
from django.shortcuts import render_to_response
from datetime import time
#from reportlab.pdfgen import canvas
#from xhtml2pdf import pisa
#from report import write_to_pdf
import HTMLParser

########################################
########### FUNÇÕES DE PÁGINA ##########
########################################
"""
def contrato(request):
	locadora = {'nome':'Eliane Viana Bezerra de Lima', 
				'rg': '002327919',
				'cpf':'068.245.484-21',
				'endereco': 'Rua Getúlio Vargas nº 271 Bairro Nordeste, Natal-RN'
				}
	local    = {'nome' : "FOFÃO RECEPÇÕES",
				'endereco' : 'Rua Getúlio Vargas nº 271 Bairro Nordeste, Natal-RN'
				}
	return render(request,'Documentos/contrato.html',{'locadora': locadora,'local':local})

def pdfHtmlPisa2(request):
	return write_to_pdf('Documentos/contrato.html',{},'teste.pdf')

def pdfHtmlPisa(request):
	
	pisa.showLogging()

	sourceHtml ="<html><body><p>To pdf or not to PDF</p></body></html>" 
	outputFileName = "test.pdf"

	resultFile = open(outputFileName,"w+b")

	pisaStatus = pisa.CreatePDF(
			sourceHtml,
			dest=resultFile
		)

	resultFile.close()

	return pisaStatus


def pdfReportLab(request):
	response = HttpResponse(content_type='application/pdf')
	response['Content-DIsposition'] = 'attachment; filename="somefilename.pdf"'

	p = canvas.Canvas(response)

	p.drawString(100,100,"Hello world.")

	p.showPage()
	p.save()
	return response
"""

def pgInicial(request):
	return render_to_response('home.html',{})

def pgCadastros(request):
	return render(request,'Cadastros/cadastrosBase.html',({'nomeTela' : 'Cadastros' }))

def pgCrud(request):
	tabela = definirTabela(request.path)
	return render(request,"Cadastros/crudBase.html",({'nomeTela' : tabela}))

def pgNovo(request):
	tabela = definirTabela(request.path)
	clientes = ""
	cidades  = ""
	tiposEvento = ""
	objetos = ""
	cores = ""
	bairros = ""

	if tabela == "Cliente" :
		cidades = Cidade.objects.all()
		bairros = Bairro.objects.all()
	elif tabela == "Bairro":
		cidades = Cidade.objects.all()
	elif tabela == "Evento":
		tiposEvento = TipoEvento.objects.all()
		clientes = Cliente.objects.all()
		objetos = ObjetosEvento.objects.all()
		cores     = Cor.objects.all()

	return render(request,'Cadastros/novoBase.html',{'nomeTela':tabela,
													 'clientes' : clientes,
													 'cidades':cidades,
													 'tiposEvento':tiposEvento,
													 'objetos': objetos,
													 'cores': cores,
													 'bairros':bairros,
													 'msg':'novo'	
													  })

def pgSalvar(request):
	msg = ""
	if request.POST:
		tabela = definirTabela(request.path)
		#try:
		url = 'Cadastros/novoBase.html'
		obj = montarObjetoSalvar(tabela,request.POST)
		obj.save()
		if request.POST.has_key('objetos'):
			objetos = ObjetosEvento.objects.filter(id__in=request.POST['objetos'])
			for objeto in objetos:	
				obj.objetos.add(objeto)
		msg = "Salvo"
		#except:
		#return HttpResponse("Erro ao salvar arquivo ")	
		return render(request,url,{'nomeTela':tabela, 'msg':msg})

def atualizar(request,pk):
	if request.POST:
		tabela = definirTabela(request.path)
		obj = montarObjetoSalvar(tabela,request.POST)
		obj.id = pk
		obj.save()
		resultSet  = recuperarItens(tabela) 
		return render(request,'Cadastros/detalhesBase.html',{'nomeTela':tabela, 'listItem':resultSet,'editar':'editar'})
	else:
		return HttpResponse("Objeto Vazio")

def deletar(request,id):
	if request:
		tabela = definirTabela(request.path)
		obj = recuperarItemPorID(tabela,id)
		if obj:
			resultSet  = recuperarItens(tabela)
			try:
				obj.delete()
				
				return render(request,'Cadastros/detalhesBase.html',{'nomeTela':tabela, 'listItem':resultSet,'deletar':'deletar'})
			except models.ProtectedError:
				return render(request,'Cadastros/detalhesBase.html',{'nomeTela':tabela, 'listItem':resultSet,'msgErro':"Este item não pode ser excluído porque outros Itens fazerem referência a este."})

		else:
			return HttpResponse("Objeto vazio")

def pgEditar(request,id):
	if request:
		tabela = definirTabela(request.path)
		obj = recuperarItemPorID(tabela,id)
		cidades  = ''
		if tabela == "Bairro":
			cidades  = Cidade.objects.all()
		elif tabela == "Cliente" :
			cidades  = Cidade.objects.all()
		"""
		elif tabela == "Evento":
			tiposEvento = TipoEvento.objects.all()
			clientes = Cliente.objects.all()
			objetos = ObjetosEvento.objects.all()
			cores     = Cor.objects.all()

			return render(request,'Cadastros/EditarBase.html',{'nomeTela':tabela,
													 'clientes' : clientes,
													 'cidades':cidades,
													 'tiposEvento':tiposEvento,
													 'objetosEvento': objetos,
													 'cores': cores,
													 'obj':obj,
													 'editar':'editar'	
													  })
			#
		"""
		if obj:
			return render(request,'Cadastros/editarBase.html',{'nomeTela':tabela, 
															   'obj':obj,
															   'cidades':cidades,
															   'editar':'editar'})
		else:
			return HttpResponse("Objeto Vazio")

def pgDetalhes(request):
	tabela     = definirTabela(request.path)
	resultSet  = recuperarItens(tabela)

	return render(request,'Cadastros/detalhesBase.html',{'nomeTela':tabela, 
														 'listItem':resultSet})

##############################################
########### FUNÇÕES AUXILIARES ###############
##############################################

def recuperarItens(nomeTabela):
	if  nomeTabela == 'TipoEvento':
		obj = TipoEvento.objects.all()
	elif nomeTabela == 'Cliente':
		obj = Cliente.objects.all()
	elif nomeTabela == 'Cor':
		obj = Cor.objects.all()
	elif nomeTabela == 'Evento':
		obj = Evento.objects.all()
	elif nomeTabela == 'ObjetosEvento':
		obj = ObjetosEvento.objects.all()
	elif nomeTabela == 'Cidade':
		obj = Cidade.objects.all()
	elif nomeTabela == 'Bairro':
		obj = Bairro.objects.all()
	elif nomeTabela == 'Evento':
		obj = Bairro.objects.all()

	return obj

def mudarCidade(request,valor):
	bairros = Bairro.objects.filter(cidade__id=valor)
	retorno = serializers.serialize("json",bairros)
	return HttpResponse(retorno,mimetype="text/javascript")
	
def filtrar(request,chave,valor):
	tabela = definirTabela(request.path)
	resultSet = ""
	
	if tabela == 'Cidade':
		if chave == 'descricao':
			resultSet = Cidade.objects.filter(descricao__contains=valor)
		elif chave == 'uf':
			resultSet = Cidade.objects.filter(estado__contains=valor)
		elif chave == 'todos':
			resultSet = Cidade.objects.all()
	elif tabela == 'TipoEvento':
		if chave == 'descricao':
			resultSet  = TipoEvento.objects.filter(descricao__contains=valor)
		elif chave == 'todos':
			resultSet = TipoEvento.objects.all()
	if tabela == 'Bairro':
		if chave == "descricao":	
			resultSet = Bairro.objects.filter(descricao__contains=valor)
		elif chave == "cidade":
			resultSet = Bairro.objects.filter(cidade__descricao__contains=valor)
		elif chave == 'todos':
			resultSet = Bairro.objects.all()
	if tabela == 'ObjetosEvento':
		if chave == 'descricao':
			resultSet  = ObjetosEvento.objects.filter(descricao__contains=valor)
		elif chave == 'todos':
			resultSet = ObjetosEvento.objects.all()
	if tabela == 'Cor':
		if chave == 'descricao':
			resultSet  = Cor.objects.filter(descricao__contains=valor)
		elif chave == 'todos':
			resultSet = Cor.objects.all()
	if tabela == 'Cliente':
		if chave == 'nome':
			resultSet  = Cliente.objects.filter(nome__contains=valor)
		elif chave == 'contatos':
			resultSet  = Cliente.objects.filter( Q(contato01__contains=valor)|Q(contato02__contains=valor)| Q(contato03__contains=valor))
		elif chave == 'CPF':
			resultSet  = Cliente.objects.filter(CPF__contains=valor)
		elif chave == 'todos':
			resultSet = Cliente.objects.all()
		

	return render(request,'Cadastros/detalhesBase.html',{'nomeTela':tabela, 'listItem':resultSet, 'acao': 'filtrar'}) 

def recuperarItemPorID(nomeTabela,pk):
	if  nomeTabela == 'TipoEvento':
		obj = TipoEvento.objects.get(id=pk)
	elif nomeTabela == 'Cliente':
		obj = Cliente.objects.get(id=pk)
	elif nomeTabela == 'Cor':
		obj = Cor.objects.get(id=pk)
	elif nomeTabela == 'Evento':
		obj = Evento.objects.get(id=pk)
	elif nomeTabela == 'ObjetosEvento':
		obj = ObjetosEvento.objects.get(id=pk)
	elif nomeTabela == 'Cidade':
		obj = Cidade.objects.get(id=pk)
	elif nomeTabela == 'Bairro':
		obj = Bairro.objects.get(id=pk)	

	return obj 

def montarObjetoSalvar(nomeTabela,post):
	if  nomeTabela == 'TipoEvento':
		descricao      = post['descricao']
		obj            = TipoEvento(descricao=descricao)
	
	elif nomeTabela == 'Cliente':
		nome           = post['nome']
		logradouro     = post['logradouro']
		numero         = post['numero']
		cidade         = Cidade.objects.get(id=post['clienteCidade'])
		bairro         = Bairro.objects.get(id=post['clienteBairro'])
		
		temp           = post['contato01']
		contato01      = temp[1:3]+ temp[4:8] + temp[9:13]
		temp           = post['contato02']
		contato02      = temp[1:3]+ temp[4:8] + temp[9:13]
		temp           = post['contato03']
		contato03      = temp[1:3]+ temp[4:8] + temp[9:13] 
		
		email          = post['email']
		RG             = post['RG']
		temp 		   = post['CPF']
		CPF           = temp[0:3]+ temp[4:7] + temp[8:11] + temp[12:14]
		
		dataNascimento = post['dataNascimento']
		comoConheceu   = post['comoConheceu']
		eventoAnterior = post['eventoAnterior']

		
		obj = Cliente(nome=nome,
					  contato01=contato01,
					  contato02=contato02,
					  contato03=contato03,
					  logradouro=logradouro,
					  numero=numero,
					  cidade=cidade,
					  bairro=bairro,
					  email=email,
					  RG=RG,CPF=CPF,
					  dataNascimento=dataNascimento,
					  comoConheceu=comoConheceu,
					  eventoAnterior=eventoAnterior)
	
	elif nomeTabela == 'Cor':
		descricao      = post['descricao']
		obj            = Cor(descricao=descricao)
	
	elif nomeTabela == 'Evento':
		data           = post['data']
		tipoEvento     = TipoEvento.objects.get(id=post['TipoEvento'])
		cliente        = Cliente.objects.get(id=post['Cliente']) 
		if 	post.has_key('pagaraLimpeza'):
			pagaraLimpeza  = post['pagaraLimpeza']
		
		temp = post['valorTotal']

		valorTotal     = temp[0:1] + temp[2:5] + "." + temp[6:8]
		valorTotal = float(valorTotal)
		
		horaInicio = post['horaInicio']
		horaTermino = post['horaTermino']
		duracao        = subtrairHora(horaInicio,horaTermino)
		if 	post['numCobertas']:
			numCobertas    = int(post['numCobertas'])
		else:
			numCobertas = 0

		if 	post.has_key('corCoberta'):
			corCoberta    = Cor(descricao=post['corCoberta'])

		
		if post.has_key('corCoberta'):
			obj            = Evento(data=data,
								tipoEvento=tipoEvento,
								cliente=cliente,
								pagaraLimpeza=pagaraLimpeza,
								valorTotal=valorTotal,
								horaInicio=horaInicio,
								horaTermino=horaTermino,
								duracao=duracao,
								numCobertas=numCobertas,
								corCoberta=corCoberta)
		else:
			obj            = Evento(data=data,
								tipoEvento=tipoEvento,
								cliente=cliente,
								pagaraLimpeza=pagaraLimpeza,
								valorTotal=valorTotal,
								horaInicio=horaInicio,
								horaTermino=horaTermino,
								duracao=duracao,
								numCobertas=numCobertas)
		
	elif nomeTabela == 'ObjetosEvento':
		descricao      = post['descricao']
		obj            = ObjetosEvento(descricao=descricao)
	elif nomeTabela == 'Cidade':
		descricao      = post['descricao']
		uf             = post['UF']
		obj            = Cidade(descricao=descricao,
								estado=uf)
	elif nomeTabela == 'Bairro':
		descricao      = post['descricao']
		cidade         = Cidade.objects.get(id=post['bairroCidade'])
		obj            = Bairro(descricao=descricao,
						        cidade=cidade)

	return obj
	
def definirTabela(path):
	tela = path
	tela = tela.split('/')
	tela = tela[2]
	return tela 

def subtrairHora(horaInicio, horaTermino):
	
	horaIni    = int(horaInicio[0:2])
	minuteIni  = int(horaInicio[3:5])
	segundosIni = (horaIni*60) + minuteIni

	horaTerm   = int(horaTermino[0:2])
	minuteTerm = int(horaTermino[3:5])
	segundosTerm = (horaTerm*60) + minuteTerm

	segundosDuracao = segundosTerm - segundosIni
	
	horaDuracao = segundosDuracao/60
	if horaDuracao > 9:
		horaDuracao = "0"+ str(horaDuracao)
	else:
		horaDuracao = str(horaDuracao)

	minutoDuracao = str(segundosDuracao%60)
	if minutoDuracao < 9:
		minutoDuracao = "0"+ str(minutoDuracao)
	else:
		minutoDuracao = str(minutoDuracao)

	duracao = horaDuracao + ":"+minutoDuracao

	return duracao

 


