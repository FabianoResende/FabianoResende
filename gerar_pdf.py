import json
from fpdf import FPDF

def criar_pdf():
    with open('dados_curriculo.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)

    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, dados['nome'].upper(), ln=True, align='C')
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 7, dados['cargo'], ln=True, align='C')
    pdf.cell(0, 7, f"{dados['contato']['email']} | {dados['contato']['cidade']}", ln=True, align='C')
    pdf.ln(10)
    
    # Resumo
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "RESUMO PROFISSIONAL", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 6, dados['sobre'])
    pdf.ln(5)
    
    # Competências Técnicas
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "COMPETÊNCIAS TÉCNICAS", ln=True)
    pdf.set_font("Arial", size=10)
    for cat, itens in dados['competencias'].items():
        pdf.cell(0, 6, f"• {cat.replace('_', ' ').title()}: {', '.join(itens)}", ln=True)
    pdf.ln(5)

    # Experiência
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "EXPERIÊNCIA PROFISSIONAL", ln=True)
    for exp in dados['experiencia']:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, f"{exp['empresa']} | {exp['cargo']} ({exp['periodo']})", ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 6, exp['resumo'])
        pdf.ln(3)

    # Projetos
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "PROJETOS EM DESTAQUE", ln=True)
    for proj in dados['projetos']:
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 6, proj['nome'], ln=True)
        pdf.set_font("Arial", size=10)
        pdf.multi_cell(0, 6, proj['descricao'])
        pdf.ln(2)

    pdf.output("curriculo_fabiano.pdf")
    print("PDF Gerado!")

if __name__ == "__main__":
    criar_pdf()
