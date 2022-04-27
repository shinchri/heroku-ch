from django.http import HttpResponse
from django.shortcuts import render
import os
import joblib
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

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

def ses_home(request):
  return render(request, "ses_index.html")

def ses_result(request):
  
  if request.method == 'POST':
    ses_result = ses_prediction()

    index = ses_result["index"]

    cols = ses_result["cols"]
    rows = ses_result["rows"]

    final_rows = zip(index, rows)
    print(final_rows)
    
    return render(request, "ses_result.html", {"index": index, "cols": cols, "rows": rows, "final": final_rows})
  return render(request, "ses_index.html")


def ses_prediction():
  module_dir = os.path.dirname(__file__)
  file_path = os.path.join(module_dir, "../static/eq3_data.csv")

  metric_df = pd.read_csv(file_path, index_col="Date")

  col = "Revenue"

  metric_df.index.freq = 'D'

  validation_days = 31

  train = metric_df.iloc[:-validation_days]
  test = metric_df.iloc[-validation_days:]

  train_idx = metric_df.index <= train.index[-1]

  test_idx = metric_df.index > train.index[-1]

  model = SimpleExpSmoothing(train[col], initialization_method='legacy-heuristic')
  model_results = model.fit()

  metric_df.loc[train_idx, 'SES Train Prediction'] = model_results.fittedvalues
  metric_df.loc[test_idx, 'SES Test Forecast'] = model_results.forecast(validation_days)
  
  results = {
    "index": metric_df.index.to_numpy(),
    "cols": metric_df.columns.to_numpy(),
    "rows": metric_df.to_numpy()
  }

  return results