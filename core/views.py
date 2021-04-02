from django.shortcuts import render
from django.contrib import messages
from .forms import ContatoForm, ProdutoModelForm
from .models import Produto
from django.shortcuts import redirect


def index(request):
    context = {
        'produtos': Produto.objects.all()
    }
    return render(request, 'index.html', context)


def contato(request):
    form = ContatoForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            form.send_mail()
            # nome = form.cleaned_data['nome']
            # email = form.cleaned_data['email']
            # assunto = form.cleaned_data['assunto']
            # mensagem = form.cleaned_data['mensagem']
            #
            # print('Mensagem enviada')
            # print(f"Nome: {nome}")
            # print(f"E-mail: {email}")
            # print(f"Assunto: {assunto}")
            # print(f"Mensagem: {mensagem}")

            messages.success(request, "E-mail enviado com sucesso!")
            form = ContatoForm()
        else:
            messages.error(request, "Error ao enviar e-mail")
    content = {
        'form': form
    }
    return render(request, 'contato.html', content)


def produto(request):
    if str(request.user) != 'AnonymousUser':
        print(f"Usuário: {request.user}")
        if str(request.method) == 'POST':
            form = ProdutoModelForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Produto salvo com sucesso!')
                form = ProdutoModelForm()
            else:
                messages.error(request, 'Erro ao salvar produto!')
        else:
            form = ProdutoModelForm()

        context = {
            'form': form
        }

        return render(request, 'produto.html', context)
    else:
        return redirect('index')