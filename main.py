import graphviz
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
data = pd.read_csv('iris.csv')


#print(data.isnull().sum())

X = data[['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm']]
y = data['Species']

#Before training the model splitting data into actual train and actual test database for training and validation purpose
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
#spliting data into validation train and validation test
Xt,Xcv,Yt,Ycv = train_test_split(X_train,y_train,test_size=0.10,random_state=1)
def training_model():
    model = DecisionTreeClassifier()
    trained_model = model.fit(X_train, y_train)
    return trained_model

trained_model = training_model()

def decisionTree():
    Iris_clf = DecisionTreeClassifier(criterion='gini', min_samples_split=2)
    Iris_clf.fit(Xt, Yt)
    return Iris_clf
Iris_clf = decisionTree()

