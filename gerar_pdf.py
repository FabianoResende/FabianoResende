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
        urllib.request.urlretrieve(FONT_URL, FONT_FILENAME)
        return True
    except Exception as e:
        print(f"Aviso: falha ao baixar fonte: {e}")
        return False

def carregar_dados():
    with open("dados_curriculo.json", "r", encoding="utf-8") as f:
        return json.load(f)

def limpar_email(email_raw):
    if not isinstance(email_raw, str):
        return ""
    return email_raw.replace("E-mail:", "").strip()

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
        self.cell(0, 10, nome, ln=1, align="C")

        contato = dados.get("contato", {})
        email_raw = contato.get("email", "")
        email = limpar_email(email_raw)
        linkedin_link = contato.get("linkedin", "")
        github_link = contato.get("github", "")
        site_link = contato.get("site", "")

        linkedin_display = "LinkedIn: /fabianofr"
        github_display = "GitHub: /FabianoResende"
        site_display = "Site: /FabianoResende Web"
        email_display = f"E-mail: {email}"

        if not fonte_disponivel:
            email_display = ascii_fallback(email_display)
            linkedin_display = ascii_fallback(linkedin_display)
            github_display = ascii_fallback(github_display)
            site_display = ascii_fallback(site_display)

        try:
            if fonte_disponivel:
                self.set_font("DejaVu", "", 10)
                self.set_text_color(0, 0, 255)
            else:
                self.set_font("Helvetica", "", 10)
                self.set_text_color(0, 0, 0)

            self.cell(0, 6, email_display, ln=1, align="C", link=f"mailto:{email}")
            self.cell(0, 6, linkedin_display, ln=1, align="C", link=linkedin_link)
            self.cell(0, 6, github_display, ln=1, align="C", link=github_link)
            self.cell(0, 6, site_display, ln=1, align="C", link=site_link)
        except Exception:
            self.set_text_color(0, 0, 0)
            self.cell(0, 6, email_display, ln=1, align="C")
            self.cell(0, 6, linkedin_display, ln=1, align="C")
            self.cell(0, 6, github_display, ln=1, align="C")
            self.cell(0, 6, site_display, ln=1, align="C")

        self.set_text_color(0, 0, 0)
        if fonte_disponivel:
            self.set_font("DejaVu", "B", 11)
        else:
            self.set_font("Helvetica", "B", 11)
        cargo = dados.get("cargo", "")
        foco = dados.get("foco", "")
        self.cell(0, 6, f"{cargo} | {foco}", ln=1, align="C")

        if fonte_disponivel:
            self.set_font("DejaVu", "", 10)
        else:
            self.set_font("Helvetica", "", 10)
        cidade = dados.get("contato", {}).get("cidade", "")
        if not fonte_disponivel:
            cidade = ascii_fallback(cidade)
        self.cell(0, 6, cidade, ln=1, align="C")
        self.ln(5)

    def secao_titulo(self, texto, fonte_disponivel=True):
        if fonte_disponivel:
            self.set_font("DejaVu", "B", 12)
        else:
            self.set_font("Helvetica", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f"  {texto}", ln=1, fill=True)
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
        pdf.cell(0, 6, linha, ln=1)
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
        pdf.cell(0, 6, cargo_empresa, ln=1)
        pdf.set_font("DejaVu", "I", 10) if fonte_ok else pdf.set_font("Helvetica", "I", 10)
        pdf.cell(0, 6, periodo, ln=1)
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
