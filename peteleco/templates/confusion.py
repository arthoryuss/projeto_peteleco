import pandas as pd
from sklearn import tree, preprocessing
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import metrics 
from sklearn.metrics import confusion_matrix
from sklearn.utils.multiclass import unique_labels
import numpy as np
import matplotlib.pyplot as plt
import graphviz 

#Importanto arquivo com amostras
df = pd.read_csv('CORRELACAO-05-FSS03-17092019.csv')

variable = df.loc[:,['Tx','R1','R2']].copy()

data_01 = df.loc[:,['Freq01','S2101','Bw01']].copy()
data_02 = df.loc[:,['Freq02','S2102','Bw02']].copy()
data_03 = df.loc[:,['Freq03','S2103','Bw03']].copy()
data_01['classification_bw'] = 0
data_01['classification_S21'] = 0
data_01['classification_Fr'] = 0
data_02['classification_bw'] = 0
data_02['classification_S21'] = 0
data_02['classification_Fr'] = 0
data_03['classification_bw'] = 0
data_03['classification_S21'] = 0
data_03['classification_Fr'] = 0
NameClass =['Insuficiente','Média','Ideal']

class Classification():
    def __init__(self):
        pass
    def segmentation(self,data):
        
        for i in data.index:
            if data.loc[i][1] >= -12:
                data.classification_S21[i] = 0
            if data.loc[i][1] < -12 and data.loc[i][1] >= -20:
                data.classification_S21[i] = 1
            if data.loc[i][1] < -20:
                data.classification_S21[i] = 2

        for i in data.index:
            if data.loc[i][2] <= 0.07:
                data.classification_bw[i] = 0
            if  data.loc[i][2] > 0.07 and data.loc[i][2] <= 0.120:
                data.classification_bw[i] = 1
            if  data.loc[i][2] > 0.120:
                data.classification_bw[i] = 2
        return data
    
    def frequency(self,data,Fr):
        for i in data.index:
            if data.loc[i][0] != 0:
                if abs((data.loc[i][0]-Fr)/Fr) >= 0.1:
                    data.classification_Fr[i] = 0
                if abs((data.loc[i][0]-Fr)/Fr) >= 0.05 and abs((data.loc[i][0]-Fr)/Fr) < 0.1:
                    data.classification_Fr[i] = 1
                if abs((data.loc[i][0]-Fr)/Fr) < 0.05:
                    data.classification_Fr[i] = 2
            else:
                data.classification_Fr[i] = 0
        return data
    
clsf = Classification()
pd.set_option('mode.chained_assignment', None)

data_01 = clsf.segmentation(data_01)
data_02 = clsf.segmentation(data_02)
data_03 = clsf.segmentation(data_03)

data_01 = clsf.frequency(data_01,4.2)
data_02 = clsf.frequency(data_02,9.5)
data_03 = clsf.frequency(data_03,10.5)


variable1_train, variable1_test, data_01_train, data_01_test = train_test_split(variable, data_01, test_size=0.3, random_state=1) 
variable2_train, variable2_test, data_02_train, data_02_test = train_test_split(variable, data_02, test_size=0.3, random_state=1)
variable3_train, variable3_test, data_03_train, data_03_test = train_test_split(variable, data_03, test_size=0.3, random_state=1)

#Criando objeto DecisionTreeClassifier para cada uma das árvores que será criada.
clf_bw_F1 = tree.DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf_bw_F2 = tree.DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf_bw_F3 = tree.DecisionTreeClassifier(criterion="entropy")
clf_s21_F1 = tree.DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf_s21_F2 = tree.DecisionTreeClassifier(criterion="entropy", max_depth=3)
clf_s21_F3 = tree.DecisionTreeClassifier(criterion="entropy")
clf_Fr_F1 = tree.DecisionTreeClassifier(criterion="entropy") #Teste de criação de árvore para Fr1=5GHz e Fr2=7GHz
clf_Fr_F2 = tree.DecisionTreeClassifier(criterion="entropy") #Teste de criação de árvore para Fr1=5GHz e Fr2=7GHz
clf_Fr_F3 = tree.DecisionTreeClassifier(criterion="entropy")

#Treinando a árvore de decisão.
clf_bw_F1 = clf_bw_F1.fit(variable1_train, data_01_train.classification_bw)
clf_bw_F2 = clf_bw_F2.fit(variable2_train, data_02_train.classification_bw)
clf_bw_F3 = clf_bw_F3.fit(variable3_train, data_03_train.classification_bw)
clf_s21_F1 = clf_s21_F1.fit(variable1_train, data_01_train.classification_S21)
clf_s21_F2 = clf_s21_F2.fit(variable2_train, data_02_train.classification_S21)
clf_s21_F3 = clf_s21_F3.fit(variable3_train, data_03_train.classification_S21)
clf_Fr_F1 = clf_Fr_F1.fit(variable1_train, data_01_train.classification_Fr) #Teste de criação de árvore para Fr1=5GHz e Fr2=7GHz
clf_Fr_F2 = clf_Fr_F2.fit(variable2_train, data_02_train.classification_Fr) #Teste de criação de árvore para Fr1=5GHz e Fr2=7GHz
clf_Fr_F3 = clf_Fr_F3.fit(variable3_train, data_03_train.classification_Fr)

#Prevendo a resposta para o conjunto de dados de teste.
clf_bw_F1_pred = clf_bw_F1.predict(variable1_test)
clf_bw_F2_pred = clf_bw_F2.predict(variable2_test)
clf_bw_F3_pred = clf_bw_F3.predict(variable3_test)
clf_s21_F1_pred = clf_s21_F1.predict(variable1_test)
clf_s21_F2_pred = clf_s21_F2.predict(variable2_test)
clf_s21_F3_pred = clf_s21_F3.predict(variable3_test)
clf_Fr_F1_pred = clf_Fr_F1.predict(variable1_test) #Teste de criação de árvore para Fr1=5GHz e Fr2=7GHz
clf_Fr_F2_pred = clf_Fr_F2.predict(variable2_test) #Teste de criação de árvore para Fr1=5GHz e Fr2=7GHz
clf_Fr_F3_pred = clf_Fr_F3.predict(variable3_test)

def plot_confusion_matrix(y_true, y_pred, classes,
                          normalize=False,
                          title=None,
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if not title:
        if normalize:
            title = 'Normalized confusion matrix'
        else:
            title = 'Confusion matrix, without normalization'

    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred)
    # Only use the labels that appear in the data
    classes = classes[unique_labels(y_true, y_pred)]
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    fig, ax = plt.subplots()
    im = ax.imshow(cm, interpolation='nearest', cmap=cmap)
    ax.figure.colorbar(im, ax=ax)
    # We want to show all ticks...
    ax.set(xticks=np.arange(cm.shape[1]),
           yticks=np.arange(cm.shape[0]),
           # ... and label them with the respective list entries
           xticklabels=classes, yticklabels=classes,
           title=title,
           ylabel='True label',
           xlabel='Predicted label')

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, format(cm[i, j], fmt),
                    ha="center", va="center",
                    color="white" if cm[i, j] > thresh else "black")
    fig.tight_layout()
    return ax

# Plot normalized confusion matrix
plot_confusion_matrix(np.array(data_03_test.classification_S21), clf_s21_F3_pred, classes=np.array(NameClass),
                      title='Confusion matrix, without normalization')

plt.savefig('teste')