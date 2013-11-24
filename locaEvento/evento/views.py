 #!/usr/bin/python
 # -*- coding: utf-8 -*-
import os, sys

from django import http
from locaEvento.evento.models import *
from django.template.loader import get_template
#from locaEvento.evento.forms import *
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render_to_response
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

	if tabela == "Contato":
		clientes = Cliente.objects.all()
	elif tabela == "Cliente" :
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
													 'objetosEvento': objetos,
													 'cores': cores,
													 'bairros':bairros	
													  })

def pgSalvar(request):
	msg = ""
	if request.POST:
		tabela = definirTabela(request.path)
		#try:
		obj = montarObjetoSalvar(tabela,request.POST)
		obj.save()
		if request.POST.has_key('objetos'):
			objetos = ObjetosEvento.objects.filter(id__in=request.POST['objetos'])
			for objeto in objetos:	
				obj.objetos.add(objeto)
		msg = "Salvo"
		return render(request,'Cadastros/novoBase.html',{'nomeTela':tabela, 'msg':msg})
		#except:
		#return HttpResponse("Erro ao salvar arquivo ")	
	else:
		return render(request,'Cadastros/novoBase.html',{'nomeTela':tabela, 'msg':msg})

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
		"""
		if tabela == "Contato":
			clientes = Cliente.objects.all()
		elif tabela == "Cliente" or tabela == "Bairro" :
			cidades = Cidade.objects.all()
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
	return render(request,'Cadastros/detalhesBase.html',{'nomeTela':tabela, 'listItem':resultSet})

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
	elif nomeTabela == 'Contato':
		obj = Contato.objects.all()
	elif nomeTabela == 'ObjetosEvento':
		obj = ObjetosEvento.objects.all()
	elif nomeTabela == 'Cidade':
		obj = Cidade.objects.all()
	elif nomeTabela == 'Bairro':
		obj = Bairro.objects.all()

	return obj

def pesquisar(request,valor):
	tabela = definirTabela(request.path)
	bairros = ""
	if tabela == 'Cliente':
		cidades = Cidade.objects.all()
		bairros = Bairro.objects.filter(cidade__id=valor)

	return render(request,'Cadastros/novoBase.html',{'nomeTela':tabela,
													 'bairros':bairros,
													 'cidades':cidades,	
													  })
	"""
	elif nomeTabela == 'Evento':
		obj = Evento.objects.all()
	elif nomeTabela == 'Contato':
		obj = Contato.objects.all()
	elif nomeTabela == 'ObjetosEvento':
		obj = ObjetosEvento.objects.all()
	elif nomeTabela == 'Cidade':
		obj = Cidade.objects.all()
	"""
	
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
	elif nomeTabela == 'Contato':
		obj = Contato.objects.get(id=pk)
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
		cidade         = Cidade.objects.get(id=post['cidade']) 
		email          = post['email']
		RG             = post['RG']
		CPF            = post['CPF']

		dataNascimento = post['dataNascimento']
		comoConheceu   = post['comoConheceu']
		if 	post.has_key('eventoAnterior'):
			eventoAnterior = post['eventoAnterior']
		else:
			eventoAnterior = False
		
		obj = Cliente(nome=nome,logradouro=logradouro,numero=numero,cidade=cidade,email=email,RG=RG,CPF=CPF,dataNascimento=dataNascimento,comoConheceu=comoConheceu,eventoAnterior=eventoAnterior)
	elif nomeTabela == 'Cor':
		descricao      = post['descricao']
		obj            = Cor(descricao=descricao)
	elif nomeTabela == 'Evento':
		data           = post['data_year']+"-"+post['data_month']+"-"+post['data_day']
		tipoEvento     = TipoEvento.objects.get(id=post['tipoEvento'])
		cliente        = Cliente.objects.get(id=post['cliente']) 
		
		if 	post.has_key('pagaraLimpeza'):
			pagaraLimpeza  = post['pagaraLimpeza']
		else:
			pagaraLimpeza = False			

		valorTotal     = post['valorTotal']
		horaInicio     = post['horaInicio']
		horaTermino    = post['horaTermino']
		numCobertas    = post['numCobertas']
		corCoberta     = Cor.objects.get(id=post['corCoberta'])	
		obj            = Evento(data=data,tipoEvento=tipoEvento,cliente=cliente,pagaraLimpeza=pagaraLimpeza,valorTotal=valorTotal,horaInicio=horaInicio,horaTermino=horaTermino,numCobertas=numCobertas,corCoberta=corCoberta)
	elif nomeTabela == 'Contato':
		contato        = post['contato'] 
		cliente        = Cliente.objects.get(id=post['cliente'])
		obj            = Contato(contato=contato,cliente=cliente)
	elif nomeTabela == 'ObjetosEvento':
		descricao      = post['descricao']
		obj            = ObjetosEvento(descricao=descricao)
	elif nomeTabela == 'Cidade':
		descricao      = post['descricao']
		uf             = post['UF']
		obj            = Cidade(descricao=descricao,estado=uf)
	elif nomeTabela == 'Bairro':
		descricao      = post['descricao']
		cidade         = Cidade.objects.get(id=post['bairroCidade'])
		obj            = Bairro(descricao=descricao,cidade=cidade)

	return obj
	
def definirTabela(path):
	tela = path
	tela = tela.split('/')
	tela = tela[2]
	return tela 
