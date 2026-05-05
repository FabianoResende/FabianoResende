from fpdf import FPDF
import json

def criar_pdf():
    with open("dados_curriculo.json", "r", encoding="utf-8") as df:
        dados = json.load(df)

    # Definindo margens para garantir espaço horizontal
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_margins(20, 20, 20)

    # Cabeçalho - Centralizado
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, dados["nome"], ln=True, align="C")
    
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"{dados['cargo']} | {dados['foco']}", ln=True, align="C")
    pdf.cell(0, 6, f"{dados['contato']['cidade']} | {dados['contato']['email']}", ln=True, align="C")
    pdf.cell(0, 6, dados["contato"]["linkedin"], ln=True, align="C")
    pdf.ln(10)

    # Seções Genéricas (Resumo, Educação, etc.)
    def adicionar_secao(titulo, conteudo):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, titulo, ln=True)
        pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 170, pdf.get_y()) # Linha divisória
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, conteudo)
        pdf.ln(4)

    adicionar_secao("Objetivo", dados["objetivo"])
    adicionar_secao("Resumo Profissional", dados["sobre"])

    # Formação
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Formação Acadêmica", ln=True)
    pdf.set_font("Arial", "", 11)
    for ed in dados["educacao"]:
        pdf.multi_cell(0, 6, f"{ed['curso']} - {ed['instituicao']} ({ed['periodo']})")
    pdf.ln(4)

    # Experiência
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Experiência Profissional", ln=True)
    pdf.set_font("Arial", "", 11)
    for exp in dados["experiencia"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{exp['empresa']} | {exp['cargo']} ({exp['periodo']})", ln=True)
        pdf.set_font("Arial", "", 11)
        # O segredo: multi_cell com largura 0 ocupa a linha toda respeitando a margem
        pdf.multi_cell(0, 5, exp["resumo"])
        pdf.ln(2)

    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    criar_pdf()
