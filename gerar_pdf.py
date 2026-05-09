import json
from fpdf import FPDF

def carregar_dados():
    with open("dados_curriculo.json", "r", encoding="utf-8") as f:
        return json.load(f)

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Nome
    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 10, dados["nome"], ln=True, align="C")
    
    # Contatos com Links
    pdf.set_font("Arial", "", 10)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(0, 6, dados["contato"]["email"], ln=True, align="C", link=f"mailto:{dados['contato']['email']}")
    pdf.cell(0, 6, "LinkedIn", ln=True, align="C", link=dados["contato"]["linkedin"])
    pdf.cell(0, 6, "GitHub", ln=True, align="C", link=dados["contato"]["github"])
    
    # Localização e Cargo
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", "B", 11)
    pdf.cell(0, 6, f"{dados['cargo']}", ln=True, align="C")
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f"{dados['contato']['cidade']}", ln=True, align="C")
    pdf.ln(5)

    # Função para títulos
    def titulo(texto):
        pdf.set_font("Arial", "B", 12)
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(0, 8, texto, ln=True, fill=True)
        pdf.ln(2)

    titulo("Objetivo")
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 6, dados["objetivo"], ln=True)
    pdf.ln(4)

    titulo("Resumo Profissional")
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, dados["sobre"])
    pdf.ln(4)

    titulo("Formação Acadêmica")
    for ed in dados["educacao"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, ed["curso"], ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, f"{ed['instituicao']} ({ed['periodo']})", ln=True)
    pdf.ln(4)

    titulo("Experiência Profissional")
    for exp in dados["experiencia"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{exp['cargo']} - {exp['empresa']}", ln=True)
        pdf.set_font("Arial", "I", 10)
        pdf.cell(0, 6, exp["periodo"], ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, exp["resumo"])
        pdf.ln(3)

    titulo("Certificados e Cursos")
    for cert in dados["certificados"]:
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, f"{cert['nome']} - {cert['instituicao']}", ln=False)
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Arial", "U", 11)
        pdf.cell(0, 6, " [Ver Pasta]", ln=True, link=cert["link"])
        pdf.set_text_color(0, 0, 0)

    pdf.output("curriculo_fabiano.pdf")

def atualizar_readme(dados):
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# Olá, eu sou o {dados['nome']} 👋\n\n")
        f.write(f"### {dados['cargo']}\n\n")
        f.write(f"## 🚀 Resumo\n{dados['sobre']}\n\n")
        f.write(f"## 🛠️ Competências\n- **Linguagens:** {', '.join(dados['competencias']['linguagens'])}\n")
        f.write(f"- **Ferramentas:** {', '.join(dados['competencias']['ferramentas'])}\n\n")
        f.write(f"--- \n### 📄 Baixar Currículo\n[👉 Clique aqui para baixar o PDF atualizado](./curriculo_fabiano.pdf)\n")

if __name__ == "__main__":
    info = carregar_dados()
    gerar_pdf(info)
    atualizar_readme(info)
