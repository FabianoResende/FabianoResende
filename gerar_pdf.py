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

def safe_text(text):
    # Normaliza e mantém Unicode; se fonte não estiver disponível, faz fallback
    if not isinstance(text, str):
        return str(text)
    return text

def ascii_fallback(text):
    # Substitui caracteres problemáticos por equivalentes ASCII simples
    if not isinstance(text, str):
        return str(text)
    # Normaliza e remove caracteres não-ASCII
    nfkd = unicodedata.normalize("NFKD", text)
    ascii_text = nfkd.encode("ascii", "ignore").decode("ascii")
    # Substituições pontuais (mantém legibilidade)
    ascii_text = ascii_text.replace("–", "-").replace("—", "-").replace("…", "...")
    return ascii_text

class PDF(FPDF):
    def header_curriculo(self, dados, fonte_disponivel=True):
        if fonte_disponivel:
            try:
                # registrar fonte TTF Unicode
                self.add_font("DejaVu", "", FONT_FILENAME, uni=True)
                self.set_font("DejaVu", "B", 18)
            except Exception as e:
                print(f"Aviso: não foi possível registrar fonte Unicode: {e}")
                fonte_disponivel = False

        if not fonte_disponivel:
            # fallback para fonte core (pode gerar warnings, mas evita crash)
            self.set_font("Helvetica", "B", 18)

        nome = safe_text(dados.get("nome", ""))
        self.cell(0, 10, nome, ln=True, align="C")

        if fonte_disponivel:
            self.set_font("DejaVu", "", 10)
        else:
            self.set_font("Helvetica", "", 10)

        contato = dados.get("contato", {})
        email = contato.get("email", "")
        linkedin = contato.get("linkedin", "")
        github = contato.get("github", "")
        site = contato.get("site", "")
        cidade = contato.get("cidade", "")

        # Se fonte não disponível, converte para ASCII simples
        if not fonte_disponivel:
            email = ascii_fallback(email)
            linkedin = ascii_fallback(linkedin)
            github = ascii_fallback(github)
            site = ascii_fallback(site)
            cidade = ascii_fallback(cidade)

        # Cabeçalho com links (link funciona se PDF viewer suportar)
        try:
            self.set_text_color(0, 0, 255)
            self.cell(0, 6, f"E-mail: {email}", ln=True, align="C", link=f"mailto:{email}")
            self.cell(0, 6, f"LinkedIn: {linkedin}", ln=True, align="C", link=linkedin)
            self.cell(0, 6, f"GitHub: {github}", ln=True, align="C", link=github)
            self.cell(0, 6, f"Site: {site}", ln=True, align="C", link=site)
        except Exception:
            # fallback sem links
            self.set_text_color(0, 0, 0)
            self.cell(0, 6, f"E-mail: {email}", ln=True, align="C")
            self.cell(0, 6, f"LinkedIn: {linkedin}", ln=True, align="C")
            self.cell(0, 6, f"GitHub: {github}", ln=True, align="C")
            self.cell(0, 6, f"Site: {site}", ln=True, align="C")

        self.set_text_color(0, 0, 0)
        if fonte_disponivel:
            self.set_font("DejaVu", "B", 11)
        else:
            self.set_font("Helvetica", "B", 11)

        cargo = safe_text(dados.get("cargo", ""))
        foco = safe_text(dados.get("foco", ""))
        self.cell(0, 6, f"{cargo} | {foco}", ln=True, align="C")

        if fonte_disponivel:
            self.set_font("DejaVu", "", 10)
        else:
            self.set_font("Helvetica", "", 10)
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
            pdf.multi_cell(0, 6, safe_text(content))
        else:
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 6, ascii_fallback(content))
        pdf.ln(4)

    pdf.secao_titulo("Formação Acadêmica", fonte_disponivel=fonte_ok)
    for ed in dados.get("educacao", []):
        curso = ed.get("curso", "")
        instituicao = ed.get("instituicao", "")
        periodo = ed.get("periodo", "")
        linha = f"{curso} - {instituicao} ({periodo})"
        if fonte_ok:
            pdf.set_font("DejaVu", "B", 11)
        else:
            pdf.set_font("Helvetica", "B", 11)
        pdf.cell(0, 6, linha, ln=True)
    pdf.ln(4)

    pdf.secao_titulo("Experiência Profissional", fonte_disponivel=fonte_ok)
    for exp in dados.get("experiencia", []):
        cargo = exp.get("cargo", "")
        empresa = exp.get("empresa", "")
        periodo = exp.get("periodo", "")
        resumo = exp.get("resumo", "")
        if fonte_ok:
            pdf.set_font("DejaVu", "B", 11)
            pdf.cell(0, 6, f"{cargo} - {empresa}", ln=True)
            pdf.set_font("DejaVu", "I", 10)
            pdf.cell(0, 6, periodo, ln=True)
            pdf.set_font("DejaVu", "", 10)
            pdf.multi_cell(0, 5, safe_text(resumo))
        else:
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(0, 6, ascii_fallback(f"{cargo} - {empresa}"), ln=True)
            pdf.set_font("Helvetica", "I", 10)
            pdf.cell(0, 6, ascii_fallback(periodo), ln=True)
            pdf.set_font("Helvetica", "", 10)
            pdf.multi_cell(0, 5, ascii_fallback(resumo))
        pdf.ln(3)

    pdf.secao_titulo("Certificados e Cursos", fonte_disponivel=fonte_ok)
    for cert in dados.get("certificados", []):
        nome = cert.get("nome", "")
        instituicao = cert.get("instituicao", "")
        link = cert.get("link", "")
        if fonte_ok:
            pdf.set_font("DejaVu", "", 11)
            pdf.write(6, f"{nome} - {instituicao} ")
            pdf.set_text_color(0, 0, 255)
            pdf.set_font("DejaVu", "U", 11)
            try:
                pdf.write(6, "[Acesse a pasta aqui]", link)
            except Exception:
                pdf.write(6, link)
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(0, 6, ascii_fallback(f"{nome} - {instituicao} {link}"))
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
