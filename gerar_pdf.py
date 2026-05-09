from fpdf import FPDF
import json

def criar_pdf():
    # 1. Carregamento dos dados com tratamento de erro
    try:
        with open("dados_curriculo.json", "r", encoding="utf-8") as df:
            dados = json.load(df)
    except Exception as e:
        print(f"Erro ao ler o arquivo JSON: {e}")
        return

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_margins(20, 20, 20)
    pdf.add_page()

    # --- CABEÇALHO ---
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, dados["nome"], ln=True, align="C")

    # Links de contato (Azul e Clicáveis)
    pdf.set_font("Arial", "", 11)
    pdf.set_text_color(0, 0, 255)
    
    # E-mail com comando mailto
    pdf.cell(0, 6, dados['contato']['email'], ln=True, align="C", link=f"mailto:{dados['contato']['email']}")
    
    # Redes Sociais
    pdf.cell(0, 6, "LinkedIn: fabianofr", ln=True, align="C", link=dados['contato']['linkedin'])
    pdf.cell(0, 6, "GitHub: FabianoResende", ln=True, align="C", link=dados['contato']['github'])

    # Informações Complementares (Preto)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 6, f"{dados['cargo']} | {dados['contato']['cidade']}", ln=True, align="C")
    pdf.ln(10)

    largura_util = pdf.w - 2 * pdf.l_margin

    # --- FUNÇÃO AUXILIAR PARA SEÇÕES ---
    def adicionar_secao(titulo, conteudo):
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, titulo, ln=True)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(largura_util, 6, conteudo)
        pdf.ln(4)

    adicionar_secao("Objetivo", dados["objetivo"])
    adicionar_secao("Resumo Profissional", dados["sobre"])

    # --- EDUCAÇÃO ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Formação Acadêmica", ln=True)
    pdf.set_font("Arial", "", 11)
    for ed in dados["educacao"]:
        pdf.multi_cell(largura_util, 6, f"{ed['curso']} - {ed['instituicao']} ({ed['periodo']})")
    pdf.ln(4)

    # --- EXPERIÊNCIA ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Experiência Profissional", ln=True)
    for exp in dados['experiencia']:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 7, f"{exp['empresa']} | {exp['cargo']} ({exp['periodo']})", ln=True)
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(largura_util, 5, exp['resumo'])
        pdf.ln(4)

    # --- CERTIFICADOS (PASTA DRIVE) ---
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Certificados e Cursos", ln=True)
    for cert in dados["certificados"]:
        pdf.set_font("Arial", "B", 11)
        pdf.cell(0, 6, cert["nome"], ln=True)
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Arial", "U", 10)
        pdf.cell(0, 5, "Clique aqui para acessar a pasta de certificados", ln=True, link=cert["link"])
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)

    # Finalização
    nome_arquivo = "curriculo_fabiano.pdf"
    pdf.output(nome_arquivo)
    print(f"Sucesso! {nome_arquivo} gerado corretamente.")

if __name__ == "__main__":
    criar_pdf()
