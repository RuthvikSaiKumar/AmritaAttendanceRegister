import PyPDF2


def merge_pdfs(file1, file2, output_file='merged.pdf'):
    pdf1_file = open(file1, 'rb')
    pdf2_file = open(file2, 'rb')

    pdf1_reader = PyPDF2.PdfReader(pdf1_file)
    pdf2_reader = PyPDF2.PdfReader(pdf2_file)

    pdf_writer = PyPDF2.PdfWriter()

    # Add all pages from pdf1
    for page_num in range(len(pdf1_reader.pages)):
        pdf_writer.add_page(pdf1_reader.pages[page_num])

    # Add all pages from pdf2
    for page_num in range(len(pdf2_reader.pages)):
        pdf_writer.add_page(pdf2_reader.pages[page_num])

    # Write the merged PDF to a file
    with open(output_file, 'wb') as merged_file:
        pdf_writer.write(merged_file)

    # Close the original files
    pdf1_file.close()
    pdf2_file.close()

    print("PDFs merged successfully!")


if __name__ == '__main__':
    merge_pdfs('attendance.pdf', 'marks_sheet.pdf')
