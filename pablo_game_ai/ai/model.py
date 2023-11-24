"""
Definition of the AI model to train
"""

import tensorflow as tf
import os

def make_model(size: int, optimizer: str, loss: str):
    """
    Create a model and return it.

    Parameters
    ----------
    size : int
        size of the state
    """
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(24, activation='relu', input_shape=(size,)),
        tf.keras.layers.Dense(24, activation='relu'),
        tf.keras.layers.Dense(6, activation='linear')
    ])
    # Compile it
    model.compile(optimizer=optimizer, loss=loss)

    return(model)




def load_model_from_path(model_path):
    """
    Load a model from a path

    Parameters
    ----------
    model_path : str
        path to get the model

    Returns
    -------
    keras.Model
        loaded model
    """
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"This file '{model_path}' doesn't exist.")

    try:
        model = tf.keras.models.load_model(model_path)
        print("The model is successfully loaded.")
        return model
    except Exception as e:
        print(f"Error of loading from {model_path} and the error is {e}")
        return(None)
