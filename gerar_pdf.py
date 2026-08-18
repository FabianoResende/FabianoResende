# -*- coding: utf-8 -*-

import json
import re
from pathlib import Path

from fpdf import FPDF


# ============================================================
# CONFIGURAÇÃO
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DADOS_FILE = BASE_DIR / "dados_curriculo.json"
PDF_FILE = BASE_DIR / "curriculo_fabiano.pdf"
FONT_FILE = BASE_DIR / "DejaVuSans.ttf"


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def carregar_dados():
    """Carrega os dados do currículo."""

    if not DADOS_FILE.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {DADOS_FILE}"
        )

    with DADOS_FILE.open(
        "r",
        encoding="utf-8"
    ) as arquivo:
        dados = json.load(arquivo)

    if not isinstance(dados, dict):
        raise ValueError(
            "dados_curriculo.json deve conter um objeto JSON."
        )

    return dados


def normalizar_url(url):
    """
    Corrige URLs que eventualmente tenham sido salvas como:
    https\://...
    """

    if not isinstance(url, str):
        return ""

    url = url.strip()

    url = re.sub(
        r"\\(?=://)",
        "",
        url
    )

    return url


# ============================================================
# CLASSE PDF
# ============================================================

class CurriculoPDF(FPDF):

    def __init__(self):
        super().__init__(
            orientation="P",
            unit="mm",
            format="A4"
        )

        self.set_margins(
            left=15,
            top=14,
            right=15
        )

        self.set_auto_page_break(
            auto=True,
            margin=14
        )

        self.registrar_fontes()

    # --------------------------------------------------------
    # PROPRIEDADES
    # --------------------------------------------------------

    @property
    def largura_util(self):
        return (
            self.w
            - self.l_margin
            - self.r_margin
        )

    # --------------------------------------------------------
    # FONTES
    # --------------------------------------------------------

    def registrar_fontes(self):

        if not FONT_FILE.exists():
            raise FileNotFoundError(
                f"Fonte não encontrada: {FONT_FILE}"
            )

        self.add_font(
            "DejaVu",
            "",
            str(FONT_FILE)
        )

        self.add_font(
            "DejaVu",
            "B",
            str(FONT_FILE)
        )

        self.add_font(
            "DejaVu",
            "I",
            str(FONT_FILE)
        )

        self.add_font(
            "DejaVu",
            "BI",
            str(FONT_FILE)
        )

    # --------------------------------------------------------
    # POSICIONAMENTO
    # --------------------------------------------------------

    def resetar_x(self):
        """
        Sempre volta o cursor para a margem esquerda.

        Isso evita o erro:
        Not enough horizontal space to render a single character
        """

        self.set_x(self.l_margin)

    # --------------------------------------------------------
    # TEXTO
    # --------------------------------------------------------

    def escrever_texto(
        self,
        texto,
        tamanho=9.5,
        altura=4.8,
        estilo=""
    ):

        if texto is None:
            return

        texto = str(texto).strip()

        if not texto:
            return

        self.resetar_x()

        self.set_font(
            "DejaVu",
            estilo,
            tamanho
        )

        self.set_text_color(
            35,
            35,
            35
        )

        self.multi_cell(
            self.largura_util,
            altura,
            texto
        )

    # --------------------------------------------------------
    # SEÇÃO
    # --------------------------------------------------------

    def secao(self, titulo):

        # Evita deixar um título isolado no final da página.
        if self.get_y() > self.h - 32:
            self.add_page()

        self.resetar_x()

        self.set_fill_color(
            240,
            242,
            245
        )

        self.set_text_color(
            35,
            35,
            35
        )

        self.set_font(
            "DejaVu",
            "B",
            10.5
        )

        self.cell(
            self.largura_util,
            7,
            titulo,
            fill=True
        )

        self.ln(4)

    # --------------------------------------------------------
    # RODAPÉ
    # --------------------------------------------------------

    def footer(self):

        self.set_y(-9)

        self.set_font(
            "DejaVu",
            "",
            7.5
        )

        self.set_text_color(
            120,
            120,
            120
        )

        self.cell(
            self.largura_util,
            4,
            f"Fabiano Faria de Resende  |  Página {self.page_no()}",
            align="C"
        )

        self.set_text_color(
            0,
            0,
            0
        )


# ============================================================
# CABEÇALHO
# ============================================================

def adicionar_cabecalho(pdf, dados):

    contato = dados.get(
        "contato",
        {}
    )

    nome = dados.get(
        "nome",
        ""
    )

    cargo = dados.get(
        "cargo",
        ""
    )

    foco = dados.get(
        "foco",
        ""
    )

    cidade = contato.get(
        "cidade",
        ""
    )

    email = contato.get(
        "email",
        ""
    )

    linkedin = normalizar_url(
        contato.get(
            "linkedin",
            ""
        )
    )

    github = normalizar_url(
        contato.get(
            "github",
            ""
        )
    )

    site = normalizar_url(
        contato.get(
            "site",
            ""
        )
    )

    # --------------------------------------------------------
    # NOME
    # --------------------------------------------------------

    pdf.resetar_x()

    pdf.set_font(
        "DejaVu",
        "B",
        19
    )

    pdf.set_text_color(
        25,
        25,
        25
    )

    pdf.cell(
        pdf.largura_util,
        9,
        nome,
        align="C"
    )

    pdf.ln(6)

    # --------------------------------------------------------
    # FOCO
    # --------------------------------------------------------

    if foco:

        pdf.resetar_x()

        pdf.set_font(
            "DejaVu",
            "",
            9
        )

        pdf.set_text_color(
            90,
            90,
            90
        )

        pdf.cell(
            pdf.largura_util,
            5,
            foco,
            align="C"
        )

        pdf.ln(5)

    # --------------------------------------------------------
    # CARGO
    # --------------------------------------------------------

    if cargo:

        pdf.resetar_x()

        pdf.set_font(
            "DejaVu",
            "B",
            10.5
        )

        pdf.set_text_color(
            45,
            45,
            45
        )

        pdf.cell(
            pdf.largura_util,
            5,
            cargo,
            align="C"
        )

        pdf.ln(6)

    # --------------------------------------------------------
    # LINKS
    # --------------------------------------------------------

    links = []

    if email:
        links.append(
            (
                "E-mail",
                f"mailto:{email}"
            )
        )

    if linkedin:
        links.append(
            (
                "LinkedIn",
                linkedin
            )
        )

    if github:
        links.append(
            (
                "GitHub",
                github
            )
        )

    if site:
        links.append(
            (
                "Portfólio",
                site
            )
        )

    if links:

        pdf.set_font(
            "DejaVu",
            "",
            8.5
        )

        # Calcula largura total
        textos = []

        for indice, (rotulo, _) in enumerate(links):

            if indice > 0:
                textos.append("  |  ")

            textos.append(rotulo)

        texto_total = "".join(textos)

        largura_total = pdf.get_string_width(
            texto_total
        )

        x = (
            pdf.w
            - largura_total
        ) / 2

        y = pdf.get_y()

        pdf.set_xy(
            x,
            y
        )

        for indice, (rotulo, url) in enumerate(links):

            if indice > 0:

                pdf.set_text_color(
                    120,
                    120,
                    120
                )

                pdf.write(
                    5,
                    "  |  "
                )

            pdf.set_text_color(
                0,
                82,
                155
            )

            pdf.write(
                5,
                rotulo,
                url
            )

        pdf.set_text_color(
            0,
            0,
            0
        )

        pdf.set_y(
            y + 5
        )

    # --------------------------------------------------------
    # CIDADE
    # --------------------------------------------------------

    if cidade:

        pdf.resetar_x()

        pdf.set_font(
            "DejaVu",
            "",
            8.5
        )

        pdf.set_text_color(
            100,
            100,
            100
        )

        pdf.cell(
            pdf.largura_util,
            5,
            cidade,
            align="C"
        )

        pdf.set_text_color(
            0,
            0,
            0
        )

        pdf.ln(7)

    # Linha divisória

    pdf.set_draw_color(
        205,
        205,
        205
    )

    pdf.line(
        pdf.l_margin,
        pdf.get_y(),
        pdf.w - pdf.r_margin,
        pdf.get_y()
    )

    pdf.ln(6)


# ============================================================
# EXPERIÊNCIA
# ============================================================

def adicionar_experiencia(
    pdf,
    experiencias
):

    for experiencia in experiencias:

        empresa = experiencia.get(
            "empresa",
            ""
        )

        cargo = experiencia.get(
            "cargo",
            ""
        )

        periodo = experiencia.get(
            "periodo",
            ""
        )

        resumo = experiencia.get(
            "resumo",
            ""
        )

        # Empresa

        if empresa:

            pdf.resetar_x()

            pdf.set_font(
                "DejaVu",
                "B",
                10
            )

            pdf.set_text_color(
                30,
                30,
                30
            )

            pdf.multi_cell(
                pdf.largura_util,
                5,
                empresa
            )

        # Cargo

        if cargo:

            pdf.resetar_x()

            pdf.set_font(
                "DejaVu",
                "B",
                9.3
            )

            pdf.multi_cell(
                pdf.largura_util,
                4.8,
                cargo
            )

        # Período

        if periodo:

            pdf.resetar_x()

            pdf.set_font(
                "DejaVu",
                "I",
                8.5
            )

            pdf.set_text_color(
                100,
                100,
                100
            )

            pdf.multi_cell(
                pdf.largura_util,
                4.5,
                periodo
            )

            pdf.set_text_color(
                35,
                35,
                35
            )

        # Resumo

        if resumo:

            pdf.escrever_texto(
                resumo,
                tamanho=9,
                altura=4.7
            )

        pdf.ln(3)


# ============================================================
# FORMAÇÃO
# ============================================================

def adicionar_formacao(
    pdf,
    educacao
):

    for formacao in educacao:

        curso = formacao.get(
            "curso",
            ""
        )

        instituicao = formacao.get(
            "instituicao",
            ""
        )

        periodo = formacao.get(
            "periodo",
            ""
        )

        if curso:

            pdf.resetar_x()

            pdf.set_font(
                "DejaVu",
                "B",
                9.5
            )

            pdf.multi_cell(
                pdf.largura_util,
                4.8,
                curso
            )

        if instituicao:

            pdf.resetar_x()

            pdf.set_font(
                "DejaVu",
                "",
                9
            )

            pdf.multi_cell(
                pdf.largura_util,
                4.7,
                instituicao
            )

        if periodo:

            pdf.resetar_x()

            pdf.set_font(
                "DejaVu",
                "I",
                8.5
            )

            pdf.set_text_color(
                100,
                100,
                100
            )

            pdf.multi_cell(
                pdf.largura_util,
                4.5,
                periodo
            )

            pdf.set_text_color(
                35,
                35,
                35
            )

        pdf.ln(2)


# ============================================================
# COMPETÊNCIAS
# ============================================================

def adicionar_competencias(
    pdf,
    competencias
):

    grupos = [
        (
            "Front-end",
            competencias.get(
                "linguagens",
                []
            )
        ),
        (
            "Back-end e Dados",
            competencias.get(
                "dados_back_end",
                []
            )
        ),
        (
            "IA Aplicada",
            competencias.get(
                "ia_aplicada",
                []
            )
        ),
        (
            "Ferramentas",
            competencias.get(
                "ferramentas",
                []
            )
        )
    ]

    for titulo, itens in grupos:

        if not itens:
            continue

        texto = (
            f"{titulo}: "
            + ", ".join(
                str(item)
                for item in itens
            )
        )

        pdf.resetar_x()

        pdf.set_font(
            "DejaVu",
            "",
            9
        )

        pdf.set_text_color(
            35,
            35,
            35
        )

        pdf.multi_cell(
            pdf.largura_util,
            4.7,
            texto
        )

        pdf.ln(1)


# ============================================================
# CERTIFICADOS
# ============================================================

def adicionar_certificados(
    pdf,
    certificados
):

    for certificado in certificados:

        nome = certificado.get(
            "nome",
            ""
        ).strip()

        instituicao = certificado.get(
            "instituicao",
            ""
        ).strip()

        link = normalizar_url(
            certificado.get(
                "link",
                ""
            )
        )

        if not nome:
            continue

        texto = f"• {nome}"

        if instituicao:
            texto += f" — {instituicao}"

        pdf.resetar_x()

        pdf.set_font(
            "DejaVu",
            "",
            9
        )

        if link:

            pdf.set_text_color(
                0,
                82,
                155
            )

            pdf.write(
                4.8,
                texto,
                link
            )

        else:

            pdf.set_text_color(
                35,
                35,
                35
            )

            pdf.multi_cell(
                pdf.largura_util,
                4.8,
                texto
            )

        pdf.set_text_color(
            35,
            35,
            35
        )

        pdf.ln(2)


# ============================================================
# GERAÇÃO DO PDF
# ============================================================

def gerar_pdf(dados):

    pdf = CurriculoPDF()

    pdf.add_page()

    # --------------------------------------------------------
    # CABEÇALHO
    # --------------------------------------------------------

    adicionar_cabecalho(
        pdf,
        dados
    )

    # --------------------------------------------------------
    # OBJETIVO
    # --------------------------------------------------------

    objetivo = dados.get(
        "objetivo",
        ""
    )

    if objetivo:

        pdf.secao(
            "OBJETIVO"
        )

        pdf.escrever_texto(
            objetivo
        )

        pdf.ln(2)

    # --------------------------------------------------------
    # PERFIL
    # --------------------------------------------------------

    sobre = dados.get(
        "sobre",
        ""
    )

    if sobre:

        pdf.secao(
            "PERFIL PROFISSIONAL"
        )

        pdf.escrever_texto(
            sobre
        )

        pdf.ln(2)

    # --------------------------------------------------------
    # EXPERIÊNCIA
    # --------------------------------------------------------

    experiencias = dados.get(
        "experiencia",
        []
    )

    if experiencias:

        pdf.secao(
            "EXPERIÊNCIA PROFISSIONAL"
        )

        adicionar_experiencia(
            pdf,
            experiencias
        )

    # --------------------------------------------------------
    # FORMAÇÃO
    # --------------------------------------------------------

    educacao = dados.get(
        "educacao",
        []
    )

    if educacao:

        pdf.secao(
            "FORMAÇÃO ACADÊMICA"
        )

        adicionar_formacao(
            pdf,
            educacao
        )

    # --------------------------------------------------------
    # COMPETÊNCIAS
    # --------------------------------------------------------

    competencias = dados.get(
        "competencias",
        {}
    )

    if competencias:

        pdf.secao(
            "COMPETÊNCIAS TÉCNICAS"
        )

        adicionar_competencias(
            pdf,
            competencias
        )

        pdf.ln(2)

    # --------------------------------------------------------
    # CERTIFICADOS
    # --------------------------------------------------------

    certificados = dados.get(
        "certificados",
        []
    )

    if certificados:

        pdf.secao(
            "CERTIFICADOS E CURSOS"
        )

        adicionar_certificados(
            pdf,
            certificados
        )

    # --------------------------------------------------------
    # SALVAR
    # --------------------------------------------------------

    pdf.output(
        str(PDF_FILE)
    )

    print(
        f"PDF gerado com sucesso: {PDF_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

def main():

    dados = carregar_dados()

    gerar_pdf(
        dados
    )


if __name__ == "__main__":
    main()
