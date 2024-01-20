from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

train_data_dir = '/Users/tszsanwu/Desktop/Code/Knowledge_Retrieval_and_Inference_System_for_Test_Yielding/AI/ADA/Computer Vision/Augmented Vision/TensorFlow/Dataset/Training'
batch_size = 32
image_size = (480, 480)

train_datagen = ImageDataGenerator()

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=image_size,
    batch_size=batch_size,
    class_mode='categorical')

model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(480, 480, 3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(47, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // batch_size,
    epochs=10)

model.save('FruitClassifier.keras')
