import numpy as np
import tensorflow as tf

model_dir = "./model"
images_dir = "./images"
image_size = 224


def load_image(path):
    image = tf.keras.preprocessing.image.load_img(path)
    image_array = tf.keras.preprocessing.image.img_to_array(image)
    return tf.image.resize(image_array, [image_size, image_size]).numpy() / 255.0


cat_image = load_image(f"{images_dir}/cat.jpg")
dog_image = load_image(f"{images_dir}/dog.jpg")
image_batch = np.array([cat_image, dog_image])

model_sm = tf.keras.models.load_model(model_dir)
model_sm.summary()
predictions_sm = model_sm.predict(image_batch)

print(predictions_sm)
print(tf.nn.softmax(predictions_sm))
