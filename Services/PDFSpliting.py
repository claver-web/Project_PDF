from PyPDF2 import PdfReader, PdfWriter

def Pdf_Reader(file_name, page_number, output_path):
    try:
        reader = PdfReader(file_name)
        writer = PdfWriter()
        
        if(len(page_number) > 1):
            for page_nums in range(page_number[0], page_number[1] + 1):
                if 0 <= page_nums < len(reader.pages):
                    writer.add_page(reader.pages[page_nums])
                else:
                    print(f"⚠️ Page {page_nums + 1} does not exist in the document.")

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)
                
                return True
                
                
            
        else:
            for page_nums in page_number:
                if 0 <= page_nums < len(reader.pages):
                    writer.add_page(reader.pages[page_nums])
                else:
                    print(f"⚠️ Page {page_nums + 1} does not exist in the document.")

            with open(output_path, 'wb') as output_file:
                writer.write(output_file)

                return True
            

    except Exception as e:
        return "error"
        # print(f"❌ Error extracting pages: {e}")
    
