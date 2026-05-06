from fpdf import FPDF
import json

def criar_pdf():
    with open("dados_curriculo.json", "r", encoding="utf-8") as df:
        dados = json.load(df)

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

    adicionar_secao("Objetivo", dados["objetivo"])
    adicionar_secao("Resumo Profissional", dados["sobre"])

    # Formação Acadêmica
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Formação Acadêmica", ln=True)
    pdf.set_font("Arial", "", 11)
    for ed in dados["educacao"]:
        pdf.multi_cell(0, 6, f"{ed['curso']} - {ed['instituicao']} ({ed['periodo']})")
    pdf.ln(4)

    # Experiência Profissional (Corrigido para dentro da função)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Experiência Profissional", ln=True)
    pdf.ln(2)

    largura_total = pdf.w - 2 * pdf.l_margin 

    for exp in dados['experiencia']:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, f"{exp['empresa']} | {exp['cargo']} ({exp['periodo']})", ln=True)
        
        pdf.set_font("Arial", "", 10)
        # Multi_cell para permitir que o resumo quebre linhas corretamente
        pdf.multi_cell(largura_total, 5, exp['resumo'], align='L')
        pdf.ln(4)

    # Certificados e Cursos
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Certificados e Cursos", ln=True)
    
    for cert in dados["certificados"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, cert["nome"], ln=True)
        pdf.set_font("Arial", "U", 10)
        pdf.set_text_color(0, 0, 255)
        # Link clicável no PDF
        pdf.cell(0, 5, f"Ver certificado na {cert['instituicao']}", ln=True, link=cert["link"])
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    criar_pdf()
