import json
from fpdf import FPDF

def carregar_dados():
    with open("dados_curriculo.json", "r", encoding="utf-8") as f:
        return json.load(f)

class PDF(FPDF):
    def header_curriculo(self, dados):
        # Nome
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, dados["nome"], new_x="LMARGIN", new_y="NEXT", align="C")

        # Contatos
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
            f"Portfólio: {dados['contato']['portfolio']}",
            new_x="LMARGIN", new_y="NEXT",
            align="C",
            link=dados["contato"]["portfolio"]
        )

        self.set_text_color(0, 0, 0)

        # Cargo
        self.set_font("Helvetica", "B", 11)
        self.cell(
            0, 6,
            dados["cargo"],
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

    # OBJETIVO
    pdf.secao_titulo("OBJETIVO")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, dados["objetivo"])
    pdf.ln(4)

    # PERFIL
    pdf.secao_titulo("PERFIL")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, dados["perfil"])
    pdf.ln(4)

    # EXPERIÊNCIA
    pdf.secao_titulo("EXPERIÊNCIA")
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

        if "atividades" in exp:
            for item in exp["atividades"]:
                pdf.multi_cell(0, 5, f"• {item}")
        else:
            pdf.multi_cell(0, 5, exp["resumo"])

        pdf.ln(3)

    # COMPETÊNCIAS TÉCNICAS
    pdf.secao_titulo("COMPETÊNCIAS TÉCNICAS")
    pdf.set_font("Helvetica", "", 11)
    comp = dados["competencias"]
    pdf.multi_cell(0, 6, f"Front-end: {', '.join(comp['front_end'])}")
    pdf.multi_cell(0, 6, f"Dados & Back-end: {', '.join(comp['dados_back_end'])}")
    pdf.multi_cell(0, 6, f"IA Aplicada: {', '.join(comp['ia_aplicada'])}")
    pdf.multi_cell(0, 6, f"Ferramentas & Controle de Versão: {', '.join(comp['ferramentas'])}")
    pdf.ln(4)

    # FORMAÇÃO
    pdf.secao_titulo("FORMAÇÃO")
    pdf.set_font("Helvetica", "", 11)
    for form in dados["formacao"]:
        pdf.multi_cell(0, 6, f"{form['curso']} — {form['instituicao']} ({form['periodo']})")
    pdf.ln(3)

    # CERTIFICAÇÕES & FORMAÇÃO COMPLEMENTAR
    pdf.secao_titulo("CERTIFICAÇÕES & FORMAÇÃO COMPLEMENTAR")
    pdf.set_font("Helvetica", "", 11)
    for cert in dados["certificados"]:
        pdf.write(6, cert["nome"] + " ")
        pdf.set_text_color(0, 0, 255)
        pdf.set_font("Helvetica", "U", 11)
        pdf.write(6, "[Acesse a pasta aqui]", cert["link"])
        pdf.set_text_color(0, 0, 0)
        pdf.ln(8)

    pdf.output("curriculo_fabiano.pdf")

if __name__ == "__main__":
    info = carregar_dados()
    gerar_pdf(info)
