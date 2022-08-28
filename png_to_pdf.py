from PIL import Image
import os
import pdf_compressor


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

    # key = 'project_public_778d413cc2b26d9a0715f38b579e2e13__2NA1bf7a78ab7ad461d3e550ab6472603d5d'
    # task = pdf_compressor.Compress(key)
    # task.add_file(pdf_file)
    # task.process()
    # task.download("./pdf")
    # task.delete_current_task()

if __name__ == '__main__':
    main()
    print('Done!')