import json
from fpdf import FPDF
import sys

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

def escrever_lista_segura(pdf, items, usable_width, line_height=6):
    """
    Escreve cada item em sua propria linha usando largura segura.
    Usa try/except para capturar e logar itens problemáticos sem quebrar o job.
    """
    for item in items:
        texto = "- " + item
        try:
            pdf.multi_cell(usable_width, line_height, texto)
        except Exception as e:
            # Log minimal para diagnostico e continuar
            sys.stderr.write(f"[WARN] falha ao escrever item: {texto[:120]}... erro: {e}\n")
            # fallback: dividir o item em pedaços por espaco e escrever em partes
            partes = texto.split(" ")
            buffer = ""
            for p in partes:
                if len(buffer + " " + p) > 200:
                    pdf.multi_cell(usable_width, line_height, buffer)
                    buffer = p
                else:
                    buffer = (buffer + " " + p).strip()
            if buffer:
                pdf.multi_cell(usable_width, line_height, buffer)

def gerar_pdf(dados):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    usable_width = pdf.w - 2 * pdf.l_margin
    line_height = 6

    # Header
    pdf.header_curriculo(dados)

    # OBJETIVO
    pdf.secao_titulo("OBJETIVO")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(usable_width, line_height, dados.get("objetivo", ""))
    pdf.ln(4)

    # PERFIL
    pdf.secao_titulo("PERFIL")
    pdf.multi_cell(usable_width, line_height, dados.get("sobre", ""))
    pdf.ln(4)

    # FORMACAO ACADEMICA
    pdf.secao_titulo("FORMACAO ACADEMICA")
    for form in dados.get("educacao", []):
        linha = f"{form.get('curso','')} - {form.get('instituicao','')} ({form.get('periodo','')})"
        pdf.multi_cell(usable_width, line_height, linha)
    pdf.ln(4)

    # COMPETENCIAS TECNICAS
    pdf.secao_titulo("COMPETENCIAS TECNICAS")
    comp = dados.get("competencias", {})

    linguagens = comp.get("linguagens", [])
    if linguagens:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, line_height, "Front-end / Linguagens:")
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(usable_width, line_height, ", ".join(linguagens))
        pdf.ln(2)

    ia_items = comp.get("ia_aplicada", [])
    if ia_items:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, line_height, "IA Aplicada:")
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 10)
        escrever_lista_segura(pdf, ia_items, usable_width, line_height)
        pdf.ln(2)

    ferramentas = comp.get("ferramentas", [])
    if ferramentas:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, line_height, "Ferramentas:")
        pdf.ln(6)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(usable_width, line_height, ", ".join(ferramentas))
        pdf.ln(4)

    # PROJETOS E PORTFOLIO
    pdf.secao_titulo("PROJETOS E PORTFOLIO")
    for exp in dados.get("experiencia", []):
        if exp.get("empresa") == "FlyRank AI":
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(usable_width, line_height, "FlyRank AI - Projetos Praticos")
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(usable_width, 5, exp.get("resumo", ""))
            pdf.ln(3)

    # EXPERIENCIA PROFISSIONAL
    pdf.secao_titulo("EXPERIENCIA PROFISSIONAL")
    for exp in dados.get("experiencia", []):
        if exp.get("empresa") != "FlyRank AI":
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(usable_width, line_height, f"{exp.get('cargo','')} - {exp.get('empresa','')}")
            pdf.set_font("Helvetica", "I", 10)
            pdf.multi_cell(usable_width, line_height, exp.get("periodo", ""))
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(usable_width, 5, exp.get("resumo", ""))
            pdf.ln(3)

    # CERTIFICADOS E CURSOS
    pdf.secao_titulo("CERTIFICADOS E CURSOS")
    for cert in dados.get("certificados", []):
        pdf.set_font("Helvetica", "", 11)
        pdf.write(6, f"{cert.get('nome','')} - {cert.get('instituicao','')} ")
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Helvetica", "U", 11)
        pdf.write(6, "[Acesse aqui]", cert.get("link", ""))
        pdf.set_text_color(0, 0, 0)
        pdf.ln(8)

    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    gerar_pdf(carregar_dados())
