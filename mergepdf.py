import PyPDF2


def merge_pdfs(pdf1, pdf2, output_pdf):
    # Create a PDF merger object
    merger = PyPDF2.PdfMerger()

    # Append both PDFs
    merger.append(pdf1)
    merger.append(pdf2)

    # Write to the output file
    merger.write(output_pdf)
    merger.close()


# Example usage
merge_pdfs("affdavit_property.pdf", "affdavit_relation.pdf", "affdavit.pdf")
print("PDFs merged successfully!")