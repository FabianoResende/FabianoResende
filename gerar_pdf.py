from fpdf import FPDF


class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 20)
        self.set_text_color(33, 37, 41)
        self.cell(0, 15, "FABIANO FARIA DE RESENDE", ln=True, align="C")
        self.set_font("helvetica", "I", 11)
        self.cell(0, 5, "Sistemas de Informacao | Transicao para TI | Automacao & Dados", ln=True, align="C")
        self.ln(10)

    def secao_titulo(self, titulo):
        self.set_font("helvetica", "B", 13)
        self.set_fill_color(240, 240, 240)
        self.cell(0, 8, f"  {titulo}", ln=True, fill=True)
        self.ln(3)


def criar_curriculo():
    pdf = PDF()
    pdf.add_page()

    # --- CONTATO ---
    pdf.set_font("helvetica", "", 10)
    contato = "Sao Goncalo, RJ | fabianofariaderesende@gmail.com | linkedin.com/in/fabianofr"
    pdf.cell(0, 5, contato, ln=True, align="C")
    pdf.ln(10)

    # --- SOBRE ---
    pdf.secao_titulo("RESUMO PROFISSIONAL")
    pdf.set_font("helvetica", "", 11)
    sobre = ("Estudante de Sistemas de Informacao (4o periodo) na Estacio. Profissional com solida "
             "experiencia administrativa e operacional, agora migrando para a area de Tecnologia. "
             "Foco em desenvolvimento Python, bancos de dados e automacao de processos.")
    pdf.multi_cell(0, 6, sobre)
    pdf.ln(5)

    # --- EXPERIENCIA ---
    pdf.secao_titulo("EXPERIENCIA PROFISSIONAL")
    pdf.set_font("helvetica", "B", 11)
    pdf.cell(0, 6, "Indigo Estacionamento - Operador de Patio VI", ln=True)
    pdf.set_font("helvetica", "I", 10)
    pdf.cell(0, 6, "2016 - 2019", ln=True)
    pdf.set_font("helvetica", "", 11)
    desc = ("Suporte tecnico N1 em terminais de autoatendimento. Administracao de sistemas WA e WPS. "
            "Gestao financeira, tesouraria e faturamento diario.")
    pdf.multi_cell(0, 6, desc)
    pdf.ln(5)

    # --- COMPETENCIAS ---
    pdf.secao_titulo("COMPETENCIAS TECNICAS")
    pdf.set_font("helvetica", "", 11)
    pdf.cell(0, 6, "- Linguagens: Python 3.10, Excel VBA, HTML/CSS", ln=True)
    pdf.cell(0, 6, "- Ferramentas: Git, GitHub, PyCharm, AWS Cloud", ln=True)
    pdf.cell(0, 6, "- Outros: Banco de Dados (SQL), LGPD, Manutencao de Sistemas", ln=True)

    pdf.output("curriculo_fabiano.pdf")
    print("Versao Premium gerada com sucesso!")


if __name__ == "__main__":
    criar_curriculo()