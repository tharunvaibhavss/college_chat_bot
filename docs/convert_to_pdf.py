"""
Converts MCA_Academic_Assistant_Project_Report.docx to PDF using Microsoft Word automation.
Updates all document fields (including Table of Contents) before exporting.
"""
import os
import sys
import win32com.client


def convert_docx_to_pdf():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    docx_path = os.path.join(base_dir, "MCA_Academic_Assistant_Project_Report.docx")
    pdf_path = os.path.join(base_dir, "MCA_Academic_Assistant_Project_Report.pdf")

    if not os.path.exists(docx_path):
        print(f"Error: {docx_path} does not exist.")
        sys.exit(1)

    print(f"Opening Word application...")
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = 0

    try:
        print(f"Loading DOCX: {docx_path}")
        doc = word.Documents.Open(docx_path)

        # Update all fields including TOC
        print("Updating document fields and Table of Contents...")
        doc.Fields.Update()
        for toc in doc.TablesOfContents:
            toc.Update()

        # Save the updated DOCX so TOC is permanently populated
        print("Saving updated DOCX...")
        doc.Save()

        # Export to PDF (wdExportFormatPDF = 17)
        print(f"Exporting PDF to: {pdf_path}")
        doc.ExportAsFixedFormat(
            OutputFileName=pdf_path,
            ExportFormat=17,
            OpenAfterExport=False,
            OptimizeFor=0,  # wdExportOptimizeForPrint
            CreateBookmarks=1,  # wdExportCreateHeadingBookmarks
            DocStructureTags=True
        )

        doc.Close(SaveChanges=True)
        print("PDF export completed successfully.")
    except Exception as e:
        print(f"Error during Word processing: {e}")
        try:
            doc.Close(SaveChanges=False)
        except:
            pass
        raise
    finally:
        word.Quit()

    if os.path.exists(pdf_path):
        size = os.path.getsize(pdf_path)
        print(f"Verified PDF file created: {pdf_path} ({size} bytes)")
    else:
        print("Error: PDF was not generated.")


if __name__ == "__main__":
    convert_docx_to_pdf()
