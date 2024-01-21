import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
data = pd.read_csv('iris.csv')


#print(data.isnull().sum())

X = data[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
y = data['Species']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

def training_model():
    model = DecisionTreeClassifier()
    trained_model = model.fit(X_train, y_train)
    return trained_model

trained_model = training_model()

