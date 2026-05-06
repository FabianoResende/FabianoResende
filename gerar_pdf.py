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

    # Função auxiliar
    def adicionar_secao(titulo, conteudo):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, titulo, ln=True)
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

    # ... (código anterior igual)

pdf.set_font("Arial", "B", 12)
pdf.cell(0, 8, "Experiência Profissional", ln=True)
pdf.ln(2)

# Largura total disponível (Margem esquerda até a margem direita)
largura_total = pdf.w - 2 * pdf.l_margin 

for exp in dados['experiencia']:
    pdf.set_font("Arial", "B", 11)
    # Usamos 0 para ocupar a linha toda no cell
    pdf.cell(0, 7, f"{exp['empresa']} | {exp['cargo']} ({exp['periodo']})", ln=True)
    
    pdf.set_font("Arial", "", 10)
    # O segredo está aqui: largura total e alinhamento 'J' (justificado) ou 'L'
    pdf.multi_cell(largura_total, 5, exp['resumo'], align='L')
    pdf.ln(4)

# ... (restante do código de certificados)

    for exp in dados["experiencia"]:
        pdf.set_font("Arial", "B", 11)
        pdf.multi_cell(largura_util, 6, f"{exp['empresa']} | {exp['cargo']} ({exp['periodo']})")
        pdf.set_font("Arial", "", 11)
        # Usando a largura calculada em vez de 0 para evitar o erro
        pdf.multi_cell(largura_util, 5, exp["resumo"])
        pdf.ln(2)

    # Certificados
    pdf.ln(2)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Certificados e Cursos", ln=True)
    
    for cert in dados["certificados"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, cert["nome"], ln=True)
        pdf.set_font("Arial", "I", 10)
        pdf.set_text_color(0, 0, 255)
        # Link direto
        pdf.cell(0, 5, f"Ver certificado na {cert['instituicao']}", ln=True, link=cert["link"])
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

    for cert in dados["certificados"]:
        texto_cert = f"{cert['nome']} - {cert['instituicao']}"

        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Arial", "U", 11)
        pdf.multi_cell(0, 6, texto_cert, link=cert['link'])

        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 11)
        pdf.ln(2)

    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    criar_pdf()
