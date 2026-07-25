import tensorflow as tf
from tensorflow.keras import layers, models

def build_disease_detection_model(num_classes: int, image_size: tuple = (224, 224), learning_rate: float = 1e-4, model_name: str = "mobilenetv3") -> tf.keras.Model:
    """
    Builds a Transfer Learning model for crop disease classification.
    Supports mobilenetv3, efficientnetb0, and resnet50.
    """
    input_shape = image_size + (3,)
    inputs = tf.keras.Input(shape=input_shape)
    
    # Preprocessing and Base Model selection
    if model_name.lower() == "mobilenetv3":
        x = tf.keras.applications.mobilenet_v3.preprocess_input(inputs)
        base_model = tf.keras.applications.MobileNetV3Large(input_shape=input_shape, include_top=False, weights='imagenet')
    elif model_name.lower() == "efficientnetb0":
        # EfficientNet expects inputs in [0, 255], preprocess_input is included in the model itself.
        x = tf.keras.applications.efficientnet.preprocess_input(inputs)
        base_model = tf.keras.applications.EfficientNetB0(input_shape=input_shape, include_top=False, weights='imagenet')
    elif model_name.lower() == "resnet50":
        x = tf.keras.applications.resnet50.preprocess_input(inputs)
        base_model = tf.keras.applications.ResNet50(input_shape=input_shape, include_top=False, weights='imagenet')
    else:
        raise ValueError(f"Unsupported model_name: {model_name}")
        
    base_model.trainable = False
    
    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.2)(x)
    outputs = layers.Dense(num_classes, activation='softmax')(x)
    
    model = tf.keras.Model(inputs, outputs, name=f"disease_detection_{model_name}")
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=learning_rate),
        loss=tf.keras.losses.CategoricalCrossentropy(),
        metrics=['accuracy']
    )
    
    return model
