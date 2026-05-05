from fpdf import FPDF
import json

def criar_pdf():
    with open("dados_curriculo.json", "r", encoding="utf-8") as df:
        dados = json.load(df)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    # Margens bem definidas para evitar o erro de falta de espaço
    pdf.set_margins(20, 20, 20)

    # Cabeçalho
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, dados["nome"], ln=True, align="C")

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"{dados['cargo']} | {dados['foco']}", ln=True, align="C")
    pdf.cell(0, 6, f"{dados['contato']['cidade']} | {dados['contato']['email']}", ln=True, align="C")
    
    # Links clicáveis no cabeçalho
    pdf.set_text_color(0, 0, 255)
    pdf.cell(0, 6, "LinkedIn", ln=True, align="C", link=dados["contato"]["linkedin"])
    pdf.cell(0, 6, "GitHub", ln=True, align="C", link=dados["contato"]["github"])
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # Função auxiliar para evitar repetição e erros de margem
    def adicionar_secao(titulo, conteudo):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, titulo, ln=True)
        pdf.set_font("Arial", "", 11)
        # O 0 aqui manda o PDF usar a largura total disponível
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

    # Experiência Profissional
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Experiência Profissional", ln=True)
    for exp in dados["experiencia"]:
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 6, f"{exp['empresa']} | {exp['cargo']} ({exp['periodo']})")
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 5, exp["resumo"])
        pdf.ln(2)

    # Certificados — Seção Limpa e Clicável
    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Certificados e Cursos", ln=True)
    
    for cert in dados["certificados"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, cert["nome"], ln=True)
        pdf.set_font("Arial", "I", 10)
        pdf.set_text_color(0, 0, 255)
        # Link clicável direto no nome da instituição
        pdf.cell(0, 5, f"Ver certificado na {cert['instituicao']}", ln=True, link=cert["link"])
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    criar_pdf()
