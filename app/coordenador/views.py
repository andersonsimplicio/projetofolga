from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from .models import *
from .forms import *
from django.views import View
from django.views.generic import ListView
from app.home.views import home
from datetime import datetime
from .Classes.Funcionario import FuncionarioEscala

import io
import tempfile
from weasyprint import HTML
from django.template.loader import render_to_string
from reportlab.pdfgen import canvas
from django.http import FileResponse
from django.template.loader import get_template



timeDate = datetime.now()
month = timeDate.month
ano = timeDate.year
# Create your views here.
def getDiasMes(mes):
    days_of_Month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    dias = days_of_Month[mes-1]
    return dias

def obterTurnodeFolgaDomingo(domingos=[],equipe="TARM"):
    turno_folgas = {}
    for d in domingos:
        f = Folga.objects.filter(data=d.strftime("%Y-%m-%d")).filter(equipe=equipe)
        p = PlantaoExtra.objects.filter(data=d.strftime("%Y-%m-%d")).filter(equipe=equipe)
        count_f = f.count()
        count_p = p.count()
        if count_f > 0:
            turno_folgas[f.values()[0]['plantao_id']]=d.strftime("%Y-%m-%d")
        else:
            if count_p > 0:
                turno_folgas[p.values()[0]['plantao_id']]=d.strftime("%Y-%m-%d")
            else:
                turno_folgas['Folguistas - E'] = d.strftime("%Y-%m-%d")
    return turno_folgas

def getFolgaE(mes=datetime,equipe="TARM"):

    dias_mes = getDiasMes(mes)

    folga = []
    folgas = Folga.objects.filter(data__month__exact=mes,equipe=equipe)
    PlaExtra = PlantaoExtra.objects.filter(data__month__exact=mes,equipe=equipe)


    dias = []
    for f in folgas:
        if int(f.data.strftime("%d")) < 10:
            d = int(f.data.strftime("%d").replace("0",""))
        else:
            d = int(f.data.strftime("%d"))
        if d not in dias:
            dias.append(datetime.strptime(f.data.strftime(str(ano)+"-"+str(mes)+"-"+str(d)) ,"%Y-%m-%d"))
        for i in range(1,dias_mes):
            folga.append(datetime.strptime(f.data.strftime(str(ano)+"-"+str(mes)+"-"+str(i)) ,"%Y-%m-%d"))

    for f in PlaExtra:
        if int(f.data.strftime("%d")) < 10:
            d = int(f.data.strftime("%d").replace("0", ""))
        else:
            d = int(f.data.strftime("%d"))
        if d not in dias:
            dias.append(datetime.strptime(f.data.strftime(str(ano)+"-"+str(mes)+"-"+str(d)) ,"%Y-%m-%d"))

    dias_folgas_E = list(set(folga) - set(dias))
    dias_folgas_E.sort()
    return (dias_folgas_E)

@login_required(login_url='login')
def homecoord(request):

    coordenador = Coordenador.objects.get(username=request.user.username)
    if coordenador.is_authenticated:
        mes = request.POST.get('selected_month')
        year = request.POST.get('selected_year')
        global ano
        if mes is None and year is None:
            mes = month
            year = ano
        else:
            mes = int(request.POST.get('selected_month'))
            ano = int(request.POST.get('selected_year'))
        dayNamesMin = ['S', 'T', 'Q', 'Q', 'S', 'S', 'D']
        meses = ["Janeiro","Fevereiro","Março","Abril","Maio","Junho","Julho","Agosto","Setembro","Outubro","Novembro","Dezembro"]
        semana = []
        domingos = []
        dias_mes = getDiasMes(mes)#recebe a quantidade de dias do mes
        for i in range(1,dias_mes+1):
            dt = datetime(year=ano, month=mes, day=i)
            if (dayNamesMin[dt.weekday()]) == 'D':
                domingos.append(datetime.strptime(dt.strftime("%Y-" + str(mes) + "-" + str(i)), "%Y-%m-%d"))
            semana.append(dayNamesMin[dt.weekday()])

        folga_domingos = obterTurnodeFolgaDomingo(domingos,coordenador.equipe)
        funcionarios = Funcionario.objects.all()\
            .filter(equipe=coordenador.equipe)\
            .exclude(Q(extra="Folguista")|Q(extra="Feirista"))\
            .order_by('turno')
        escala_f = []
        for fun in funcionarios:
            f = FuncionarioEscala((fun.nome +" "+fun.sobrenome),fun.turno)
            for i in range(1,dias_mes+1):
                f.add_escala((fun.turno).split(" - ")[0])
            escala_f.append(f)
        func = Folga.objects.all().filter(equipe=coordenador.equipe).filter(data__year__exact=year)
        extra = PlantaoExtra.objects.all().filter(equipe=coordenador.equipe).filter(data__year__exact=year)
        plantonistas = Funcionario.objects.all().filter(equipe=coordenador.equipe)


        for esc_fun in escala_f:
            for i in func:
                plantao = i.plantao
                folga = ((i.data).strftime("%d"))
                mesEscala = int(((i.data).strftime("%m")))
                x = 0
                folga = (int(folga)-1)
                while x < (dias_mes):
                    x+=1
                    if mesEscala == mes:
                        if (plantao.turno == esc_fun.turno):
                            esc_fun.add_folga(folga)

                        for i in extra:
                            plantaExtra = i.plantao
                            diaExtra = ((i.data).strftime("%d"))
                            mesExtra = int(((i.data).strftime("%m")))
                            diaExtra =(int(diaExtra)-1)
                            if mesExtra == mes:
                                 if plantaExtra.turno  == esc_fun.turno:
                                     esc_fun.add_extra(diaExtra)
        return render(request,"coordenador/inicial.html",{"ano":ano,"mes":meses[mes-1],"funcionarios":funcionarios,'range': range(1,dias_mes+1),'semana':semana,'escala':escala_f,"plantonistas":plantonistas,"domingos":folga_domingos})
    else:
        return redirect('logout_view')

class CadCoordView(View):
    form_class = CoordenadorForm
    model = Coordenador
    template_name = 'home/index.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            coordenador = Coordenador()
            coordenador.username = form.cleaned_data['username']
            coordenador.email = form.cleaned_data['email']
            coordenador.equipe = form.cleaned_data['equipe']
            coordenador.set_password(form.cleaned_data['password1'])
            coordenador.set_password(form.cleaned_data['password2'])
            form.save()
            user = authenticate(username=coordenador.username, password=coordenador.password)
            return redirect(loginCoordenador)
        else:
            context = {"form": form, "form.errors": form.errors}
            messages.error(request, "Cadastro não Realizado")
            return render(request, self.template_name, context)

        context = {"form": form}
        return render(request, self.template_name, context)


def loginCoordenador(request):
    if request.POST:
        email = request.POST.get('email')
        password = request.POST.get('password')
        coordenador = None
        try:
            coordenador = Coordenador.objects.get(email=email)
            usuario = authenticate(request,username=coordenador.username,password=password)
            if coordenador.check_password(password):
                login(request,usuario)
                return redirect('homecood')
            else:
                msg = "Email ou Senha incorretos!"
                return render(request, "coordenador/login.html", {"msg": msg})
        except Exception as e:
            msg = "Email ou Senha incorretos!"
            return render(request, "coordenador/login.html", {"msg": msg})
    else:
        return render(request, "coordenador/login.html")


def logout_view(request):
    logout(request)
    return redirect('home')


# cadastro de funcionario
@login_required(login_url='login')
def cad_func(request):
    plantoes = Plantao.objects.all()
    coordenador = Coordenador.objects.get(username=request.user.username)
    context = {}
    template_name = 'coordenador/cad_func.html'
    func_campos = FuncionarioForm(request.POST)
    if request.method == 'POST' and coordenador.is_authenticated:
        if func_campos.is_valid():
            context['is_valid'] = True
            func_campos.save(commit=False)
            funcionario = Funcionario()
            funcionario.nome = func_campos.cleaned_data['nome']
            funcionario.sobrenome = func_campos.cleaned_data['sobrenome']
            funcionario.turno = func_campos.cleaned_data['turno']
            funcionario.extra = func_campos.cleaned_data['extra']
            funcionario.equipe = coordenador.equipe
            funcionario.save()
            plantao = Plantao.objects.get(turno=funcionario.turno)
            plantao.funcionario.add(funcionario)
            plantao.save()
            messages.success(request,"Funcionario Cadastrado!")
            context["plantao"]= plantoes
        else:
            context["plantao"]= plantoes
            context["form.errors"]= func_campos.errors
            messages.error(request, "Funcionário não Cadastrado"),
        
    else:
        if coordenador.is_authenticated:
            context["plantao"]= plantoes
            return render(request, template_name,context)
        else:
            return redirect('logout_view')
    return render(request, template_name,context)
#lista dos funcionarios cadastrados
@login_required(login_url='login')
def listar_func(request):
    plantao = Plantao.objects.all()
    coordenador = Coordenador.objects.get(username=request.user.username)
    funcionarios = Funcionario.objects.all().filter(equipe=coordenador.equipe).order_by('turno')

    if coordenador.is_authenticated:
        return render(request, "coordenador/lista_func.html",{"funcionarios":funcionarios,"plantao":plantao})
    else:
        return redirect('logout_view')

#apagar funcionario
@login_required(login_url='login')
def apagar_func(request, id):
    coordenador = Coordenador.objects.get(username=request.user.username)
    funcionarios = Funcionario.objects.filter(id=id,equipe=coordenador.equipe)
    
    funcionarios.delete()
    funcionarios = Funcionario.objects.all().filter(equipe=coordenador.equipe)
    
    if coordenador.is_authenticated:
        return render(request, "coordenador/lista_func.html",{"funcionarios":funcionarios})
    else:
        return redirect('logout_view')

#atualizar cadastro do funcionario // refazer utilizando classe 
@login_required(login_url='login')
def update_func(request, id):
    coordenador = Coordenador.objects.get(username=request.user.username)
    funcionarios = Funcionario.objects.get(id=id)
    plantao = Plantao.objects.all()
    if request.method == 'POST' and coordenador.is_authenticated:
        form = FuncionarioUpdate(request.POST, request.FILES)
        if form.is_valid():
            funcionarios = form.save(commit=False)
            funcionario = Funcionario.objects.get(id=id)
            old_turno = funcionario.turno

            funcionario.nome = form.cleaned_data['nome']
            funcionario.sobrenome = form.cleaned_data['sobrenome']
            funcionario.extra = form.cleaned_data['extra']
            funcionario.turno = form.cleaned_data['turno']

            funcionario.save()
            #Remove o anigo relacionamento
            old_plantao = Plantao.objects.get(turno=old_turno)
            old_plantao.funcionario.remove(funcionario)
            old_plantao.save()
            #Salvando o novo relacionamento
            plantao =Plantao.objects.get(turno=funcionario.turno)
            plantao.funcionario.add(funcionario)
            plantao.save()
            return redirect(listar_func)
        else:
            return render(request, "coordenador/update_func.html",{"funcionarios":funcionarios,"plantao":plantao})
    else:
        if coordenador.is_authenticated:
            return render(request,"coordenador/update_func.html",{"funcionarios":funcionarios,"plantao":plantao})
        else:
            return redirect('logout_view')

class PlantaoView(View):
    form_class = PlantaoForm
    model = Plantao
    template_name = 'coordenador/cad_plantao.html'
    def get(self, request):
        form = self.form_class()
        context = {"form":form}
        return render(request, self.template_name, context)

    #@login_required(login_url='login')
    def post(self, request):
        #coordenador = Coordenador.objects.get(username=request.user.username)
        form = self.form_class(request.POST)
        if form.is_valid():# and coordenador.is_authenticated:
            form.save()

        plantao = Plantao.objects.all()
        context = {"form":form,"plantao":plantao}
        return render(request, self.template_name, context)

class FolgaView(ListView):
    form_class = FolgaForm
    model = Folga
    template_name = 'coordenador/cad_folga.html'

    def get(self, request):
        if request.user.is_authenticated:
            coordenador = Coordenador.objects.get(username=request.user.username)
            form = self.form_class()
            plantao = Plantao.objects.all()
            context = {"form":form,"plantao":plantao,}
            return render(request, self.template_name, context)
        else:
            return redirect(homecoord)

    def post(self, request):
        coordenador = Coordenador.objects.get(username=request.user.username)
        form = self.form_class(request.POST)
        turno_padrao ="NDA"
        if form.is_valid():# and coordenador.is_authenticated:
            data = form.cleaned_data['data']
            turno = form.cleaned_data['plantao']
            turno_padrao = turno
            form.save(commit=False)
            primeiraFolga = Folga()
            plantao = Plantao.objects.get(turno=turno.turno)
            dayoff = int(data.strftime("%d").replace("0", ""))
            mes = int(data.strftime("%m").replace("0",""))
            daysTotal = getDiasMes(mes)
            primeiraFolga.plantao =plantao
            primeiraFolga.data = data
            primeiraFolga.equipe = coordenador.equipe
            primeiraFolga.save()

            while dayoff <= (daysTotal):
                   dayoff +=6
                   if dayoff >(daysTotal):
                       break
                   dataNova = datetime.strptime(data.strftime("%Y-%m-"+str(dayoff)) ,"%Y-%m-%d")
                   dataNova = dataNova.strftime("%Y-%m-%d")
                   newfolga = Folga()
                   newfolga.plantao = plantao
                   newfolga.data = dataNova
                   newfolga.equipe = coordenador.equipe
                   newfolga.save()
        else:
            plantao = Plantao.objects.all()
            context = {"form": form, "form.errors": form.errors,'plantao':plantao}
            messages.error(request, "Cadastro não Realizado")
            return render(request, self.template_name, context)
        form = self.form_class()
        plantao = Plantao.objects.all()

        context = {"form":form,"plantao":plantao,"turno":turno_padrao,}
        return render(request, self.template_name, context)

class PlantaoExtraView(View):
    
    form_class = PlantaoExtraForm
    model = PlantaoExtra
    template_name = 'coordenador/cad_plantao_extra.html'


    def get(self, request):
        if request.user.is_authenticated:
            coordenador = Coordenador.objects.get(username=request.user.username)
            form = self.form_class()
            plantao = Plantao.objects.all()
            context = {"form":form,"plantao":plantao,"user":coordenador}
            return render(request, self.template_name, context)
        else:
            return redirect(homecoord)


    def post(self, request):
        form = self.form_class(request.POST)
        coordenador = Coordenador.objects.get(username=request.user.username)
        plantao = Plantao.objects.all()
        if form.is_valid():# and coordenador.is_authenticated
            form.save(commit=False)
            try:
                plantaoEx = self.model()
                plantaoEx.equipe = coordenador.equipe
                plantaoEx.data = form.cleaned_data['data']
                plantaoEx.plantao = form.cleaned_data['plantao']
                folga = Folga.objects.filter(data=plantaoEx.data,equipe=coordenador.equipe).count()

                if folga == 0:

                    messages.success(request,"cadastro feito com sucesso!!!")
                    plantaoEx.save()
                else:
                    messages.error(request, "Plantao extra já existe!")
                    context = {"form": form, "plantao": plantao}
            except:
                messages.error(request, "Plantao extra já existe!")
                context = {"form": form, "form.errors": form.errors, 'plantao': plantao}
        else:
            plantao = Plantao.objects.all()
            context = {"form": form, "form.errors": form.errors,'plantao':plantao}
            messages.error(request, "Cadastro não Realizado")

        return render(request, self.template_name, context)

class PlantaoDiaView(View):

    template_name = 'coordenador/plantao_dia.html'
    def get(self, request):
        coordenador = Coordenador.objects.get(username=request.user.username)
        plantao = Plantao.objects.all()
        listaPlantao = getTurno(plantao)
        return render(request, self.template_name,{"plantao":listaPlantao})

    #@login_required(login_url='login')
    def post(self, request):
        totalPlantoes = 0
        coordenador = Coordenador.objects.get(username=request.user.username)
        turno = request.POST.get('plantao')
        mes =request.POST.get('month')
        ano  = request.POST.get('year')

        plantao = Plantao.objects.all()
        plantaoExtra = PlantaoExtra.objects.\
            filter(plantao=turno,data__month__exact=mes,data__year__exact=ano,equipe=coordenador.equipe)

        listaPlantao = getTurno(plantao)
        folga_plantao_e = getFolgaE(int(mes),equipe=coordenador.equipe)

        plantaofolga = Folga.objects.filter(plantao=turno,data__month__exact=mes,data__year__exact=ano,equipe=coordenador.equipe)
        totalPlantoes = getTotalDayoff(plantaofolga,mes,coordenador.equipe)

        return render(request, self.template_name,{"mes":mes,"plantao":listaPlantao,"plantaofolga":plantaofolga,"turno":turno,"plantaoExtra":plantaoExtra,"folga_plantao_e":folga_plantao_e,"totalPlantoes":totalPlantoes})

@login_required(login_url='login')
def apagar_plantao(request, data=datetime,turno=""):
    coordenador = Coordenador.objects.get(username=request.user.username)
    plantao = Plantao.objects.all()
    listaPlantao = getTurno(plantao)
    try:
        folga = Folga.objects.get(data=data,equipe=coordenador.equipe)
        folga.delete()
    except:
        plantaoExtra = PlantaoExtra.objects.filter(data=data,equipe=coordenador.equipe)
        plantaoExtra.delete()

    if turno is not " ":
        folga = Folga.objects.filter(plantao=turno,data__month__exact=data[5:7],equipe=coordenador.equipe)
        plantaoExtra = PlantaoExtra.objects.filter(plantao=turno,data__month__exact=data[5:7],equipe=coordenador.equipe)

    funcionarios = Funcionario.objects.all()
    plantaofolga = Folga.objects.filter(plantao=turno,data__month__exact=data[5:7],equipe=coordenador.equipe)

    totalPlantoes = getTotalDayoff(plantaofolga, data[5:7],coordenador.equipe)

    context = {"folga":folga,"funcionarios":funcionarios,"plantaoExtra":plantaoExtra,"plantao":listaPlantao,"plantaofolga":folga,"turno":turno,"totalPlantoes":totalPlantoes}
    if coordenador.is_authenticated:
        return render(request, "coordenador/plantao_dia.html",context)
    else:
        return redirect('logout_view')

def get_context(request):
    coordenador = Coordenador.objects.get(username=request.user.username)
    if coordenador.is_authenticated:
        mes = request.POST.get('selected_month')
        year = request.POST.get('selected_year')
        global ano
        if mes is None and year is None:
            mes = month
            year = ano
        else:
            mes = int(request.POST.get('selected_month'))
            ano = int(request.POST.get('selected_year'))
        dayNamesMin = ['S', 'T', 'Q', 'Q', 'S', 'S', 'D']
        meses = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro",
                 "Novembro", "Dezembro"]
        semana = []
        domingos = []
        dias_mes = getDiasMes(mes)  # recebe a quantidade de dias do mes
        for i in range(1, dias_mes + 1):
            dt = datetime(year=ano, month=mes, day=i)
            if (dayNamesMin[dt.weekday()]) == 'D':
                domingos.append(datetime.strptime(dt.strftime("%Y-" + str(mes) + "-" + str(i)), "%Y-%m-%d"))
            semana.append(dayNamesMin[dt.weekday()])

        folga_domingos = obterTurnodeFolgaDomingo(domingos, coordenador.equipe)
        funcionarios = Funcionario.objects.all() \
            .filter(equipe=coordenador.equipe) \
            .exclude(Q(extra="Folguista") | Q(extra="Feirista")) \
            .order_by('turno')
        escala_f = []
        for fun in funcionarios:
            f = FuncionarioEscala((fun.nome + " " + fun.sobrenome), fun.turno)
            for i in range(1, dias_mes + 1):
                f.add_escala((fun.turno).split(" - ")[0])
            escala_f.append(f)
        func = Folga.objects.all().filter(equipe=coordenador.equipe).filter(data__year__exact=year)
        extra = PlantaoExtra.objects.all().filter(equipe=coordenador.equipe).filter(data__year__exact=year)
        plantonistas = Funcionario.objects.all().filter(equipe=coordenador.equipe)

        for esc_fun in escala_f:
            for i in func:
                plantao = i.plantao
                folga = ((i.data).strftime("%d"))
                mesEscala = int(((i.data).strftime("%m")))
                x = 0
                folga = (int(folga) - 1)
                while x < (dias_mes):
                    x += 1
                    if mesEscala == mes:
                        if (plantao.turno == esc_fun.turno):
                            esc_fun.add_folga(folga)

                        for i in extra:
                            plantaExtra = i.plantao
                            diaExtra = ((i.data).strftime("%d"))
                            mesExtra = int(((i.data).strftime("%m")))
                            diaExtra = (int(diaExtra) - 1)
                            if mesExtra == mes:
                                if plantaExtra.turno == esc_fun.turno:
                                    esc_fun.add_extra(diaExtra)

        context={"ano": ano, "mes": meses[mes - 1], "funcionarios": funcionarios, 'range': range(1, dias_mes + 1),
                       'semana': semana, 'escala': escala_f, "plantonistas": plantonistas, "domingos": folga_domingos, "coordenador":coordenador}
        return context
    else:
        return redirect('logout_view')
@login_required(login_url='login')
def pdf_view(request):
    from weasyprint import HTML, CSS

    context = get_context(request)
    html_string = render_to_string('coordenador/tabelapdf.html',context)
    html = HTML(string=html_string)
    result = html.write_pdf(stylesheets=[CSS(string='border-collapse: collapse !important;')])
    response = HttpResponse(content_type='application/pdf;')
    response['Content-Disposition'] = 'inline; filename=escala.pdf'
    response['Content-Transfer-Encoding'] = 'binary'

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name, 'rb')
        response.write(output.read())

    return response


def getTurno(plantao):
    listaplantao = []
    for p in plantao:
        listaplantao.append(p.turno)
    return listaplantao

def getFolgaE(mes=datetime,equipe="TARM"):

    dias_mes = getDiasMes(mes)

    folga = []
    folgas = Folga.objects.filter(data__month__exact=mes,equipe=equipe)
    PlaExtra = PlantaoExtra.objects.filter(data__month__exact=mes,equipe=equipe)


    dias = []
    for f in folgas:
        if int(f.data.strftime("%d")) < 10:
            d = int(f.data.strftime("%d").replace("0",""))
        else:
            d = int(f.data.strftime("%d"))
        if d not in dias:
            dias.append(datetime.strptime(f.data.strftime(str(ano)+"-"+str(mes)+"-"+str(d)) ,"%Y-%m-%d"))
        for i in range(1,dias_mes):
            folga.append(datetime.strptime(f.data.strftime(str(ano)+"-"+str(mes)+"-"+str(i)) ,"%Y-%m-%d"))

    for f in PlaExtra:
        if int(f.data.strftime("%d")) < 10:
            d = int(f.data.strftime("%d").replace("0", ""))
        else:
            d = int(f.data.strftime("%d"))
        if d not in dias:
            dias.append(datetime.strptime(f.data.strftime(str(ano)+"-"+str(mes)+"-"+str(d)) ,"%Y-%m-%d"))

    dias_folgas_E = list(set(folga) - set(dias))
    dias_folgas_E.sort()
    return (dias_folgas_E)

def getTotalDayoff(plantaoFolga,mes="1",equipe="TARM"):
    if plantaoFolga.count() > 0:
        folgas=Folga.objects.filter(data__month__exact=mes)
        total_folgas = 0
        total_folgas += folgas.filter(plantao=plantaoFolga.values()[0]['plantao_id'],equipe=equipe).count()
        folgas = PlantaoExtra.objects.filter(data__month__exact=mes)
        total_folgas += folgas.filter(plantao=plantaoFolga.values()[0]['plantao_id'],equipe=equipe).count()
        mes = getDiasMes(int(mes))
        return mes - total_folgas
    else:
        folgas_E = len(getFolgaE(int(mes),equipe))
        mes = getDiasMes(int(mes))
        return mes - folgas_E

def getDiaData(dt=datetime.now()):
    return dt.strftime("%d")

@login_required(login_url='login')
def clean_dayoff(request, plantao, data=datetime):
    coordenador = Coordenador.objects.get(username=request.user.username)
    folgas = Folga.objects.filter(data__month__exact=data[5:7], plantao=plantao, equipe=coordenador.equipe)
    folgas.delete()
    return redirect('plantao_dia')

class SearchPerDay(View):
    template_name = 'coordenador/search.html'
    

    def get(self, request):
        coordenador = Coordenador.objects.get(username=request.user.username)
        plantao = Plantao.objects.all()
        context = {'plantao':plantao}
        return render(request, self.template_name, context)
    
    def post(self, request):
        coordenador = Coordenador.objects.get(username=request.user.username)
        data =request.POST.get('data')
        dia = data[0:2]
        turno = Folga.objects.filter(data__day__exact=dia)[0].plantao.turno

        funcionario = Funcionario.objects.filter(equipe=coordenador.equipe).filter(turno=turno)

        context = {'folga':turno, 'funcionario':funcionario}


        return render(request, self.template_name,context)