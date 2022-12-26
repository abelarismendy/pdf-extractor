import os, sys, re, shutil
from PyPDF2 import PdfFileMerger



merger = PdfFileMerger()

def merge_book(book_id):
    all_pdfs = []

    file_pattern = re.compile(r'Data\s?(\(\d+\))?.pdf')

    path = f'./pdf/{book_id}/'
    destination = f'./pdf/{book_id}/all/'
    os.makedirs(destination, exist_ok=True)
    dirs = os.listdir(path)
    # sort the dirs by page range
    dirs.remove('all')
    dirs.sort(key=lambda x: int(x.split('-')[0]))
    for subpath in dirs:
        start_page = int(subpath.split('-')[0])
        end_page = int(subpath.split('-')[1])
        print(start_page, end_page)

        files = os.listdir(path + subpath)

        for file in files:
            # sort files by filename with the format Data (number).pdf
            if file_pattern.match(file):
                if '(' not in file:
                    page = 0
                else:
                    page = int(file.split('(')[1].split(')')[0])

                real_page = start_page + page
                shutil.copy(path + subpath + '/' + file, destination + str(real_page) + '.pdf')
                full_path = destination + str(real_page) + '.pdf'
                all_pdfs.append(full_path)

    all_pdfs.sort(key=lambda x: int(x.split('/')[-1].split('.')[0]))

    for pdf in all_pdfs:
        merger.append(pdf)

    destination_merged = f'./books/{book_id}.pdf'

    merger.write(destination_merged)
    merger.close()
