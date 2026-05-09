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
        self.set_text_color(0, 0, 255) # Azul para links
        self.cell(0, 6, dados["contato"]["email"], ln=True, align="C", link=f"mailto:{dados['contato']['email']}")
        self.cell(0, 6, f"LinkedIn: {dados['contato']['linkedin']}", ln=True, align="C", link=dados['contato']['linkedin'])
        self.cell(0, 6, f"GitHub: {dados['contato']['github']}", ln=True, align="C", link=dados['contato']['github'])
        
        self.set_text_color(0, 0, 0)
        self.set_font("Arial", "B", 11)
        self.cell(0, 6, f"{dados['cargo']}", ln=True, align="C")
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

    # Objetivo
    pdf.secao_titulo("Objetivo")
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, dados["objetivo"])
    pdf.ln(4)

    # Resumo
    pdf.secao_titulo("Resumo Profissional")
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, dados["sobre"])
    pdf.ln(4)

    # Formação
    pdf.secao_titulo("Formação Acadêmica")
    for ed in dados["educacao"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, ed["curso"], ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, f"{ed['instituicao']} ({ed['periodo']})", ln=True)
    pdf.ln(4)

    # Experiência
    pdf.secao_titulo("Experiência Profissional")
    for exp in dados["experiencia"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{exp['cargo']} - {exp['empresa']}", ln=True)
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 6, exp["periodo"], ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, exp["resumo"])
        pdf.ln(3)

    # Certificados
    pdf.secao_titulo("Certificados e Cursos")
    for cert in dados["certificados"]:
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, f"{cert['nome']} - {cert['instituicao']}", ln=False)
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Arial", "U", 11)
        pdf.cell(0, 6, " [Acesse aqui]", ln=True, link=cert["link"])
        pdf.set_text_color(0, 0, 0)

    pdf.output("curriculo_fabiano.pdf")

def atualizar_readme(dados):
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# {dados['nome']} 👋\n\n")
        f.write(f"### {dados['cargo']}\n\n")
        f.write(f"## 🚀 Sobre\n{dados['sobre']}\n\n")
        f.write(f"## 🛠️ Competências\n- **Linguagens:** {', '.join(dados['competencias']['linguagens'])}\n")
        f.write(f"- **Ferramentas:** {', '.join(dados['competencias']['ferramentas'])}\n\n")
        f.write(f"--- \n### 📄 Baixar Currículo em PDF\n[Clique aqui para acessar o documento atualizado](./curriculo_fabiano.pdf)\n")

if __name__ == "__main__":
    info = carregar_dados()
    gerar_pdf(info)
    atualizar_readme(info)
