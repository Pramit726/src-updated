# -*- coding: utf-8 -*-
"""Training.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y8fwD-RFsvKqa1GZQt93LC_ILq_YFjmn

# **Feature Extraction and Fine-Tuning with MobileNetV2 and Hyperparameter Optimization**

This notebook illustrates the process of leveraging MobileNetV2 for feature extraction and fine-tuning on a custom dataset. The primary focus is on optimizing hyperparameters to enhance model performance.
"""

# Commented out IPython magic to ensure Python compatibility.
# %run -i Model.ipynb

"""### **Importing necessary libraries**"""

from keras.callbacks import EarlyStopping
from keras_tuner import RandomSearch
import matplotlib.pyplot as plt

"""### **Hyperparameter Tuning with Random Search**"""

tuner = RandomSearch(
    build_model_feature_extraction,
    objective='val_accuracy',
    max_trials=3,
    executions_per_trial=1,
    directory='./',
    project_name='Image_classification_food_ingredients_v1'
)

tuner.search(train_ds, epochs=3, validation_data=val_ds)

"""### **Get the best hyperparameters**"""

# Get the best hyperparameters from the tuner
best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]

# Retrieve the best learning rate from the best hyperparameters
base_learning_rate = best_hps.get('learning_rate')

"""### **Build feature extraction model and show summary**"""

# Build the model using the best hyperparameters for feature extraction
model = build_model_feature_extraction(best_hps)

# Print a summary of the model architecture
model.summary()

"""### **Visualize the model architecture with shape information**"""

tf.keras.utils.plot_model(model, show_shapes=True)

"""### **Early Stopping Configuration for Model Training**"""

early_stopping = EarlyStopping(
    monitor="val_loss",      # Monitor validation loss
    min_delta=0.001,         # Minimum change in the monitored quantity to qualify as an improvement
    patience=3,             # Number of epochs with no improvement after which training will be stopped
    verbose=1,               # Verbosity mode. 0: silent, 1: progress bar, 2: one line per epoch
    mode="auto",             # Direction of improvement to detect, automatically inferred from the monitored quantity
    baseline=None,           # Baseline value for the monitored quantity, used for early stopping
    restore_best_weights=False  # Whether to restore model weights from the epoch with the best value of the monitored quantity
)

"""### **Number of epochs for training**"""

epochs_size = 10

"""### **Model Training with Feature Extraction and Early Stopping**"""

print("Feature extraction\n")

# Train the model with feature extraction and early stopping
history_feature_extraction = model.fit(train_ds, epochs=epochs_size, validation_data=val_ds, callbacks=early_stopping)

"""### **Accuracy and Loss Comparison Across Epochs- Feature Extraction**"""

epochs = range(1, len(history_feature_extraction.history['accuracy']) + 1)

# Plot accuracy and loss
plt.subplot(1, 2, 1)
plt.plot(epochs, history_feature_extraction.history['accuracy'], color='y', label='train')
plt.plot(epochs, history_feature_extraction.history['val_accuracy'], color='k', label='validation')
plt.legend()
plt.title('Accuracy comparison')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs, history_feature_extraction.history['loss'], color='r', label='train')
plt.plot(epochs, history_feature_extraction.history['val_loss'], color='b', label='validation')
plt.legend()
plt.title('Loss comparison')
plt.xlabel('Epochs')
plt.ylabel('Loss')

plt.subplots_adjust(right=2)
plt.show()

"""### **Build the fine tuning model**"""

build_model_fine_tuning()

"""### **Compile the fine tuning model**"""

model.compile(optimizer=Adam(learning_rate=base_learning_rate/10), loss='sparse_categorical_crossentropy', metrics=['accuracy'])

"""### **Summary of fine tuning model**"""

model.summary()

"""### **Visulaize the fine tuning model**"""

tf.keras.utils.plot_model(model, show_shapes=True)

"""### **Continue training the model**"""

# Calculate the initial number of epochs based on the length of the accuracy history
initial_epochs = len(history_feature_extraction.history['accuracy'])

# Define the number of epochs for fine-tuning
fine_tune_epochs = 10

# Calculate the total number of epochs for fine-tuning
total_epochs = initial_epochs + fine_tune_epochs

"""### **Model Training with Fine tuning and Early Stopping**"""

print("Fine tuning\n")
history_fine_tuning = model.fit(train_ds, epochs=total_epochs, initial_epoch=initial_epochs, validation_data=val_ds, callbacks=early_stopping)

"""### **Accuracy and Loss Comparison Across Epochs- Fine Tuning**"""

epochs = range(1, len(history_fine_tuning.history['accuracy']) + 1)

# Plot accuracy and loss
plt.subplot(1, 2, 1)
plt.plot(epochs, history_fine_tuning.history['accuracy'], color='y', label='train')
plt.plot(epochs, history_fine_tuning.history['val_accuracy'], color='k', label='validation')
plt.legend()
plt.title('Accuracy comparison')
plt.xlabel('Epochs')
plt.ylabel('Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs, history_fine_tuning.history['loss'], color='r', label='train')
plt.plot(epochs, history_fine_tuning.history['val_loss'], color='b', label='validation')
plt.legend()
plt.title('Loss comparison')
plt.xlabel('Epochs')
plt.ylabel('Loss')

plt.subplots_adjust(right=2)
plt.show()