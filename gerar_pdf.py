from fpdf import FPDF
import json

def criar_pdf():
    # Carrega os dados
    with open("dados_curriculo.json", "r", encoding="utf-8") as df:
        dados = json.load(df)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(20, 20, 20)
    pdf.add_page()

    # Nome Principal
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, dados["nome"], ln=True, align="C")

    # Contatos com Links Azuis
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0, 0, 255)
    
    # E-mail (mailto para abrir o Outlook/Gmail)
    pdf.cell(0, 6, dados['contato']['email'], ln=True, align="C", link=f"mailto:{dados['contato']['email']}")
    
    # LinkedIn e GitHub
    pdf.cell(0, 6, "LinkedIn: fabianofr", ln=True, align="C", link=dados['contato']['linkedin'])
    pdf.cell(0, 6, "GitHub: FabianoResende", ln=True, align="C", link=dados['contato']['github'])

    # Reseta cor para preto
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f"{dados['cargo']} | {dados['contato']['cidade']}", ln=True, align="C")
    pdf.ln(10)

    largura_util = pdf.w - 2 * pdf.l_margin

    def adicionar_secao(titulo, conteudo):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, titulo, ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(largura_util, 6, conteudo)
        pdf.ln(4)

    adicionar_secao("Objetivo", dados["objetivo"])
    adicionar_secao("Resumo Profissional", dados["sobre"])

    # Educação
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Formação Acadêmica", ln=True)
    pdf.set_font("Arial", "", 11)
    for ed in dados["educacao"]:
        pdf.multi_cell(largura_util, 6, f"{ed['curso']} - {ed['instituicao']} ({ed['periodo']})")
    pdf.ln(4)

    # Experiência
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Experiência Profissional", ln=True)
    for exp in dados['experiencia']:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, f"{exp['empresa']} | {exp['cargo']} ({exp['periodo']})", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(largura_util, 5, exp['resumo'])
        pdf.ln(4)

    # Certificados (Pasta do Drive)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Certificados e Cursos", ln=True)
    for cert in dados["certificados"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, cert["nome"], ln=True)
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Arial", "U", 10)
        pdf.cell(0, 5, "Acesse a pasta completa de certificados aqui", ln=True, link=cert["link"])
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    criar_pdf()
