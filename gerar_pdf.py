from fpdf import FPDF


def criar_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "FABIANO FARIA DE RESENDE", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Sistemas de Informacao - Estacio", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "RESUMO PROFISSIONAL", ln=True)

    pdf.set_font("Arial", size=11)
    texto = ("Estudante de TI em transicao de carreira. Experiencia com suporte N1, "
             "sistemas operacionais e automacao com Python.")
    pdf.multi_cell(0, 7, texto)

    pdf.output("curriculo_fabiano.pdf")
    print("PDF Gerado com Sucesso!")


if __name__ == "__main__":
    criar_pdf()