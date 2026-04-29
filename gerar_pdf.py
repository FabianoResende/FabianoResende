from fpdf import FPDF


def criar_pdf():
    pdf = FPDF()
    pdf.add_page()

    # Cabeçalho Direto
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "FABIANO FARIA DE RESENDE", ln=True, align='C')

    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, "Estudante de Sistemas de Informacao (4o Periodo)", ln=True, align='C')
    pdf.cell(0, 10, "Sao Goncalo - RJ | fabianofariaderesende@gmail.com", ln=True, align='C')

    # Seção Experiência
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "RESUMO PROFISSIONAL E EXPERIENCIA", ln=True)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())

    pdf.set_font("Helvetica", size=11)
    pdf.ln(5)
    texto = ("Profissional em transicao para TI. Experiencia na Indigo Estacionamento "
             "(2016-2019) com suporte N1, sistemas WA/WPS e gestao financeira. "
             "Atualmente focado em Python, AWS e Automacao.")
    pdf.multi_cell(0, 7, texto)

    pdf.output("curriculo_fabiano.pdf")
    print("Sucesso! PDF gerado com dados internos.")


if __name__ == "__main__":
    criar_pdf()