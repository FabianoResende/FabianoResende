import json
from fpdf import FPDF

def criar_pdf():
    # 1. Carregar os dados do JSON
    with open('dados_curriculo.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)

    pdf = FPDF()
    pdf.add_page()
    
    # Cabeçalho - Nome e Cargo
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, dados['nome'].upper(), ln=True, align='C')
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, dados['cargo'], ln=True, align='C')
    
    pdf.ln(5)
    
    # Contato
    pdf.set_font("Arial", size=10)
    contato = f"{dados['contato']['email']} | {dados['contato']['cidade']} | {dados['contato']['linkedin']}"
    pdf.cell(0, 10, contato, ln=True, align='C')
    
    pdf.ln(10)
    
    # Seção Sobre
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "RESUMO PROFISSIONAL", ln=True)
    pdf.set_font("Arial", size=11)
    pdf.multi_cell(0, 7, dados['sobre'])
    
    pdf.ln(5)
    
    # Experiência (Lógica para listar itens do JSON)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "EXPERIÊNCIA PROFISSIONAL", ln=True)
    for exp in dados['experiencia']:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, f"{exp['empresa']} | {exp['periodo']}", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 7, exp['resumo'])
        pdf.ln(2)

    # Tecnologias
    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "TECNOLOGIAS E COMPETÊNCIAS", ln=True)
    pdf.set_font("Arial", size=11)
    tecs = ", ".join(dados['tecnologias'])
    pdf.multi_cell(0, 7, tecs)

    # Salvar
    pdf.output("curriculo_fabiano.pdf")
    print("Sucesso! PDF gerado a partir do JSON.")

if __name__ == "__main__":
    criar_pdf()
