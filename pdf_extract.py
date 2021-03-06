import PyPDF2
import os.path
from PIL import Image

if __name__ == '__main__':
    DIR = 'raw-pdf'
    OUTPUT_DIR = 'PyPDF-img'
    for i in range(len(os.listdir(DIR))):
        INPUT_DATA = os.listdir(DIR)[i]
        input1 = PyPDF2.PdfFileReader(open(os.path.join(DIR,INPUT_DATA), "rb"))

        for i in range(input1.numPages):
            page = input1.getPage(i)
            xObject = page['/Resources']['/XObject'].getObject()

            for obj in xObject:
                if xObject[obj]['/Subtype'] == '/Image':
                    size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
                    data = xObject[obj].getData()
                    if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
                        mode = "RGB"
                    else:
                        mode = "P"

                    if xObject[obj]['/Filter'] == '/FlateDecode':
                        img = Image.frombytes(mode, size, data)
                        img.save(OUTPUT_DIR + '/' + INPUT_DATA + str(i) + ".png")
                    elif xObject[obj]['/Filter'] == '/DCTDecode':
                        img = open(OUTPUT_DIR + '/' + INPUT_DATA + str(i) + ".jpg", "wb")
                        img.write(data)
                        img.close()
                    elif xObject[obj]['/Filter'] == '/JPXDecode':
                        img = open(OUTPUT_DIR + '/' + INPUT_DATA + str(i) + ".jp2", "wb")
                        img.write(data)