import json
from fpdf import FPDF


def criar_pdf():
    with open('dados_curriculo.json', 'r', encoding='utf-8') as f:
        d = json.load(f)

    pdf = FPDF()
    pdf.add_page()

    # Nome e Cargo
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, d['nome'], ln=True, align='C')
    pdf.set_font("Helvetica", size=12)
    pdf.cell(0, 10, d['cargo'], ln=True, align='C')

    # Contato
    pdf.ln(5)
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(0, 7, f"Email: {d['contato']['email']} | Local: {d['contato']['cidade']}", ln=True, align='C')
    pdf.cell(0, 7, f"LinkedIn: {d['contato']['linkedin']}", ln=True, align='C')

    # Experiência
    pdf.ln(10)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Experiência Profissional", ln=True)
    pdf.set_font("Helvetica", size=10)
    for exp in d['experiencia']:
        pdf.cell(0, 7, f"{exp['empresa']} ({exp['periodo']})", ln=True)
        pdf.multi_cell(0, 7, exp['resumo'])

    pdf.output("curriculo_fabiano.pdf")
    print("Sucesso! PDF atualizado com dados reais.")


if __name__ == "__main__":
    criar_pdf()