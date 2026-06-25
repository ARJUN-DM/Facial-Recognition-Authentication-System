import os
import hashlib

image_ext =['.jpg']
def hash_image(filepath):
    with open(filepath,'rb') as f:
        bytes=f.read()
        hash_text=hashlib.sha256(bytes).hexdigest()
        print(filepath)
        print(hash_text)

def get_images(path):
    for f in os.listdir(path):
        full_path = os.path.join(path, f)
        if os.path.isdir(full_path):
            get_images(full_path)
        else:
            ext = os.path.splitext(full_path)[1]
            if ext in image_ext:
                hash_image(full_path)
if __name__=='__main__':
    get_images(".")






