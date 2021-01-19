from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Person
from .forms import PersonForm
from django.core.paginator import Paginator


@login_required
def persons_list(request):
    nome = request.GET.get('nome', None)
    sobrenome = request.GET.get('sobrenome', None)

    '''
    busca por nome && sobrenome
    persons = Person.filter(first_name=nome, last_name=sobrenome)
    '''
    '''
    busca por nome OU sobrenome
    '''
    if nome or sobrenome:
        persons = Person.objects.filter(first_name__icontains=nome) | Person.objects.filter(last_name__icontains=sobrenome)
    else:
        persons = Person.objects.all()
    return render(request, 'person.html', {'persons': persons})

@login_required
def persons_new(request):
    form = PersonForm(request.POST, request.FILES or None)

    if form.is_valid():
        form.save()
        return redirect('person_list')
    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_update(request, id):
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if form.is_valid():
        form.save()
        return redirect('person_list')

    return render(request, 'person_form.html', {'form': form})


@login_required
def persons_delete(request, id):
    person = get_object_or_404(Person, pk=id)
    form = PersonForm(request.POST or None, request.FILES or None, instance=person)

    if request.method == 'POST':
        person.delete()
        return redirect('person_list')

    return render(request, 'person_delete_confirm.html', {'person': person})
