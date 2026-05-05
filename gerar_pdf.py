from fpdf import FPDF
import json

def criar_pdf():
    with open("dados_curriculo.json", "r", encoding="utf-8") as df:
        dados = json.load(df)

    # Configuração inicial do PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(20, 20, 20)
    pdf.add_page()

    # Cabeçalho
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, dados["nome"], ln=True, align="C")

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, f"{dados['cargo']} | {dados['foco']}", ln=True, align="C")
    pdf.cell(0, 6, f"{dados['contato']['cidade']} | {dados['contato']['email']}", ln=True, align="C")
    pdf.cell(0, 6, dados["contato"]["linkedin"], ln=True, align="C")
    pdf.cell(0, 6, dados["contato"]["github"], ln=True, align="C")
    pdf.ln(10)

    # Função auxiliar para seções simples
    def adicionar_secao(titulo, conteudo):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, titulo, ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, conteudo)
        pdf.ln(4)

    # Objetivo e Resumo
    adicionar_secao("Objetivo", dados["objetivo"])
    adicionar_secao("Resumo Profissional", dados["sobre"])

    # Formação Acadêmica
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Formação Acadêmica", ln=True)
    pdf.set_font("Arial", "", 11)
    for ed in dados["educacao"]:
        pdf.multi_cell(0, 6, f"{ed['curso']} - {ed['instituicao']} ({ed['periodo']})")
    pdf.ln(4)

    # Experiência Profissional
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Experiência Profissional", ln=True)
    pdf.set_font("Arial", "", 11)
    for exp in dados["experiencia"]:
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(0, 6, f"{exp['empresa']} | {exp['cargo']} ({exp['periodo']})")
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, exp["resumo"])
        pdf.ln(2)

    # Certificados — SEÇÃO NOVA
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Certificados", ln=True)
    pdf.set_font("Arial", "", 11)
    for cert in dados["certificados"]:
        pdf.multi_cell(0, 6, f"{cert['nome']} - {cert['instituicao']}\n{cert['link']}")
        pdf.ln(1)
    pdf.ln(4)

    # Exportar PDF
    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    criar_pdf()
