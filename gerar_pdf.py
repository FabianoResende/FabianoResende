import json
from fpdf import FPDF

def carregar_dados():
    with open("dados_curriculo.json", "r", encoding="utf-8") as f:
        return json.load(f)

def gerar_pdf(dados):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Cabeçalho
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, dados["nome"], ln=True, align="C")
    
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(0, 6, dados["contato"]["email"], ln=True, align="C", link=f"mailto:{dados['contato']['email']}")
    
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f"{dados['cargo']} | {dados['contato']['cidade']}", ln=True, align="C")
    pdf.ln(10)

    # Seção Sobre
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Resumo Profissional", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 6, dados["sobre"])
    pdf.ln(5)

    # Experiência
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Experiência", ln=True)
    for exp in dados["experiencia"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, f"{exp['empresa']} ({exp['periodo']})", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 5, exp["resumo"])
        pdf.ln(2)

    pdf.output("curriculo_fabiano.pdf")
    print("PDF 'curriculo_fabiano.pdf' gerado com sucesso!")

def atualizar_readme(dados):
    conteudo = f"""# Olá, eu sou o {dados['nome']} 👋

### {dados['cargo']}

## 🎯 Objetivo
{dados['objetivo']}

## 🚀 Sobre Mim
{dados['sobre']}

## 🛠️ Tecnologias e Competências
- **Linguagens:** {', '.join(dados['competencias']['linguagens'])}
- **Ferramentas:** {', '.join(dados['competencias']['ferramentas'])}

---
### 📄 Currículo Completo
[Clique aqui para baixar o PDF Atualizado](./curriculo_fabiano.pdf)
---
*Atualizado automaticamente via Python e GitHub Actions.*
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(conteudo)
    print("README.md atualizado com sucesso!")

if __name__ == "__main__":
    try:
        info = carregar_dados()
        gerar_pdf(info)
        atualizar_readme(info)
    except Exception as e:
        print(f"Erro na execução: {e}")
