from fpdf import FPDF
import json

def criar_pdf():
    with open("dados_curriculo.json", "r", encoding="utf-8") as df:
        dados = json.load(df)

    pdf = FPDF()
    pdf.add_page()

    # Cabeçalho
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, dados["nome"], ln=True, align="C")

    pdf.set_font("Arial", "", 11)
    contato_linha1 = f'{dados["contato"]["cidade"]} | {dados["contato"]["email"]}'
    pdf.cell(0, 8, contato_linha1, ln=True, align="C")
    pdf.cell(0, 8, dados["contato"]["linkedin"], ln=True, align="C")
    pdf.ln(8)

    # Objetivo
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Objetivo", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, dados["objetivo"])
    pdf.ln(4)

    # Sobre
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Resumo Profissional", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, dados["sobre"])
    pdf.ln(4)

    # Formação Acadêmica
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Formação Acadêmica", ln=True)
    pdf.set_font("Arial", "", 11)
    for formacao in dados["educacao"]:
        linha = f'{formacao["curso"]} - {formacao["instituicao"]} ({formacao["periodo"]})'
        pdf.multi_cell(0, 6, linha)
    pdf.ln(4)

    # Competências Técnicas
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Competências Técnicas", ln=True)
    pdf.set_font("Arial", "", 11)

    comp = dados["competencias"]
    texto_comp = []
    texto_comp.append("Linguagens: " + ", ".join(comp["linguagens"]))
    texto_comp.append("Banco de Dados: " + ", ".join(comp["banco_de_dados"]))
    texto_comp.append("Ferramentas: " + ", ".join(comp["ferramentas"]))
    texto_comp.append("Sistemas: " + ", ".join(comp["sistemas"]))

    pdf.multi_cell(0, 6, "\n".join(texto_comp))
    pdf.ln(4)

    # Experiência Profissional
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Experiência Profissional", ln=True)
    pdf.set_font("Arial", "", 11)
    for exp in dados["experiencia"]:
        pdf.multi_cell(0, 6, f'{exp["cargo"]} - {exp["empresa"]} ({exp["periodo"]})')
        pdf.multi_cell(0, 6, exp["resumo"])
        pdf.ln(2)

    # Projetos
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Projetos", ln=True)
    pdf.set_font("Arial", "", 11)
    for proj in dados["projetos"]:
        pdf.multi_cell(0, 6, f'{proj["nome"]}: {proj["descricao"]}')
        pdf.ln(1)

    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    criar_pdf()
