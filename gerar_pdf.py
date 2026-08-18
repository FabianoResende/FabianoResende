# -*- coding: utf-8 -*-
import json
import os
import sys
from fpdf import FPDF

FONT_FILENAME = "DejaVuSans.ttf"  # coloque este arquivo na raiz do repo

def carregar_dados():
    with open("dados_curriculo.json", "r", encoding="utf-8") as f:
        return json.load(f)

class PDF(FPDF):
    def registrar_fonte_unicode(self):
        if os.path.isfile(FONT_FILENAME):
            try:
                self.add_font("DejaVu", "", FONT_FILENAME)
                self.add_font("DejaVu", "B", FONT_FILENAME)
                self.add_font("DejaVu", "I", FONT_FILENAME)
                self.add_font("DejaVu", "BI", FONT_FILENAME)
                self.default_font = "DejaVu"
                return
            except Exception as e:
                sys.stderr.write(f"[WARN] Falha ao registrar fonte Unicode: {e}\n")
        sys.stderr.write("[WARN] Fonte Unicode não encontrada. Usando Helvetica.\n")
        self.default_font = "Helvetica"

    def secao_titulo(self, texto, usable_width):
        self.set_font(self.default_font, "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(usable_width, 8, f"  {texto}", fill=True)
        self.ln(6)

    def header_curriculo(self, dados, usable_width):
        self.registrar_fonte_unicode()
        self.set_font(self.default_font, "B", 18)
        self.cell(0, 10, dados.get("nome", ""), align="C")
        self.ln(8)

        self.set_font(self.default_font, "", 10)
        self.set_text_color(0, 0, 255)
        self.cell(0, 6, f"E-mail: {dados['contato'].get('email','')}", align="C", link=f"mailto:{dados['contato'].get('email','')}")
        self.ln(6)
        self.cell(0, 6, f"LinkedIn: {dados['contato'].get('linkedin','')}", align="C", link=dados["contato"].get("linkedin",""))
        self.ln(6)
        self.cell(0, 6, f"GitHub: {dados['contato'].get('github','')}", align="C", link=dados["contato"].get("github",""))
        self.ln(6)
        self.cell(0, 6, f"Portfolio: {dados['contato'].get('site','')}", align="C", link=dados["contato"].get("site",""))
        self.ln(8)

        self.set_text_color(0, 0, 0)
        self.set_font(self.default_font, "B", 11)
        self.cell(0, 6, dados.get("cargo", ""), align="C")
        self.ln(6)
        self.set_font(self.default_font, "", 10)
        self.cell(0, 6, dados["contato"].get("cidade", ""), align="C")
        self.ln(10)

def escrever_lista_segura(pdf, items, usable_width, line_height=6):
    for item in items:
        texto = "- " + item
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(usable_width, line_height, texto)

def gerar_pdf(dados):
    pdf = PDF()
    pdf.registrar_fonte_unicode()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    usable_width = pdf.w - 2 * pdf.l_margin
    line_height = 6

    # Cabeçalho
    pdf.header_curriculo(dados, usable_width)

    # OBJETIVO
    pdf.secao_titulo("OBJETIVO", usable_width)
    pdf.set_font(pdf.default_font, "", 11)
    pdf.multi_cell(usable_width, line_height, dados.get("objetivo", ""))
    pdf.ln(4)

    # PERFIL
    pdf.secao_titulo("PERFIL", usable_width)
    pdf.multi_cell(usable_width, line_height, dados.get("sobre", ""))
    pdf.ln(4)

    # FORMAÇÃO ACADÊMICA
    pdf.secao_titulo("FORMAÇÃO ACADÊMICA", usable_width)
    for form in dados.get("educacao", []):
        linha = f"{form.get('curso','')} - {form.get('instituicao','')} ({form.get('periodo','')})"
        pdf.multi_cell(usable_width, line_height, linha)
    pdf.ln(4)

    # COMPETÊNCIAS TÉCNICAS
    pdf.secao_titulo("COMPETÊNCIAS TÉCNICAS", usable_width)
    comp = dados.get("competencias", {})
    pdf.set_font(pdf.default_font, "B", 11)
    pdf.cell(0, line_height, "Front-end / Linguagens:")
    pdf.ln(6)
    pdf.set_font(pdf.default_font, "", 10)
    pdf.multi_cell(usable_width, line_height, ", ".join(comp.get("linguagens", [])))
    pdf.ln(2)

    pdf.set_font(pdf.default_font, "B", 11)
    pdf.cell(0, line_height, "IA Aplicada:")
    pdf.ln(6)
    pdf.set_font(pdf.default_font, "", 10)
    escrever_lista_segura(pdf, comp.get("ia_aplicada", []), usable_width, line_height)
    pdf.ln(2)

    pdf.set_font(pdf.default_font, "B", 11)
    pdf.cell(0, line_height, "Ferramentas:")
    pdf.ln(6)
    pdf.set_font(pdf.default_font, "", 10)
    pdf.multi_cell(usable_width, line_height, ", ".join(comp.get("ferramentas", [])))
    pdf.ln(4)

    # PROJETOS E PORTFÓLIO
    pdf.secao_titulo("PROJETOS E PORTFÓLIO", usable_width)
    for exp in dados.get("experiencia", []):
        if exp.get("empresa") == "FlyRank AI":
            pdf.set_font(pdf.default_font, "B", 11)
            pdf.multi_cell(usable_width, line_height, "Programa Prático de Engenharia Front-end com IA | FlyRank AI")
            pdf.set_font(pdf.default_font, "", 10)
            pdf.multi_cell(usable_width, 5, exp.get("resumo", ""))
            pdf.ln(3)

    # EXPERIÊNCIA PROFISSIONAL
    pdf.secao_titulo("EXPERIÊNCIA PROFISSIONAL", usable_width)
    for exp in dados.get("experiencia", []):
        if exp.get("empresa") != "FlyRank AI":
            pdf.set_font(pdf.default_font, "B", 11)
            pdf.multi_cell(usable_width, line_height, f"{exp.get('cargo','')} | {exp.get('empresa','')}")
            pdf.set_font(pdf.default_font, "I", 10)
            pdf.multi_cell(usable_width, line_height, exp.get("periodo", ""))
            pdf.set_font(pdf.default_font, "", 10)
            pdf.multi_cell(usable_width, 5, exp.get("resumo", ""))
            pdf.ln(3)

    # CERTIFICADOS E CURSOS (título clicável)
    DRIVE_LINK = "https://drive.google.com/drive/folders/1qsDa6bGyc49aoh98x7J0JtX6ToiAs6WM?usp=drive_link"
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font(pdf.default_font, "B", 12)
    pdf.cell(usable_width, 8, "  CERTIFICADOS E CURSOS", fill=True)
    pdf.ln(6)

    # link sobre o título
    x_title = pdf.l_margin + 2
    y_title = pdf.get_y() - 12
    pdf.set_xy(x_title, y_title)
    pdf.set_text_color(0, 0, 255)
    pdf.set_font(pdf.default_font, "U", 12)
    pdf.write(8, "CERTIFICADOS E CURSOS", DRIVE_LINK)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)

    # lista de certificados
    pdf.set_font(pdf.default_font, "", 11)
    for cert in dados.get("
