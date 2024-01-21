from flask import Flask, render_template, request
import main
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
        sepal_length = float(request.form['SepalLengthCm'])
        sepal_width = float(request.form['SepalWidthCm'])
        petal_length = float(request.form['PetalLengthCm'])
        petal_width = float(request.form['PetalWidthCm'])

        y_pred = [[sepal_length, sepal_width, petal_length, petal_width]]
        trained_model = main.training_model()
        prediction_value = trained_model.predict(y_pred)


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

        return render_template('index.html', result_text=result_text, plot_url=plot_url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
