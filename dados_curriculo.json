from fpdf import FPDF
import json

class PDF(FPDF):
    def header_curriculo(self, dados):
        self.set_font("Helvetica", "B", 18)
        self.cell(0, 10, dados["nome"], new_x="LMARGIN", new_y="NEXT", align="C")

        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, f"E-mail: {dados['contato']['email']}", new_x="LMARGIN", new_y="NEXT", align="C", link=f"mailto:{dados['contato']['email']}")
        self.cell(0, 6, f"LinkedIn: {dados['contato']['linkedin']}", new_x="LMARGIN", new_y="NEXT", align="C", link=dados["contato"]["linkedin"])
        self.cell(0, 6, f"GitHub: {dados['contato']['github']}", new_x="LMARGIN", new_y="NEXT", align="C", link=dados["contato"]["github"])
        self.cell(0, 6, f"Portfólio: {dados['contato']['portfolio']}", new_x="LMARGIN", new_y="NEXT", align="C", link=dados["contato"]["portfolio"])
        self.ln(5)

def gerar_pdf(dados):
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # OBJETIVO
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "OBJETIVO", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, dados["objetivo"])
    pdf.ln(3)

    # PERFIL
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "PERFIL", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(0, 6, dados["perfil"])
    pdf.ln(3)

    # EXPERIÊNCIA
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "EXPERIÊNCIA", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "B", 12)
    for exp in dados["experiencia"]:
        pdf.cell(0, 8, f"{exp['cargo']} — {exp['empresa']}", new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 6, f"{exp['periodo']} | {exp['local']}", new_x="LMARGIN", new_y="NEXT")

        if "atividades" in exp:
            for item in exp["atividades"]:
                pdf.multi_cell(0, 6, f"• {item}")
        else:
            pdf.multi_cell(0, 6, exp["resumo"])

        pdf.ln(3)
        pdf.set_font("Helvetica", "B", 12)

    # COMPETÊNCIAS
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "COMPETÊNCIAS TÉCNICAS", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    comp = dados["competencias"]

    pdf.multi_cell(0, 6, f"Front-end: {', '.join(comp['front_end'])}")
    pdf.multi_cell(0, 6, f"Dados & Back-end: {', '.join(comp['dados_back_end'])}")
    pdf.multi_cell(0, 6, f"IA Aplicada: {', '.join(comp['ia_aplicada'])}")
    pdf.multi_cell(0, 6, f"Ferramentas: {', '.join(comp['ferramentas'])}")
    pdf.ln(3)

    # FORMAÇÃO
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "FORMAÇÃO", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    for form in dados["formacao"]:
        pdf.multi_cell(0, 6, f"{form['curso']} — {form['instituicao']} ({form['periodo']})")
    pdf.ln(3)

    # CERTIFICADOS
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, "CERTIFICADOS & FORMAÇÃO COMPLEMENTAR", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    for cert in dados["certificados"]:
        pdf.multi_cell(0, 6, f"{cert['nome']} — {cert['link']}", link=cert["link"])

    pdf.output("curriculo.pdf")

# Carregar JSON
with open("dados_curriculo.json", "r", encoding="utf-8") as f:
    info = json.load(f)

gerar_pdf(info)
