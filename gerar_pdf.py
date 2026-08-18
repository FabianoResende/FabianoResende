# -*- coding: utf-8 -*-

import json
from pathlib import Path

from fpdf import FPDF


BASE_DIR = Path(__file__).resolve().parent

DADOS_FILE = BASE_DIR / "dados_curriculo.json"
PDF_FILE = BASE_DIR / "curriculo_fabiano.pdf"
FONT_FILE = BASE_DIR / "DejaVuSans.ttf"


class CurriculoPDF(FPDF):
    """PDF profissional do currículo."""

    def __init__(self):
        super().__init__(
            orientation="P",
            unit="mm",
            format="A4"
        )

        self.set_auto_page_break(
            auto=True,
            margin=15
        )

        self.set_margins(
            left=15,
            top=15,
            right=15
        )

        self.registrar_fonte()

    def registrar_fonte(self):
        """Registra a fonte Unicode DejaVu Sans."""

        if not FONT_FILE.exists():
            raise FileNotFoundError(
                f"Fonte não encontrada: {FONT_FILE}"
            )

        # O repositório contém a versão regular.
        # Registramos o mesmo TTF para permitir estilos
        # usados pelo documento sem depender das fontes
        # adicionais no repositório.
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

        self.default_font = "DejaVu"

    def footer(self):
        """Rodapé com número da página."""

        self.set_y(-10)

        self.set_font(
            self.default_font,
            "",
            8
        )

        self.set_text_color(
            110,
            110,
            110
        )

        self.cell(
            0,
            5,
            f"Fabiano Faria de Resende | Página {self.page_no()}",
            align="C"
        )

        self.set_text_color(
            0,
            0,
            0
        )

    def titulo_secao(
        self,
        texto,
        link=None
    ):
        """Cria título de seção."""

        largura = self.w - self.l_margin - self.r_margin

        self.set_fill_color(
            238,
            240,
            243
        )

        self.set_text_color(
            30,
            30,
            30
        )

        self.set_font(
            self.default_font,
            "B",
            11
        )

        self.cell(
            largura,
            8,
            f"  {texto}",
            fill=True,
            link=link
        )

        self.ln(5)

    def texto(
        self,
        texto,
        tamanho=10,
        altura=5,
        estilo=""
    ):
        """Escreve texto com quebra automática."""

        if not texto:
            return

        self.set_font(
            self.default_font,
            estilo,
            tamanho
        )

        self.set_text_color(
            0,
            0,
            0
        )

        self.multi_cell(
            0,
            altura,
            str(texto)
        )

    def link_inline(
        self,
        texto,
        link
    ):
        """Escreve um link clicável."""

        if not texto or not link:
            return

        self.set_text_color(
            0,
            82,
            155
        )

        self.set_font(
            self.default_font,
            "",
            9
        )

        self.write(
            5,
            texto,
            link
        )

        self.set_text_color(
            0,
            0,
            0
        )


def carregar_dados():
    """Carrega dados do currículo."""

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


def adicionar_cabecalho(pdf, dados):
    """Adiciona cabeçalho profissional."""

    nome = dados.get(
        "nome",
        "Nome"
    )

    cargo = dados.get(
        "cargo",
        ""
    )

    contato = dados.get(
        "contato",
        {}
    )

    email = contato.get(
        "email",
        ""
    )

    linkedin = contato.get(
        "linkedin",
        ""
    )

    github = contato.get(
        "github",
        ""
    )

    site = contato.get(
        "site",
        ""
    )

    cidade = contato.get(
        "cidade",
        ""
    )

    # Nome
    pdf.set_font(
        pdf.default_font,
        "B",
        20
    )

    pdf.set_text_color(
        25,
        25,
        25
    )

    pdf.cell(
        0,
        10,
        nome,
        align="C"
    )

    pdf.ln(8)

    # Cargo
    if cargo:
        pdf.set_font(
            pdf.default_font,
            "",
            11
        )

        pdf.set_text_color(
            70,
            70,
            70
        )

        pdf.cell(
            0,
            6,
            cargo,
            align="C"
        )

        pdf.ln(7)

    # Links
    links = []

    if email:
        links.append(
            ("E-mail", f"mailto:{email}")
        )

    if linkedin:
        links.append(
            ("LinkedIn", linkedin)
        )

    if github:
        links.append(
            ("GitHub", github)
        )

    if site:
        links.append(
            ("Portfólio", site)
        )

    if links:
        pdf.set_font(
            pdf.default_font,
            "",
            9
        )

        pdf.set_text_color(
            0,
            82,
            155
        )

        largura = pdf.w - pdf.l_margin - pdf.r_margin

        texto_links = "  |  ".join(
            item[0]
            for item in links
        )

        pdf.cell(
            largura,
            5,
            texto_links,
            align="C"
        )

        # Criamos os links individualmente
        # sobre os textos correspondentes.
        x_inicio = pdf.l_margin

        largura_total = pdf.get_string_width(
            texto_links
        )

        x_inicio = (
            pdf.w - largura_total
        ) / 2

        x_atual = x_inicio

        for index, (texto, url) in enumerate(links):

            largura_texto = pdf.get_string_width(
                texto
            )

            pdf.link(
                x_atual,
                pdf.get_y(),
                largura_texto,
                5,
                url
            )

            x_atual += largura_texto

            if index < len(links) - 1:
                separador = "  |  "

                x_atual += pdf.get_string_width(
                    separador
                )

        pdf.set_text_color(
            0,
            0,
            0
        )

        pdf.ln(6)

    # Cidade
    if cidade:
        pdf.set_font(
            pdf.default_font,
            "",
            9
        )

        pdf.set_text_color(
            90,
            90,
            90
        )

        pdf.cell(
            0,
            5,
            cidade,
            align="C"
        )

        pdf.set_text_color(
            0,
            0,
            0
        )

        pdf.ln(8)


def adicionar_experiencia(
    pdf,
    experiencia
):
    """Adiciona experiência profissional."""

    for item in experiencia:

        empresa = item.get(
            "empresa",
            ""
        )

        cargo = item.get(
            "cargo",
            ""
        )

        periodo = item.get(
            "periodo",
            ""
        )

        resumo = item.get(
            "resumo",
            ""
        )

        if empresa:
            pdf.set_font(
                pdf.default_font,
                "B",
                11
            )

            pdf.multi_cell(
                0,
                5,
                empresa
            )

        if cargo:
            pdf.set_font(
                pdf.default_font,
                "B",
                10
            )

            pdf.multi_cell(
                0,
                5,
                cargo
            )

        if periodo:
            pdf.set_font(
                pdf.default_font,
                "I",
                9
            )

            pdf.set_text_color(
                90,
                90,
                90
            )

            pdf.multi_cell(
                0,
                5,
                periodo
            )

            pdf.set_text_color(
                0,
                0,
                0
            )

        if resumo:
            pdf.set_font(
                pdf.default_font,
                "",
                9
            )

            pdf.multi_cell(
                0,
                4.8,
                resumo
            )

        pdf.ln(2)


def adicionar_formacao(
    pdf,
    educacao
):
    """Adiciona formação acadêmica."""

    for item in educacao:

        curso = item.get(
            "curso",
            ""
        )

        instituicao = item.get(
            "instituicao",
            ""
        )

        periodo = item.get(
            "periodo",
            ""
        )

        if curso:
            pdf.set_font(
                pdf.default_font,
                "B",
                10
            )

            pdf.multi_cell(
                0,
                5,
                curso
            )

        if instituicao:
            pdf.set_font(
                pdf.default_font,
                "",
                9
            )

            pdf.multi_cell(
                0,
                5,
                instituicao
            )

        if periodo:
            pdf.set_font(
                pdf.default_font,
                "I",
                9
            )

            pdf.set_text_color(
                90,
                90,
                90
            )

            pdf.multi_cell(
                0,
                5,
                periodo
            )

            pdf.set_text_color(
                0,
                0,
                0
            )

        pdf.ln(2)


def adicionar_competencias(
    pdf,
    competencias
):
    """Adiciona competências técnicas."""

    grupos = [
        (
            "Front-end",
            competencias.get(
                "front_end",
                []
            )
        ),
        (
            "Back-end e Dados",
            competencias.get(
                "back_end_dados",
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

        pdf.set_font(
            pdf.default_font,
            "B",
            9.5
        )

        pdf.cell(
            42,
            5,
            f"{titulo}:"
        )

        pdf.set_font(
            pdf.default_font,
            "",
            9.5
        )

        pdf.multi_cell(
            0,
            5,
            ", ".join(
                str(item)
                for item in itens
            )
        )

        pdf.ln(1)


def adicionar_certificados(
    pdf,
    dados
):
    """Adiciona certificados e link do Google Drive."""

    certificados = dados.get(
        "certificados",
        []
    )

    contato = dados.get(
        "contato",
        {}
    )

    drive_link = contato.get(
        "certificados",
        ""
    )

    if drive_link:
        pdf.set_font(
            pdf.default_font,
            "",
            9
        )

        pdf.set_text_color(
            0,
            82,
            155
        )

        pdf.cell(
            0,
            5,
            "Acessar certificados e cursos no Google Drive",
            link=drive_link
        )

        pdf.set_text_color(
            0,
            0,
            0
        )

        pdf.ln(7)

    for certificado in certificados:

        nome = certificado.get(
            "nome",
            ""
        ).strip()

        instituicao = certificado.get(
            "instituicao",
            ""
        ).strip()

        ano = certificado.get(
            "ano",
            ""
        ).strip()

        if not nome:
            continue

        texto = nome

        if instituicao:
            texto += f" — {instituicao}"

        if ano:
            texto += f" ({ano})"

        pdf.set_font(
            pdf.default_font,
            "",
            9.5
        )

        pdf.multi_cell(
            0,
            5,
            f"• {texto}"
        )

        pdf.ln(1)


def gerar_pdf(dados):
    """Gera o currículo em PDF."""

    pdf = CurriculoPDF()

    pdf.add_page()

    adicionar_cabecalho(
        pdf,
        dados
    )

    # ---------------------------------------------------------
    # OBJETIVO
    # ---------------------------------------------------------

    objetivo = dados.get(
        "objetivo",
        ""
    )

    if objetivo:
        pdf.titulo_secao(
            "OBJETIVO"
        )

        pdf.texto(
            objetivo,
            tamanho=9.5,
            altura=5
        )

        pdf.ln(3)

    # ---------------------------------------------------------
    # PERFIL
    # ---------------------------------------------------------

    sobre = dados.get(
        "sobre",
        ""
    )

    if sobre:
        pdf.titulo_secao(
            "PERFIL PROFISSIONAL"
        )

        pdf.texto(
            sobre,
            tamanho=9.5,
            altura=5
        )

        pdf.ln(3)

    # ---------------------------------------------------------
    # EXPERIÊNCIA
    # ---------------------------------------------------------

    experiencia = dados.get(
        "experiencia",
        []
    )

    if experiencia:
        pdf.titulo_secao(
            "EXPERIÊNCIA PROFISSIONAL"
        )

        adicionar_experiencia(
            pdf,
            experiencia
        )

    # ---------------------------------------------------------
    # FORMAÇÃO
    # ---------------------------------------------------------

    educacao = dados.get(
        "educacao",
        []
    )

    if educacao:
        pdf.titulo_secao(
            "FORMAÇÃO ACADÊMICA"
        )

        adicionar_formacao(
            pdf,
            educacao
        )

    # ---------------------------------------------------------
    # COMPETÊNCIAS
    # ---------------------------------------------------------

    competencias = dados.get(
        "competencias",
        {}
    )

    if competencias:
        pdf.titulo_secao(
            "COMPETÊNCIAS TÉCNICAS"
        )

        adicionar_competencias(
            pdf,
            competencias
        )

        pdf.ln(3)

    # ---------------------------------------------------------
    # CERTIFICADOS
    # ---------------------------------------------------------

    certificados = dados.get(
        "certificados",
        []
    )

    contato = dados.get(
        "contato",
        {}
    )

    drive_link = contato.get(
        "certificados",
        ""
    )

    if certificados or drive_link:
        pdf.titulo_secao(
            "CERTIFICADOS E CURSOS",
            link=drive_link if drive_link else None
        )

        adicionar_certificados(
            pdf,
            dados
        )

    # ---------------------------------------------------------
    # SAÍDA
    # ---------------------------------------------------------

    pdf.output(
        str(PDF_FILE)
    )

    print(
        f"PDF gerado com sucesso: {PDF_FILE}"
    )


def main():
    dados = carregar_dados()
    gerar_pdf(dados)


if __name__ == "__main__":
    main()
