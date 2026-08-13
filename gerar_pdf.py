import json
import os
import sys
import unicodedata
import urllib.request
from fpdf import FPDF

FONT_FILENAME = "DejaVuSans.ttf"
FONT_URL = "https://github.com/dejavu-fonts/dejavu-fonts/raw/master/ttf/DejaVuSans.ttf"

def baixar_fonte_se_necessario():
    if os.path.isfile(FONT_FILENAME):
        return True
    try:
        print(f"Baixando fonte {FONT_FILENAME} ...")
        urllib.request.urlretrieve(FONT_URL, FONT_FILENAME)
        print("Fonte baixada com sucesso.")
        return True
    except Exception as e:
        print(f"Falha ao baixar fonte: {e}")
        return False

def carregar_dados():
    with open("dados_curriculo.json", "r", encoding="utf-8") as f:
        return json.load(f)

def ascii_fallback(text):
    if not isinstance(text, str):
        return str(text)
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_text = nfkd.encode("ascii", "ignore").decode("ascii")
    ascii_text = ascii_text.replace("–", "-").replace("—", "-").replace("…", "...")
    return ascii_text

class PDF(FPDF):
    def registrar_fonte(self):
        try:
            # uni parameter may warn on some versions; keep try/except
            self.add_font("DejaVu", "", FONT_FILENAME, uni=True)
            return True
        except Exception as e:
            print(f"Aviso: não foi possível registrar fonte Unicode: {e}")
            return False

    def header_curriculo(self, dados, fonte_disponivel=True):
        if fonte_disponivel:
            fonte_disponivel = self.registrar_fonte()

        if fonte_disponivel:
            self.set_font("DejaVu", "B", 18)
        else:
            self.set_font("Helvetica", "B", 18)

        nome = dados.get("nome", "")
        self.cell(0, 10, nome, ln=True, align="C")

        if fonte_disponivel:
            self.set_font("DejaVu", "", 10)
            self.set_text_color(0, 0, 255)
        else:
            self.set_font("Helvetica", "", 10)
            self.set_text_color(0, 0, 0)

        contato = dados.get("contato", {})
        # Exibição conforme PDF "Antes": mostrar rótulos curtos, mas linkar para URLs completos
        email_display = f"E-mail: {contato.get('email', '')}"
        linkedin_display = "LinkedIn: /fabianofr"
        github_display = "GitHub: /FabianoResende"
        site_display = "Site: /FabianoResende Web"

        email_link = f"mailto:{contato.get('email','')}"
        linkedin_link = contato.get('linkedin', '')
        github_link = contato.get('github', '')
        site_link = contato.get('site', '')

        try:
            # tenta escrever com links (se viewer suportar)
            self.cell(0, 6, email_display, ln=True, align="C", link=email_link)
            # exibir rótulos curtos, linkar para URLs reais
            self.cell(0, 6, linkedin_display, ln=True, align="C", link=linkedin_link)
            self.cell(0, 6, github_display, ln=True, align="C", link=github_link)
            self.cell(0, 6, site_display, ln=True, align="C", link=site_link)
        except Exception:
            # fallback sem links
            self.set_text_color(0, 0, 0)
            self.cell(0, 6, email_display, ln=True, align="C")
            self.cell(0, 6, linkedin_display, ln=True, align="C")
            self.cell(0, 6, github_display, ln=True, align="C")
            self.cell(0, 6, site_display, ln=True, align="C")

        self.set_text_color(0, 0, 0)
        if fonte_disponivel:
            self.set_font("DejaVu", "B", 11)
        else:
            self.set_font("Helvetica", "B", 11)

        cargo = dados.get("cargo", "")
        foco = dados.get("foco", "")
        # manter a linha de cargo e foco como no "Antes"
        self.cell(0, 6, f"{cargo} | {foco}", ln=True, align="C")

        if fonte_disponivel:
            self.set_font("DejaVu", "", 10)
        else:
            self.set_font("Helvetica", "", 10)

        cidade = dados.get("contato", {}).get("cidade", "")
        # manter acentuação; se fonte não disponível, converter
        if not fonte_disponivel:
            cidade = ascii_fallback(cidade)
        self.cell(0, 6, cidade, ln=True, align="C")
        self.ln(5)

    def secao_titulo(self, texto, fonte_disponivel=True):
        if fonte_disponivel:
            self.set_font("DejaVu", "B", 12)
        else:
            self.set_font("Helvetica", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f"  {texto}", ln=True, fill=True)
        self.ln(2)

def gerar_pdf(dados):
    fonte_ok = baixar_fonte_se_necessario()
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.header_curriculo(dados, fonte_disponivel=fonte_ok)

    sections = [
        ("Objetivo", dados.get("objetivo", "")),
        ("Resumo Profissional", dados.get("sobre", ""))
    ]

    for title, content in sections:
        pdf.secao_titulo(title, fonte_disponivel=fonte_ok)
        if fonte_ok:
            pdf.set_font("DejaVu", "", 11)
            pdf.multi_cell(0, 6, content)
        else:
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 6, ascii_fallback(content))
        pdf.ln(4)

    pdf.secao_titulo("Formação Acadêmica", fonte_disponivel=fonte_ok)
    for ed in dados.get("educacao", []):
        linha = f"{ed.get('curso','')} - {ed.get('instituicao','')} ({ed.get('periodo','')})"
        if not fonte_ok:
            linha = ascii_fallback(linha)
        pdf.set_font("DejaVu", "B", 11) if fonte_ok else pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, linha, ln=True)
    pdf.ln(4)

    pdf.secao_titulo("Experiência Profissional", fonte_disponivel=fonte_ok)
    for exp in dados.get("experiencia", []):
        cargo_empresa = f"{exp.get('cargo','')} - {exp.get('empresa','')}"
        periodo = exp.get('periodo','')
        resumo = exp.get('resumo','')
        if not fonte_ok:
            cargo_empresa = ascii_fallback(cargo_empresa)
            periodo = ascii_fallback(periodo)
            resumo = ascii_fallback(resumo)
        pdf.set_font("DejaVu", "B", 11) if fonte_ok else pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, cargo_empresa, ln=True)
        pdf.set_font("DejaVu", "I", 10) if fonte_ok else pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 6, periodo, ln=True)
        pdf.set_font("DejaVu", "", 10) if fonte_ok else pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, resumo)
        pdf.ln(3)

    pdf.secao_titulo("Certificados e Cursos", fonte_disponivel=fonte_ok)
    for cert in dados.get("certificados", []):
        nome = cert.get("nome","")
        instituicao = cert.get("instituicao","")
        link = cert.get("link","")
        if not fonte_ok:
            linha = ascii_fallback(f"{nome} - {instituicao} {link}")
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 6, linha)
        else:
            pdf.set_font("DejaVu", "", 11)
            pdf.write(6, f"{nome} - {instituicao} ")
            pdf.set_text_color(0, 0, 255)
            try:
                pdf.set_font("DejaVu", "U", 11)
                pdf.write(6, "[Acesse a pasta aqui]", link)
            except Exception:
                pdf.write(6, link)
            pdf.set_text_color(0, 0, 0)
        pdf.ln(8)

    output_file = "curriculo_fabiano.pdf"
    pdf.output(output_file)
    print(f"PDF gerado: {output_file}")

if __name__ == "__main__":
    try:
        info = carregar_dados()
    except Exception as e:
        print(f"Erro ao carregar dados_curriculo.json: {e}")
        sys.exit(1)
    try:
        gerar_pdf(info)
    except Exception as e:
        print(f"Erro ao gerar PDF: {e}")
        sys.exit(1)
