import json
from fpdf import FPDF


def criar_pdf():
    # Lendo o JSON
    with open('dados_curriculo.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)

    # Escrevendo no PDF
    pdf.cell(0, 10, dados['nome'], ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, dados['cargo'], ln=True, align='C')
    pdf.cell(0, 10, f"Local: {dados['contato']['cidade']}", ln=True)

    pdf.output("curriculo_fabiano.pdf")
    print("Sucesso! PDF gerado.")


if __name__ == "__main__":
    criar_pdf()
