from fpdf import FPDF


def gerar():
    pdf = FPDF()
    pdf.add_page()

    # Cabeçalho Direto (Sem ler de arquivo externo)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "FABIANO FARIA DE RESENDE", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Estudante de Sistemas de Informacao - Estacio", ln=True, align='C')
    pdf.cell(0, 10, "Local: Sao Goncalo - RJ", ln=True, align='C')

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "EXPERIENCIA PROFISSIONAL", ln=True)

    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, "Indigo Estacionamento (2016-2019): Suporte Tecnico N1 e Gestao Financeira.")

    pdf.output("curriculo_fabiano.pdf")
    print("Sucesso Total! PDF gerado com dados internos.")


if __name__ == "__main__":
    gerar()