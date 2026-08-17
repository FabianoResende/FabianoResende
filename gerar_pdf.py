import json
from fpdf import FPDF

def carregar_dados():
    with open("dados_curriculo.json", "r", encoding="utf-8") as f:
        return json.load(f)

class PDF(FPDF):
    def header_curriculo(self, dados):
        # Nome centralizado
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, dados["nome"], align="C")
        self.ln(8)

        # Contatos (links clicaveis)
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 255)
        self.cell(0, 6, f"E-mail: {dados['contato']['email']}", align="C", link=f"mailto:{dados['contato']['email']}")
        self.ln(6)
        self.cell(0, 6, f"LinkedIn: {dados['contato']['linkedin']}", align="C", link=dados["contato"]["linkedin"])
        self.ln(6)
        self.cell(0, 6, f"GitHub: {dados['contato']['github']}", align="C", link=dados["contato"]["github"])
        self.ln(6)
        self.cell(0, 6, f"Portfolio: {dados['contato']['site']}", align="C", link=dados["contato"]["site"])
        self.ln(8)

        # Cargo e cidade
        self.set_text_color(0, 0, 0)
        self.set_font("Helvetica", "B", 11)
        # Se o cargo for muito longo, fpdf quebra automaticamente; mantemos texto simples
        self.cell(0, 6, dados["cargo"], align="C")
        self.ln(6)
        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, dados["contato"]["cidade"], align="C")
        self.ln(10)

    def secao_titulo(self, texto):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f"  {texto}", fill=True)
        self.ln(4)

def gerar_pdf(dados):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header
    pdf.header_curriculo(dados)

    # Objetivo
    pdf.secao_titulo("OBJETIVO")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, dados.get("objetivo", ""))
    pdf.ln(4)

    # Perfil / Sobre
    pdf.secao_titulo("PERFIL")
    pdf.multi_cell(0, 6, dados.get("sobre", ""))
    pdf.ln(4)

    # Formacao
    pdf.secao_titulo("FORMACAO ACADEMICA")
    for form in dados.get("educacao", []):
        linha = f"{form.get('curso','')} - {form.get('instituicao','')} ({form.get('periodo','')})"
        pdf.multi_cell(0, 6, linha)
    pdf.ln(4)

    # Competencias tecnicas
    pdf.secao_titulo("COMPETENCIAS TECNICAS")
    comp = dados.get("competencias", {})

    # Linguagens / Front-end
    linguagens = comp.get("linguagens", [])
    if linguagens:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, "Front-end / Linguagens:")
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 10)
        # escrevemos em linhas curtas para evitar quebra de palavra
        pdf.multi_cell(0, 6, ", ".join(linguagens))
        pdf.ln(2)

    # IA Aplicada - escrevemos cada item em linha separada para evitar erro de largura
    ia_items = comp.get("ia_aplicada", [])
    if ia_items:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, "IA Aplicada:")
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 10)
        for item in ia_items:
            # se item for muito longo, deixamos o multi_cell quebrar naturalmente
            pdf.multi_cell(0, 6, "- " + item)
        pdf.ln(2)

    # Ferramentas
    ferramentas = comp.get("ferramentas", [])
    if ferramentas:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, "Ferramentas:")
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 6, ", ".join(ferramentas))
        pdf.ln(4)

    # Projetos e portfolio (prioriza FlyRank)
    pdf.secao_titulo("PROJETOS E PORTFOLIO")
    for exp in dados.get("experiencia", []):
        if exp.get("empresa") == "FlyRank AI":
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 6, "FlyRank AI - Projetos Praticos")
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, exp.get("resumo", ""))
            pdf.ln(3)

    # Experiencia profissional (outras)
    pdf.secao_titulo("EXPERIENCIA PROFISSIONAL")
    for exp in dados.get("experiencia", []):
        if exp.get("empresa") != "FlyRank AI":
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 6, f"{exp.get('cargo','')} - {exp.get('empresa','')}")
            pdf.set_font("Helvetica", "I", 10)
            pdf.multi_cell(0, 6, exp.get("periodo", ""))
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, exp.get("resumo", ""))
            pdf.ln(3)

    # Certificados e cursos (links clicaveis)
    pdf.secao_titulo("CERTIFICADOS E CURSOS")
    for cert in dados.get("certificados", []):
        pdf.set_font("Helvetica", "", 11)
        pdf.write(6, f"{cert.get('nome','')} - {cert.get('instituicao','')} ")
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Helvetica", "U", 11)
        # write(h, txt, link) -> link param
        pdf.write(6, "[Acesse aqui]", cert.get("link", ""))
        pdf.set_text_color(0, 0, 0)
        pdf.ln(8)

    # Salva arquivo
    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    gerar_pdf(carregar_dados())
