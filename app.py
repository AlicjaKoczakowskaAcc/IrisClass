
from flask import Flask, render_template, request
from sklearn.model_selection import cross_val_score
from sklearn.tree import export_graphviz
import pydotplus
import main
import matplotlib.pyplot as plt
import io
import base64
import seaborn as sns
import pandas as pd

data = pd.read_csv('iris.csv')

#Inicjalizuje obiekt Flask, który będzie obsługiwał aplikację.
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def basic():
    #Sprawdza, czy formularz został przesłany metodą POST, a następnie pobiera dane wejściowe z formularza.
    if request.method == 'POST':
        sepal_length = float(request.form['SepalLengthCm'])
        sepal_width = float(request.form['SepalWidthCm'])
        petal_length = float(request.form['PetalLengthCm'])
        petal_width = float(request.form['PetalWidthCm'])

        #Przygotowuje dane wejściowe dla modelu i przewiduje wartość za pomocą wcześniej wytrenowanego modelu.
        y_pred = [[sepal_length, sepal_width, petal_length, petal_width]]
        trained_model = main.training_model()
        prediction_value = trained_model.predict(y_pred)

        #Tworzy tekstowy komunikat na podstawie przewidywanej klasy irysa.
        setosa = 'The flower is classified as Setosa'
        versicolor = 'The flower is classified as Versicolor'
        virginica = 'The flower is classified as Virginica'

        if prediction_value == "Iris-setosa":
            result_text = setosa
        elif prediction_value == "Iris-versicolor":
            result_text = versicolor
        else:
            result_text = virginica

        # Generowanie wykresów
        feature_names = ['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']
        features = [sepal_length, sepal_width, petal_length, petal_width]

        plt.figure(figsize=(12, 4))

        plt.subplot(1, 2, 1)
        plt.bar(feature_names, features, color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'])
        plt.title('Input Features')
        plt.ylabel('Feature Value')

        plt.subplot(1, 2, 2)
        probabilities = trained_model.predict_proba(y_pred)[0]
        plt.bar(trained_model.classes_, probabilities, color=['#1f77b4', '#ff7f0e', '#2ca02c'])
        plt.title('Class Probabilities')
        plt.ylabel('Probability')

        # Zapisz wykres do obiektu do przekazania do szablonu HTML
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        img.close()

        # Dodaje wykres sns.pairplot
        iris_pairplot = sns.pairplot(data.drop('Id', axis=1), hue='Species')
        pairplot_img = io.BytesIO()
        iris_pairplot.savefig(pairplot_img, format='png')
        pairplot_img.seek(0)
        pairplot_url = base64.b64encode(pairplot_img.getvalue()).decode()
        plt.ioff()
        pairplot_img.close()

        # Oblicza dokładność modelu za pomocą walidacji krzyżowej.
        accuracy_score = cross_val_score(main.Iris_clf, main.Xt, main.Yt, cv=3, scoring='accuracy').mean() * 100

        #return render_template('index.html', result_text=result_text, plot_url=plot_url,pairplot_url=pairplot_url,accuracy_score=accuracy_score)
        return render_template('index.html', result_text=result_text, plot_url=plot_url, pairplot_url=pairplot_url,
                               accuracy_score=accuracy_score, setosa=setosa, versicolor=versicolor, virginica=virginica)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
