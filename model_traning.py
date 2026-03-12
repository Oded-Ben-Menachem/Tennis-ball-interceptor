from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np
import joblib
import os

np.set_printoptions(suppress=True, precision=4)
if __name__ == "__main__":

    x_tennis_ball = np.load('tennis_ball_fithre1.npy')
    x_other = np.load('other_ball_fithre1.npy')

    print(f'tennis matrix shape: {x_tennis_ball.shape}. other matrix shape: {x_other.shape}')
    X = np.vstack((x_tennis_ball,x_other))

    y = np.array(['T'] * x_tennis_ball.shape[0] + ['O'] * x_other.shape[0])

    # split for traning and for check
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)
    # biult the model
    rf_model = RandomForestClassifier(n_estimators=10 ,random_state=42)

    #trainning the model
    rf_model.fit(X_train, y_train)


    #
    predictions = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)

    feature_names = ['width_high_ratio ','circularity','circle_square_ratio',]
    importances = rf_model.feature_importances_

    print('Feature Importance:')
    for i in range(len(feature_names)):
        print(f'{feature_names[i]}:{importances[i]}')

    print('-'*30)
    print(f'prediction:{predictions}')
    print(f'accuracy: {accuracy*100:.4f}%')
    joblib.dump(rf_model,'tennis_ball_recognize.pkl')

    print(f"Current Working Directory: {os.getcwd()}")
    model_path = os.path.abspath('tennis_ball_recognize.pkl')
    print(f"Full path to your model: {model_path}")
    if os.path.exists(model_path):
        print("Found it! The file exists at this path.")
    else:
        print("Still missing. Check if you ran the save script correctly.")