# CSCI 5922 Final Project
# Bailey Sauter, Fall 2023

import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, InputLayer, Lambda
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

# Function for plotting loss and accuracy across epochs
def twoAxisEpochsPlot(accuracy, loss, num_epochs):
    # Create the first axis (left y-axis)
    fig, ax1 = plt.subplots()
    x = np.linspace(1,num_epochs,num_epochs)

    # Plot the accuracy on the left y-axis
    ax1.plot(x, accuracy, color='blue', label='Model Accuracy')
    ax1.set_xlabel('Epoch #')
    ax1.set_ylabel('Accuracy', color='blue')
    ax1.tick_params('y', colors='blue')

    # Create the second axis (right y-axis)
    ax2 = ax1.twinx()

    # Plot the loss on the right y-axis
    ax2.plot(x, loss, color='red', label='Loss Function')
    ax2.set_ylabel('Loss', color='red')
    ax2.tick_params('y', colors='red')

    # Add legend
    ax1.legend(loc='upper left')
    ax2.legend(loc='upper right')

    plt.title('Model Accuracy and Loss over Epochs')
    plt.show()

def RNN_model(X,y):
    # Split into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=99)

    print("Running RNN Model")

    # Build sequential Keras model
    ncaaw_rnn = Sequential([
        InputLayer(input_shape=(X.shape[1],X.shape[2])),
        LSTM(units=100, return_sequences=True),
        Dense(64, activation='relu'),
        Dropout(rate=0.25),
        Dense(16, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    # Compile model
    ncaaw_rnn.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])

    # Print model summary
    ncaaw_rnn.summary()

    # Train model while tracking accuracy and loss metrics
    training = ncaaw_rnn.fit(X_train, y_train, batch_size=256, epochs=100, use_multiprocessing=True, verbose=True)
    accuracy = training.history['accuracy']
    loss = training.history['loss']
    # Plot accuracy vs. loss during training
    twoAxisEpochsPlot(accuracy, loss, len(loss))

    print("---TESTING---")
    # test model
    predictions = ncaaw_rnn.predict(X_test, batch_size=32, use_multiprocessing=True, verbose=True)
    evaluation = ncaaw_rnn.evaluate(X_test, y_test, batch_size=32, use_multiprocessing=True, verbose=True)

    final_predictions = np.asarray([sequence[-1][0] for sequence in predictions])
    y_test_final = np.asarray([sequence[-1] for sequence in y_test])

    # Round predictions for firm WIN/LOSS guesses
    true_accuracy = float(np.sum(np.round(final_predictions).astype(int) == y_test_final.astype(int))) / len(y_test_final)
    print("Firm Prediction Accuracy: ", true_accuracy)

    return ncaaw_rnn