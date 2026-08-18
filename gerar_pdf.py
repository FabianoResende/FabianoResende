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
                # registra variantes usando o mesmo arquivo TTF
                self.add_font("DejaVu", "", FONT_FILENAME, uni=True)
                self.add_font("DejaVu", "B", FONT_FILENAME, uni=True)
                self.add_font("DejaVu", "I", FONT_FILENAME, uni=True)
                self.add_font("DejaVu", "BI", FONT_FILENAME, uni=True)
                self.default_font = "DejaVu"
                return
            except Exception as e:
                sys.stderr.write(f"[WARN] Falha ao registrar fonte Unicode: {e}\n")
        sys.stderr.write("[WARN] Fonte Unicode nao encontrada. Usando Helvetica (sem acentos).\n")
        self.default_font = "Helvetica"

    def header_curriculo(self, dados, usable_width):
        # garante que a fonte esteja registrada antes de usar set_font
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

    def secao_titulo(self, texto, usable_width):
        self.set_font(self.default_font, "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(usable_width, 8, f"  {texto}", fill=True)
        self.ln(6)

def escrever_lista_segura(pdf, items, usable_width, line_height=6):
    for item in items:
        texto = "- " + item
        pdf.set_x(pdf.l_margin)
        try:
            pdf.multi_cell(usable_width, line_height, texto)
        except Exception as e:
            sys.stderr.write(f"[WARN] falha ao escrever item: {texto[:120]}... erro: {e}\n")
            partes = texto.split(" ")
            buffer = ""
            for p in partes:
                if len(buffer) + len(p) + 1 > 120:
                    pdf.set_x(pdf.l_margin)
                    pdf.multi_cell(usable_width, line_height, buffer)
                    buffer = p
                else:
                    buffer = (buffer + " " + p).strip()
            if buffer:
                pdf.set_x(pdf.l_margin)
                pdf.multi_cell(usable_width, line_height, buffer)

def gerar_pdf(dados):
    pdf = PDF()
    # Garantir registro da família DejaVu antes de qualquer set_font
    try:
        if hasattr(pdf, "registrar_fonte_unicode"):
            pdf.registrar_fonte_unicode()
        else:
            pdf.add_font("DejaVu", "", FONT_FILENAME, uni=True)
            pdf.add_font("DejaVu", "B", FONT_FILENAME, uni=True)
            pdf.add_font("DejaVu", "I", FONT_FILENAME, uni=True)
            pdf.add_font("DejaVu", "BI", FONT_FILENAME, uni=True)
            pdf.default_font = "DejaVu"
    except Exception as _e:
        sys.stderr.write(f"[WARN] falha ao registrar fonte DejaVu: {_e}\n")

    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    usable_width = pdf.w - 2 * pdf.l_margin
    line_height = 6

    pdf.header_curriculo(dados, usable_width)

    pdf.secao_titulo("OBJETIVO", usable_width)
    pdf.set_font(pdf.default_font, "", 11)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(usable_width, line_height, dados.get("objetivo", ""))
    pdf.ln(4)

    pdf.secao_titulo("PERFIL", usable_width)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(usable_width, line_height, dados.get("sobre", ""))
    pdf.ln(4)

    pdf.secao_titulo("FORMAÇÃO ACADÊMICA", usable_width)
    for form in dados.get("educacao", []):
        linha = f"{form.get('curso','')} - {form.get('instituicao','')} ({form.get('periodo','')})"
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(usable_width, line_height, linha)
    pdf.ln(4)

    pdf.secao_titulo("COMPETÊNCIAS TÉCNICAS", usable_width)
    comp = dados.get("competencias", {})

    linguagens = comp.get("linguagens", [])
    if linguagens:
        pdf.set_font(pdf.default_font, "B", 11)
        pdf.cell(0, line_height, "Front-end / Linguagens:")
        pdf.ln(6)
        pdf.set_font(pdf.default_font, "", 10)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(usable_width, line_height, ", ".join(linguagens))
        pdf.ln(2)

    ia_items = comp.get("ia_aplicada", [])
    if ia_items:
        pdf.set_font(pdf.default_font, "B", 11)
        pdf.cell(0, line_height, "IA Aplicada:")
        pdf.ln(6)
        pdf.set_font(pdf.default_font, "", 10)
        escrever_lista_segura(pdf, ia_items, usable_width, line_height)
        pdf.ln(2)

    ferramentas = comp.get("ferramentas", [])
    if ferramentas:
        pdf.set_font(pdf.default_font, "B", 11)
        pdf.cell(0, line_height, "Ferramentas:")
        pdf.ln(6)
        pdf.set_font(pdf.default_font, "", 10)
        pdf.set_x(pdf.l_margin)
        pdf.multi_cell(usable_width, line_height, ", ".join(ferramentas))
        pdf.ln(4)

    pdf.secao_titulo("PROJETOS E PORTFÓLIO", usable_width)
    for exp in dados.get("experiencia", []):
        if exp.get("empresa") == "FlyRank AI":
            pdf.set_font(pdf.default_font, "B", 11)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(usable_width, line_height, "FlyRank AI - Projetos Práticos")
            pdf.set_font(pdf.default_font, "", 10)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(usable_width, 5, exp.get("resumo", ""))
            pdf.ln(3)

    pdf.secao_titulo("EXPERIÊNCIA PROFISSIONAL", usable_width)
    for exp in dados.get("experiencia", []):
        if exp.get("empresa") != "FlyRank AI":
            pdf.set_font(pdf.default_font, "B", 11)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(usable_width, line_height, f"{exp.get('cargo','')} - {exp.get('empresa','')}")
            pdf.set_font(pdf.default_font, "I", 10)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(usable_width, line_height, exp.get("periodo", ""))
            pdf.set_font(pdf.default_font, "", 10)
            pdf.set_x(pdf.l_margin)
            pdf.multi_cell(usable_width, 5, exp.get("resumo", ""))
            pdf.ln(3)

                    # --- CERTIFICADOS E CURSOS (título clicável) ---
    DRIVE_LINK = "https://drive.google.com/drive/folders/1qsDa6bGyc49aoh98x7J0JtX6ToiAs6WM?usp=drive_link"

    # desenha o título como célula preenchida (mesma aparência de secao_titulo)
    pdf.set_fill_color(230, 230, 230)
    pdf.set_font(pdf.default_font, "B", 12)
    # escreve o título normalmente (preenchido)
    pdf.cell(usable_width, 8, f"  CERTIFICADOS E CURSOS", fill=True)
    pdf.ln(6)

    # sobrepõe o link clicável exatamente sobre o texto do título
    # posiciona o cursor no início do título (mesma X da margem) e escreve o texto com link
    x_title = pdf.l_margin + 2  # pequeno deslocamento para alinhar com o espaço inicial "  "
    y_title = pdf.get_y() - 14   # volta para a linha do título (ajuste se necessário)
    pdf.set_xy(x_title, y_title)
    pdf.set_text_color(0, 0, 255)
    pdf.set_font(pdf.default_font, "U", 12)
    pdf.write(8, "CERTIFICADOS E CURSOS", DRIVE_LINK)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # lista de certificados (apenas texto, sem links por item)
    certs = dados.get("certificados", [])
    pdf.set_font(pdf.default_font, "", 11)
    pdf.set_x(pdf.l_margin)
    for cert in certs:
        linha = f"● {cert.get('nome','')} - {cert.get('instituicao','')} ({cert.get('ano','')})"
        pdf.multi_cell(usable_width, 6, linha)
    pdf.ln(6)


    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    gerar_pdf(carregar_dados())

