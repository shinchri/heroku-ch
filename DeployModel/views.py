from django.http import HttpResponse
from django.shortcuts import render
import joblib

def home(request):
  return render(request, "home.html")

def result(request):
  if request.method == 'POST':

    cls = joblib.load("finalized_model.sav")
    lis = []
    lis.append(request.POST['RI'])
    lis.append(request.POST['Na'])
    lis.append(request.POST['Mg'])
    lis.append(request.POST['Al'])
    lis.append(request.POST['Si'])
    lis.append(request.POST['K'])
    lis.append(request.POST['Ca'])
    lis.append(request.POST['Ba'])
    lis.append(request.POST['Fe'])

    print(lis)

    ans = cls.predict([lis])

    return render(request, "result.html", {'ans': ans, 'lis': lis})
  return render(request, "home.html")