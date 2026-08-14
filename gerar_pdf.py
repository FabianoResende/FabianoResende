import json
from fpdf import FPDF

def carregar_dados():
    with open("dados_curriculo.json", "r", encoding="utf-8") as f:
        return json.load(f)

class PDF(FPDF):
    def header_curriculo(self, dados):
        # Título
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, dados["nome"], new_x="LMARGIN", new_y="NEXT", align="C")

        # Contatos com links
        self.set_font("Helvetica", "", 10)
        self.set_text_color(0, 0, 255)

        self.cell(
            0, 6,
            f"E-mail: {dados['contato']['email']}",
            new_x="LMARGIN", new_y="NEXT",
            align="C",
            link=f"mailto:{dados['contato']['email']}"
        )

        self.cell(
            0, 6,
            f"LinkedIn: {dados['contato']['linkedin']}",
            new_x="LMARGIN", new_y="NEXT",
            align="C",
            link=dados["contato"]["linkedin"]
        )

        self.cell(
            0, 6,
            f"GitHub: {dados['contato']['github']}",
            new_x="LMARGIN", new_y="NEXT",
            align="C",
            link=dados["contato"]["github"]
        )

        self.cell(
            0, 6,
            f"Portfólio: {dados['contato']['site']}",
            new_x="LMARGIN", new_y="NEXT",
            align="C",
            link=dados["contato"]["site"]
        )

        # Reset de cor
        self.set_text_color(0, 0, 0)

        # Cargo + foco
        self.set_font("Helvetica", "B", 11)
        self.cell(
            0, 6,
            f"{dados['cargo']} | {dados['foco']}",
            new_x="LMARGIN", new_y="NEXT",
            align="C"
        )

        # Cidade
        self.set_font("Helvetica", "", 10)
        self.cell(
            0, 6,
            dados["contato"]["cidade"],
            new_x="LMARGIN", new_y="NEXT",
            align="C"
        )

        self.ln(5)

    def secao_titulo(self, texto):
        self.set_font("Helvetica", "B", 12)
        self.set_fill_color(230, 230, 230)
        self.cell(0, 8, f"  {texto}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)

def gerar_pdf(dados):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.header_curriculo(dados)

    # Objetivo e perfil
    pdf.secao_titulo("Objetivo")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, dados["objetivo"])
    pdf.ln(4)

    pdf.secao_titulo("Perfil")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, dados["sobre"])
    pdf.ln(4)

    # Formação
    pdf.secao_titulo("Formação Acadêmica")
    for ed in dados["educacao"]:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(
            0, 6,
            f"{ed['curso']} — {ed['instituicao']} ({ed['periodo']})",
            new_x="LMARGIN", new_y="NEXT"
        )
    pdf.ln(4)

    # Experiência
    pdf.secao_titulo("Experiência Profissional")
    for exp in dados["experiencia"]:
        pdf.set_font("Helvetica", "B", 11)
        pdf.cell(
            0, 6,
            f"{exp['cargo']} — {exp['empresa']}",
            new_x="LMARGIN", new_y="NEXT"
        )
        pdf.set_font("Helvetica", "I", 10)
        pdf.cell(
            0, 6,
            f"{exp['periodo']} | {exp['local']}",
            new_x="LMARGIN", new_y="NEXT"
        )
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 5, exp["resumo"])
        pdf.ln(3)

    # Competências
    pdf.secao_titulo("Competências Técnicas")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, f"Linguagens: {', '.join(dados['competencias']['linguagens'])}")
    pdf.multi_cell(0, 6, f"Ferramentas: {', '.join(dados['competencias']['ferramentas'])}")
    pdf.ln(4)

    # Certificados
    pdf.secao_titulo("Certificações & Formação Complementar")
    for cert in dados["certificados"]:
        pdf.set_font("Helvetica", "", 11)
        pdf.write(6, f"{cert['nome']} — {cert['instituicao']} ")
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Helvetica", "U", 11)
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
        f.write("## 🛠️ Competências\n")
        f.write(f"- **Linguagens:** {', '.join(dados['competencias']['linguagens'])}\n")
        f.write(f"- **Ferramentas:** {', '.join(dados['competencias']['ferramentas'])}\n\n")
        f.write("--- \n### 📄 Currículo Completo Atualizado\n[👉 Visualizar PDF](./curriculo_fabiano.pdf)\n\n")
        f.write("*Nota: Atualizado via Automação.*")

if __name__ == "__main__":
    info = carregar_dados()
    gerar_pdf(info)
    atualizar_readme(info)
