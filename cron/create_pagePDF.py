from PyPDF2 import PdfFileWriter, PdfFileReader
import subprocess

subprocess.call(['pyenv', 'global', ' 2.7.11rc1'])
input1 = PdfFileReader(open("../src/main_api/test_dlPDF/test.pdf", "rb"))
for index in range(100):
    output = PdfFileWriter()
    page5 = input1.getPage(index)
    output.addPage(page5)

    outputStream = file("../src/main_api/test/{}.pdf".format(index), "wb")
    output.write(outputStream)
    outputStream.close()
subprocess.call(['pyenv', 'global', ' 3.5.2'])
