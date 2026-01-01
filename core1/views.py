from django.shortcuts import render

def pagina_view(request):
    return render(request, 'biblioteca\index.html')
    
def catalog_view(request):
    return render(request,'catalogo\catalog.html')