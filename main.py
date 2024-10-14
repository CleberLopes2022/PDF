import streamlit as st
from PyPDF2 import PdfReader, PdfWriter

# Função para carregar PDF e exibir as páginas disponíveis
def load_pdf(file):
    reader = PdfReader(file)
    num_pages = len(reader.pages)
    return reader, num_pages

# Função para mesclar PDFs com base nas páginas selecionadas
def merge_pdfs(pdf1, pdf2, pages_pdf1, pages_pdf2):
    writer = PdfWriter()
    
    # Adiciona as páginas selecionadas do primeiro PDF
    for page_num in pages_pdf1:
        writer.add_page(pdf1.pages[page_num - 1])
    
    # Adiciona as páginas selecionadas do segundo PDF
    for page_num in pages_pdf2:
        writer.add_page(pdf2.pages[page_num - 1])
    
    return writer

# Título do aplicativo
st.title("Unificador de PDFs com seleção de páginas")


with st.sidebar:
    st.image("pdf.png")
    st.text(" ")
    st.text("Unifique seu pdf com este aplicativo web")



# Upload dos dois arquivos PDF
uploaded_file1 = st.file_uploader("Envie o primeiro PDF", type="pdf")
uploaded_file2 = st.file_uploader("Envie o segundo PDF", type="pdf")

if uploaded_file1 and uploaded_file2:
    # Carrega os PDFs
    pdf1, num_pages_pdf1 = load_pdf(uploaded_file1)
    pdf2, num_pages_pdf2 = load_pdf(uploaded_file2)
    
    st.write(f"O primeiro PDF tem {num_pages_pdf1} páginas.")
    st.write(f"O segundo PDF tem {num_pages_pdf2} páginas.")
    
    # Seleciona as páginas para unir
    pages_pdf1 = st.multiselect(f"Selecione as páginas do primeiro PDF (1 a {num_pages_pdf1})", list(range(1, num_pages_pdf1 + 1)))
    pages_pdf2 = st.multiselect(f"Selecione as páginas do segundo PDF (1 a {num_pages_pdf2})", list(range(1, num_pages_pdf2 + 1)))
    
    if st.button("Unir PDFs"):
        if pages_pdf1 and pages_pdf2:
            # Mescla os PDFs
            writer = merge_pdfs(pdf1, pdf2, pages_pdf1, pages_pdf2)
            
            # Salva o arquivo PDF unificado
            output_pdf = "pdf_unificado.pdf"
            with open(output_pdf, "wb") as f:
                writer.write(f)
            
            # Disponibiliza o PDF para download
            with open(output_pdf, "rb") as f:
                st.download_button("Baixar PDF Unificado", data=f, file_name="pdf_unificado.pdf", mime="application/pdf")
        else:
            st.warning("Selecione ao menos uma página de cada PDF para continuar.")
