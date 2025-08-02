import os
import sys
import dill
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from src.exception import CustomException


def save_object(file_path, obj):
    """
    Save any Python object using dill.
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)


def evaluate_models(x_train, y_train, x_test, y_test, models, param):
    """
    Evaluate multiple models with GridSearchCV and return a dictionary 
    of model names with their test R2 scores.
    """
    try:
        report = {}

        for model_name, model in models.items():
            para = param[model_name]

            # Grid search to find best hyperparameters
            gs = GridSearchCV(model, para, cv=3, n_jobs=-1, verbose=0)
            gs.fit(x_train, y_train)

            # Set best parameters to the model
            model.set_params(**gs.best_params_)
            model.fit(x_train, y_train)

            # Predictions
            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            # R2 scores
            train_model_score = r2_score(y_train, y_train_pred)
            test_model_score = r2_score(y_test, y_test_pred)

            report[model_name] = test_model_score

        return report

    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    """
    Load any Python object using dill.
    """
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)
