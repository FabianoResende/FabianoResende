import json
from fpdf import FPDF

# 1. Função para carregar os dados do JSON
def carregar_dados():
    with open("dados_curriculo.json", "r", encoding="utf-8") as f:
        return json.load(f)

# 2. Classe customizada para o PDF (Design e Cabeçalho)
class PDF(FPDF):
    def header_curriculo(self, dados):
        # Nome Centralizado
        self.set_font("Arial", "B", 18)
        self.cell(0, 10, dados["nome"], ln=True, align="C")
        
        # Contatos Amigáveis com Links Ativos
        self.set_font("Arial", "", 10)
        self.set_text_color(0, 0, 255) # Azul
        
        # Email clicável
        self.cell(0, 6, dados["contato"]["email"], ln=True, align="C", link=f"mailto:{dados['contato']['email']}")
        
        # LinkedIn formatado (exibe apenas o user, mas o link é o completo)
        self.cell(0, 6, "LinkedIn: /fabianofr", ln=True, align="C", link=dados["contato"]["linkedin"])
        
        # GitHub formatado
        self.cell(0, 6, "GitHub: /FabianoResende", ln=True, align="C", link=dados["contato"]["github"])
        
        # Cargo e Localização
        self.set_text_color(0, 0, 0) # Volta para preto
        self.set_font("Arial", "B", 11)
        self.cell(0, 6, dados["cargo"], ln=True, align="C")
        self.set_font("Arial", "", 10)
        self.cell(0, 6, dados["contato"]["cidade"], ln=True, align="C")
        self.ln(5)

    def secao_titulo(self, texto):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(230, 230, 230) # Fundo Cinza Claro
        self.cell(0, 8, f"  {texto}", ln=True, fill=True)
        self.ln(2)

# 3. Função para gerar o arquivo PDF
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

    # Resumo / Sobre
    pdf.secao_titulo("Resumo Profissional")
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, dados["sobre"])
    pdf.ln(4)

    # Formação Acadêmica
    pdf.secao_titulo("Formação Acadêmica")
    for ed in dados["educacao"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, ed["curso"], ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.cell(0, 6, f"{ed['instituicao']} ({ed['periodo']})", ln=True)
    pdf.ln(4)

    # Experiência Profissional
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
    print("Sucesso: PDF gerado!")

# 4. Função para atualizar o README com Badges (Escudos)
def atualizar_readme(dados):
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(f"# {dados['nome']} 👋\n\n")
        f.write(f"### {dados['cargo']}\n\n")
        
        # Badges Visuais (Hard Skills)
        f.write("![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ")
        f.write("![SQL](https://img.shields.io/badge/mysql-%2300f.svg?style=for-the-badge&logo=mysql&logoColor=white) ")
        f.write("![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)\n\n")
        
        f.write(f"## 🚀 Sobre\n{dados['sobre']}\n\n")
        f.write(f"## 🛠️ Competências\n")
        f.write(f"- **Linguagens:** {', '.join(dados['competencias']['linguagens'])}\n")
        f.write(f"- **Ferramentas:** {', '.join(dados['competencias']['ferramentas'])}\n\n")
        f.write(f"--- \n### 📄 Currículo Completo Atualizado\n")
        f.write(f"[👉 Clique aqui para visualizar o PDF gerado nesta automação](./curriculo_fabiano.pdf)\n\n")
        f.write(f"*Nota: Este README e o PDF anexo são atualizados automaticamente via Python e GitHub Actions toda vez que o arquivo JSON de dados é alterado.*")
    print("Sucesso: README atualizado!")

# Execução Principal
if __name__ == "__main__":
    try:
        conteudo = carregar_dados()
        gerar_pdf(conteudo)
        atualizar_readme(conteudo)
    except Exception as e:
        print(f"Erro no mestre: {e}")
