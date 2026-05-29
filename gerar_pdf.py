import json
from fpdf import FPDF

def carregar_dados():
    with open("dados_curriculo.json", "r", encoding="utf-8") as f:
        return json.load(f)

class PDF(FPDF):
    def header_curriculo(self, dados):
        self.set_font("Arial", "B", 18)
        self.cell(0, 10, dados["nome"], ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.set_text_color(0, 0, 255)
        self.cell(0, 6, dados["contato"]["email"], ln=True, align="C", link=f"mailto:{dados['contato']['email']}")
        self.cell(0, 6, "LinkedIn: /fabianofr", ln=True, align="C", link=dados["contato"]["linkedin"])
        self.cell(0, 6, "GitHub: /FabianoResende", ln=True, align="C", link=dados["contato"]["github"])
        self.cell(0, 6, "https://fabianoresende.github.io/meu-projeto-web/", ln=True, align="C", link=dados["contato"]["site"])
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "B", 11)
        self.cell(0, 6, f"{dados['cargo']} | {dados['foco']}", ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 6, dados["contato"]["cidade"], ln=True, align="C")
        self.ln(5)

    def secao_titulo(self, texto):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f"  {texto}", ln=True, fill=True)
        self.ln(2)

def gerar_pdf(dados):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.header_curriculo(dados)

    sections = [
        ("Objetivo", dados["objetivo"]),
        ("Resumo Profissional", dados["sobre"])
    ]

    for title, content in sections:
        pdf.secao_titulo(title)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, content)
        pdf.ln(4)

    pdf.secao_titulo("Formação Acadêmica")
    for ed in dados["educacao"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{ed['curso']} - {ed['instituicao']} ({ed['periodo']})", ln=True)
    pdf.ln(4)

    pdf.secao_titulo("Experiência Profissional")
    for exp in dados["experiencia"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{exp['cargo']} - {exp['empresa']}", ln=True)
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 6, exp["periodo"], ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, exp["resumo"])
        pdf.ln(3)

    pdf.secao_titulo("Certificados e Cursos")
    for cert in dados["certificados"]:
        pdf.set_font("Arial", "", 11)
        pdf.write(6, f"{cert['nome']} - {cert['instituicao']} ")
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Arial", "U", 11)
        pdf.write(6, "[Acesse a pasta aqui]", cert["link"])
        pdf.set_text_color(0, 0, 0)
        pdf.ln(8)

    pdf.output("curriculo_fabiano.pdf")

def atualizar_readme(dados):
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# {dados['nome']} 👋\n\n")
        f.write(f"### {dados['cargo']}\n\n")
        f.write("![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ")
        f.write("![SQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white) ")
        f.write("![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)\n\n")
        f.write(f"## 🚀 Sobre\n{dados['sobre']}\n\n")
        f.write(f"## 🛠️ Competências\n- **Linguagens:** {', '.join(dados['competencias']['linguagens'])}\n")
        f.write(f"- **Ferramentas:** {', '.join(dados['competencias']['ferramentas'])}\n\n")
        f.write(f"--- \n### 📄 Currículo Completo Atualizado\n[👉 Visualizar PDF](./curriculo_fabiano.pdf)\n\n")
        f.write(f"*Nota: Atualizado via Automação.*")

if __name__ == "__main__":
    info = carregar_dados()
    gerar_pdf(info)
    atualizar_readme(info)
