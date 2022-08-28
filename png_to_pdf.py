from email.mime import image
from PIL import Image
import os


def main():
    # obtain all the images in the specified directory
    directory = './screenshots'
    images = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.png')]

    images.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    # iterate through all the images and add them to a pdf file

    pdf_file = './01.pdf'

    images_list = []



    for i in images:
        imagen = Image.open(i)
        imagen = imagen.convert('RGB')
        images_list.append(imagen)

    images_list[0].save(pdf_file, 'PDF', resolution=100.0, save_all=True, append_images=images_list[1:])

if __name__ == '__main__':
    main()
    print('Done!')