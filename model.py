import os
import numpy as np
import tensorflow as tf
import string
from pathlib import Path

IMG_HEIGHT = 100
IMG_WIDTH = 120
CHARS = string.ascii_lowercase
idx_to_char = {idx: char for idx, char in enumerate(CHARS)}

model_path = 'cnn_captcha.keras'
if os.path.exists(model_path):
    model = tf.keras.models.load_model(model_path)
input("ready for predict...")
test_img_dir = Path('test_captcha')

for c in test_img_dir.iterdir():
    if os.path.exists(c):
        img = tf.keras.utils.load_img(c, target_size = (IMG_HEIGHT, IMG_WIDTH), color_mode = 'grayscale')
        img_array = tf.keras.utils.img_to_array(img)
        input_tensor = np.expand_dims(img_array, axis=0)
        predictions = model.predict(input_tensor, verbose = 0)
        
        predicted_text = ""
        for i in range(4):
            char_idx = np.argmax(predictions[i][0])
            predicted_text += idx_to_char[char_idx]
            
        file_name = c.stem
        if len(file_name) > 4:
            file_name = c.stem.split('_')[0] 

        '''if file_name != predicted_text:
            print(f"{c.name}:{predicted_text}\n")'''

        print("\n==============================================")
        print(f"=     target：{c}     =")
        print(f"=\t     resault：【 {predicted_text} 】             =")
        print("==============================================")
        '''
        for i in range(4):
            top_3_idx = np.argsort(predictions[i][0])[-2:][::-1]
            for idx in top_3_idx:print(f"字元:{idx_to_char[idx]}, 信心度:{predictions[i][0][idx]*100:.2f}%")
            print("==============================================")
    '''