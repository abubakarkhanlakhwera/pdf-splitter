import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
import os
import zipfile
import shutil

# Streamlit app
def main():
    st.title("PDF Page Splitter with Single Download")

    # Upload PDF file
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Reading the uploaded PDF file
        reader = PdfReader(uploaded_file)
        total_pages = len(reader.pages)

        # Show number of pages
        st.write(f"Total pages: {total_pages}")

        # Create a directory for the uploaded PDF file
        pdf_name = uploaded_file.name.replace('.pdf', '')
        dir_name = f"split_pdfs/{pdf_name}"

        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # Split each page into separate PDF
        for page_number in range(total_pages):
            writer = PdfWriter()
            writer.add_page(reader.pages[page_number])

            output_filename = os.path.join(dir_name, f"page_{page_number + 1}.pdf")

            with open(output_filename, "wb") as output_file:
                writer.write(output_file)

        # Create a zip file containing all the split PDFs
        zip_filename = f"{dir_name}.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(dir_name):
                for file in files:
                    zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), dir_name))

        # Provide a single download button for the zip file
        with open(zip_filename, "rb") as zip_file:
            st.download_button(
                label="Download All Pages as ZIP",
                data=zip_file,
                file_name=zip_filename,
                mime="application/zip"
            )

        # Clean up by removing the directory and zip file after download
        shutil.rmtree(dir_name)
        os.remove(zip_filename)

if __name__ == "__main__":
    main()
