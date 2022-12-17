import pandas as pd
import base64
import io

from sklearn import tree
from sklearn import preprocessing
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import train_test_split

# def remove_target(data):
#     if isinstance(data, pd.DataFrame):
#         data.columns = data.columns.str.lower()
#     else:
#         data = pd.DataFrame(data)
#         data.columns = data.columns.str.lower()
    
#     # if columns -1 is category
#     if data[data.columns[-1]].dtype == 'object':
#         status = True
#         data = data.drop(data.columns[-1], axis=1)
#     else :
#         status = False
#         data = pd.DataFrame()
        
#     return status, data


# def get_cleaned_data(contents, names):
#     if isinstance(contents, pd.DataFrame):
#         df = contents
#     else:
#         df = to_dataframe(contents, names)
    
#     df = df.dropna() # drop missing value
#     df = remove_outlier(df) # remove outlier
#     df = remove_unused_columns(df) # remove unused columns

#     return df

# def get_recomendaion(data, input_value):
    # X_train, X_test, y_train, y_test, X, y = split_data(data)

    # clf = tree.DecisionTreeClassifier(
    #     criterion="entropy", 
    #     max_depth=3,
    #     # splitter="random"
    # )
    # clf.fit(X, y)

    # y_pred = clf.predict(X_test)

    # pred = clf.predict([input_value])
    # acc = accuracy_score(y_test, y_pred)

    # return pred, acc


# def mass_recomendation(train, test):
#     train = pd.DataFrame(train)
#     train = get_cleaned_data(train, "train")

#     X_train, X_test, y_train, y_test, X, y = split_data(train)

#     countable = test[test.columns[2:]]


#     clf = tree.DecisionTreeClassifier(
#         criterion="entropy", 
#         max_depth=3,
#         # splitter="random"
#     )
#     clf.fit(X, y)

#     y_pred = clf.predict(X_test)

#     pred = clf.predict(countable)
#     acc = accuracy_score(y_test, y_pred)

#     pred = pd.DataFrame(pred)

#     # merge test with pred
#     test = test.merge(pred, left_index=True, right_index=True)

#     return test

# def remove_outlier(data):
#     Q1 = data.quantile(0.25)
#     Q3 = data.quantile(0.75)

#     IQR = Q3 - Q1

#     return data[~((data < (Q1 - 1.5 * IQR)) | (data > (Q3 + 1.5 * IQR))).any(axis=1)]


# def remove_unused_columns(data):

#     if isinstance(data, pd.DataFrame):
#         data.columns = data.columns.str.lower()
#     else:
#         data = pd.DataFrame(data)
#         data.columns = data.columns.str.lower()
    
#     if 'no' in data.columns and 'nama' in data.columns:
#         data = data.drop(['no', 'nama'], axis=1)

#     return data


# def split_data(data):
#     if 'nama' not in data.columns:
#         X = scale_data(data.drop(columns=data.columns[-1], axis=1))
#         y = data[data.columns[-1]]

#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

#         return X_train, X_test, y_train, y_test, X, y
#     else :
#         df = remove_unused_columns(data)
        
#         X = scale_data(df.drop(columns=df.columns[-1], axis=1))
#         y = df[df.columns[-1]]

#         X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

#         return X_train, X_test, y_train, y_test, X, y


# def scale_data(data):
#     min_max_scaler = preprocessing.MinMaxScaler()
#     x_scaled = min_max_scaler.fit_transform(data)

#     return x_scaled