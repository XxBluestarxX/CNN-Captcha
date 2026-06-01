import string
import numpy as np
import os
import tensorflow as tf
import keras
from keras import layers, models
import random

CHARS = string.ascii_lowercase  # a~z

char_to_idx = {char: idx for idx, char in enumerate(CHARS)} #幫個字母編碼 a~z:0~25
idx_to_char = {idx: char for idx, char in enumerate(CHARS)}

'''轉化為onehot編碼'''
def text_to_onehot(text):
    one_hot = np.zeros((4, 26)) # 產生4x26的零矩陣
    for i, char in enumerate(text.lower()):
        if char in char_to_idx:
            one_hot[i, char_to_idx[char]] = 1.0
    return one_hot
    
def load_and_clean_data(img_dir):
    images = []
    labels = [[], [], [], []] # 建立4個空列表 存放四個字 cus驗證碼有4位
    
    if not os.path.exists(img_dir):
        print("ERROR:can't find dir cheack your path")
        return None, None

    filenames = os.listdir(img_dir)
    print(f"THERE ARE {len(filenames)} FILES")

    for filename in filenames:
        if filename.endswith(('.png')):
            '''讀取並主黨名刪除檔案副檔名'''
            name_without_ext = os.path.splitext(filename)[0] # ex. abcd.png  splitext [['abcd'], ['.png']]
            
            '''如果檔名不是四個字就只取前面四個'''
            if len(name_without_ext) != 4:
                name_without_ext = name_without_ext[:4]
        
            '''讀取圖片 轉成詼諧'''
            img_path = os.path.join(img_dir, filename)
            img = tf.keras.utils.load_img(img_path, target_size=(100, 120), color_mode="grayscale")
            img_array = tf.keras.utils.img_to_array(img) / 255.0  # 歸一化
            images.append(img_array)

            one_hot = text_to_onehot(name_without_ext) # 把正確答案改成one-hot編碼
            for i in range(4):
                labels[i].append(one_hot[i]) # 並導入labels標籤裡

    X = np.array(images)
    Y = [np.array(labels[i]) for i in range(4)] # 匯入4次因為有四碼
    if len(X) > 0:
        actual_size = X.shape[0]
        indices = np.arange(actual_size)
        np.random.shuffle(indices)
        X = X[indices]
        Y = [Y[i][indices] for i in range(4)]
    
    return X, Y

folder_name = 'train_captcha'
X_data, Y_data = load_and_clean_data(folder_name)

if X_data is not None and len(X_data) > 0:
    print("file read and shuffle success")
    print(f"there are {len(X_data)} captchas")
    print(X_data.shape)
model_path = './cnn_captcha.keras'
if os.path.exists(model_path):
    model = models.load_model(model_path)
else:
    '''定義輸入層:告訴電腦一張圖的形狀是(100,120,1)'''
    inputs = layers.Input(shape=(100, 120, 1), name = 'image_input')

    '''第一層卷積層'''
    x = layers.Conv2D(32, (3,3), padding="same", activation="relu")(inputs)
    '''第一層池化層'''
    x = layers.MaxPooling2D((2,2))(x)
    '''第二層卷積層'''
    x = layers.Conv2D(64, (3,3), padding="same", activation="relu")(x)
    '''第二層池化層'''
    x = layers.MaxPooling2D((2,2))(x)
    '''第三層卷積層'''
    x = layers.Conv2D(128, (3,3), padding="same", activation="relu")(x)
    '''第三層池化層'''
    x = layers.MaxPooling2D((2,2))(x)
    '''第四層卷基層'''
    x = layers.Conv2D(256, (3,3), padding="same", activation="relu")(x)
    '''第四層池化層'''
    x = layers.MaxPooling2D((2,2))(x)
    '''第五層卷基層'''
    x = layers.Conv2D(512, (3,3), padding="same", activation="relu")(x)
    '''第五層池化層'''
    x = layers.MaxPooling2D((2,2))(x)

    x = layers.Flatten()(x)
    x = layers.Dense(512, activation="relu")(x)

    out1 = layers.Dense(26, activation="softmax", name="char1")(x)
    out2 = layers.Dense(26, activation="softmax", name="char2")(x)
    out3 = layers.Dense(26, activation="softmax", name="char3")(x)
    out4 = layers.Dense(26, activation="softmax", name="char4")(x)

    model = models.Model(inputs=inputs, outputs=[out1, out2, out3, out4])

model.summary()

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate = 1e-5 if os.path.exists(model_path) else 0.001),
    loss={
        'char1':'categorical_crossentropy',
        'char2':'categorical_crossentropy',
        'char3':'categorical_crossentropy',
        'char4':'categorical_crossentropy'
    },
    metrics={
        'char1':'accuracy',
        'char2':'accuracy',
        'char3':'accuracy',
        'char4':'accuracy'
    }
)

history = model.fit(
    X_data,
    {
        'char1':Y_data[0],
        'char2':Y_data[1],
        'char3':Y_data[2],
        'char4':Y_data[3]
    },
    batch_size=32,
    epochs=5,
    validation_split=0.2
)

results = model.evaluate(np.array(X_data), [Y_data[0], Y_data[1], Y_data[2], Y_data[3]], verbose=0)
avg_accuracy = (results[5] * results[6] * results[7] * results[8])
avg_loss = results[1] * results[2] * results[3] * results[4]
print("==========================================================")
print('TOTEL LOSS:', results[0])
print(results[5], results[7], results[6], results[8])
print('TEST ACCURACY:', f'{(avg_accuracy)*100:.2f}%')
model.save('cnn_captcha.keras')