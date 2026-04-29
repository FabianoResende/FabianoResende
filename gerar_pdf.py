from fpdf import FPDF


def criar_pdf():
    pdf = FPDF()
    pdf.add_page()

    # Nome e Titulo
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "FABIANO FARIA DE RESENDE", ln=True, align='C')

    pdf.set_font("helvetica", "", 12)
    pdf.cell(0, 10, "Estudante de Sistemas de Informacao - Estacio (4o Periodo)", ln=True, align='C')

    # Contato
    pdf.ln(5)
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 7, "Email: fabianofariaderesende@gmail.com | Local: Sao Goncalo - RJ", ln=True, align='C')

    # Resumo
    pdf.ln(10)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, "RESUMO PROFISSIONAL", ln=True)
    pdf.set_font("helvetica", "", 11)
    pdf.multi_cell(0, 7,
                   "Profissional em transicao para TI. Experiencia na Indigo Estacionamento (2016-2019) com suporte N1 e gestao financeira. Foco em Python e Automacao.")

    pdf.output("curriculo_fabiano.pdf")
    print("Sucesso! PDF gerado.")


if __name__ == "__main__":
    criar_pdf()