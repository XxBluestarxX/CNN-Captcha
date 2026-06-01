import pathlib
import os

captcha_dir = pathlib.Path('./unrename_captcha')

for c in captcha_dir.iterdir():
    new_filename = os.path.basename(c).split(".")[0]

    os.rename(c, f'./xtrain_captcha/{new_filename}_2.png')
