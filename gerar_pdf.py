# -*- coding: utf-8 -*-
"""
Gera o currículo PDF oficial a partir de dados_curriculo.json.

Arquivo de entrada:
    dados_curriculo.json

Arquivo de saída:
    curriculo_fabiano.pdf

Requisitos:
    Python 3.10+
    fpdf2
    DejaVuSans.ttf na raiz do repositório
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from fpdf import FPDF
from fpdf.enums import Align, XPos, YPos


# ============================================================
# CAMINHOS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_FILE = BASE_DIR / "dados_curriculo.json"
FONT_FILE = BASE_DIR / "DejaVuSans.ttf"
OUTPUT_FILE = BASE_DIR / "curriculo_fabiano.pdf"


# ============================================================
# LINK OFICIAL DOS CERTIFICADOS
# Somente o título "CERTIFICADOS E CURSOS" será clicável.
# ============================================================

DRIVE_CERTIFICADOS = (
    "https://drive.google.com/drive/folders/"
    "1qsDa6bGyc49aoh98x7J0JtX6ToiAs6WM?usp=drive_link"
)


# ============================================================
# CONFIGURAÇÕES DO PDF
# ============================================================

MARGIN_LEFT = 18
MARGIN_RIGHT = 18
MARGIN_TOP = 15
MARGIN_BOTTOM = 16

BODY_SIZE = 9.5
BODY_LINE = 4.6

SECTION_SIZE = 10.5

TITLE_SIZE = 17
SUBTITLE_SIZE = 11
CONTACT_SIZE = 8.5


# ============================================================
# CLASSE PRINCIPAL DO PDF
# ============================================================

class CurriculumPDF(FPDF):
    """
    Layout profissional e estável do currículo.
    """

    def __init__(self) -> None:
        super().__init__(
            orientation="P",
            unit="mm",
            format="A4",
        )

        self.set_margins(
            MARGIN_LEFT,
            MARGIN_TOP,
            MARGIN_RIGHT,
        )

        self.set_auto_page_break(
            auto=True,
            margin=MARGIN_BOTTOM,
        )

        self.set_compression(True)

        self._font_registered = False

    # --------------------------------------------------------
    # Fonte Unicode
    # --------------------------------------------------------

    def register_font(self) -> None:
        """
        Registra DejaVuSans.ttf.

        IMPORTANTE:
        fpdf2 atual não utiliza mais uni=True.
        """

        if self._font_registered:
            return

        if not FONT_FILE.is_file():
            raise FileNotFoundError(
                f"Fonte obrigatória não encontrada: {FONT_FILE}"
            )

        # Fonte normal
        self.add_font(
            "DejaVu",
            style="",
            fname=str(FONT_FILE),
        )

        # Usa o mesmo TTF para permitir estilo B
        # sem exigir outro arquivo na raiz.
        self.add_font(
            "DejaVu",
            style="B",
            fname=str(FONT_FILE),
        )

        self._font_registered = True

    # --------------------------------------------------------
    # Header automático desativado
    # --------------------------------------------------------

    def header(self) -> None:
        """
        O cabeçalho do currículo é construído manualmente.
        """
        pass

    # --------------------------------------------------------
    # Footer
    # --------------------------------------------------------

    def footer(self) -> None:
        self.set_y(-10)

        self.set_font(
            "DejaVu",
            size=7.5,
        )

        self.set_text_color(
            120,
            120,
            120,
        )

        self.cell(
            0,
            5,
            text=f"Fabiano Faria de Resende  |  Página {self.page_no()}",
            align=Align.C,
        )

        self.set_text_color(
            0,
            0,
            0,
        )

    # --------------------------------------------------------
    # Título das seções
    # --------------------------------------------------------

    def section_title(
        self,
        text: str,
    ) -> None:

        self.set_font(
            "DejaVu",
            style="B",
            size=SECTION_SIZE,
        )

        self.set_text_color(
            30,
            30,
            30,
        )

        # IMPORTANTE:
        # Sempre reposiciona o cursor no início.
        self.set_x(self.l_margin)

        self.cell(
            self.epw,
            6,
            text=text,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

        # Linha divisória
        self.set_draw_color(
            185,
            185,
            185,
        )

        self.line(
            self.l_margin,
            self.get_y(),
            self.w - self.r_margin,
            self.get_y(),
        )

        self.ln(2.5)

    # --------------------------------------------------------
    # Texto normal
    # --------------------------------------------------------

    def body(
        self,
        text: str,
        *,
        size: float = BODY_SIZE,
        line: float = BODY_LINE,
    ) -> None:

        if not text:
            return

        self.set_font(
            "DejaVu",
            size=size,
        )

        self.set_text_color(
            35,
            35,
            35,
        )

        # Garante posição correta antes de multi_cell.
        self.set_x(self.l_margin)

        self.multi_cell(
            self.epw,
            line,
            text=text,
            align=Align.L,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

    # --------------------------------------------------------
    # Bullet
    # --------------------------------------------------------

    def bullet(
        self,
        text: str,
    ) -> None:

        if not text:
            return

        self.set_font(
            "DejaVu",
            size=BODY_SIZE,
        )

        self.set_text_color(
            35,
            35,
            35,
        )

        self.set_x(self.l_margin)

        self.multi_cell(
            self.epw,
            BODY_LINE,
            text=f"• {text}",
            align=Align.L,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )


# ============================================================
# LEITURA DO JSON
# ============================================================

def load_data() -> dict[str, Any]:

    with DATA_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError(
            "dados_curriculo.json deve conter um objeto JSON."
        )

    return data


# ============================================================
# NORMALIZAÇÃO DE URL
# ============================================================

def clean_url(
    value: str,
) -> str:

    value = (value or "").strip()

    # Corrige especificamente o erro:
    # https\://
    if value.startswith("https\\://"):
        value = value.replace(
            "https\\://",
            "https://",
            1,
        )

    return value


# ============================================================
# CABEÇALHO
# ============================================================

def add_header(
    pdf: CurriculumPDF,
    data: dict[str, Any],
) -> None:

    contato = data.get(
        "contato",
        {},
    ) or {}

    # --------------------------------------------------------
    # Nome
    # --------------------------------------------------------

    pdf.set_font(
        "DejaVu",
        style="B",
        size=TITLE_SIZE,
    )

    pdf.set_text_color(
        20,
        20,
        20,
    )

    pdf.cell(
        pdf.epw,
        8,
        text=str(
            data.get(
                "nome",
                "",
            )
        ),
        align=Align.C,
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    # --------------------------------------------------------
    # Cargo
    # --------------------------------------------------------

    pdf.set_font(
        "DejaVu",
        style="B",
        size=SUBTITLE_SIZE,
    )

    pdf.cell(
        pdf.epw,
        6,
        text=str(
            data.get(
                "cargo",
                "",
            )
        ),
        align=Align.C,
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    pdf.ln(1.5)

    # --------------------------------------------------------
    # Contatos
    # --------------------------------------------------------

    cidade = str(
        contato.get(
            "cidade",
            "",
        )
    ).strip()

    email = str(
        contato.get(
            "email",
            "",
        )
    ).strip()

    linkedin = clean_url(
        str(
            contato.get(
                "linkedin",
                "",
            )
        )
    )

    github = clean_url(
        str(
            contato.get(
                "github",
                "",
            )
        )
    )

    site = clean_url(
        str(
            contato.get(
                "site",
                "",
            )
        )
    )

    # --------------------------------------------------------
    # Linha principal de contato
    # --------------------------------------------------------

    pdf.set_font(
        "DejaVu",
        size=CONTACT_SIZE,
    )

    pdf.set_text_color(
        70,
        70,
        70,
    )

    pdf.set_x(
        pdf.l_margin
    )

    parts = []

    if cidade:
        parts.append(
            (
                cidade,
                None,
            )
        )

    if email:
        parts.append(
            (
                email,
                f"mailto:{email}",
            )
        )

    if linkedin:
        parts.append(
            (
                "linkedin.com/in/fabianofr",
                linkedin,
            )
        )

    if github:
        parts.append(
            (
                "github.com/FabianoResende",
                github,
            )
        )

    for index, (
        label,
        link,
    ) in enumerate(parts):

        if index:
            pdf.write(
                text="  |  "
            )

        if link:

            pdf.set_text_color(
                35,
                90,
                150,
            )

            pdf.write(
                text=label,
                link=link,
            )

            pdf.set_text_color(
                70,
                70,
                70,
            )

        else:

            pdf.write(
                text=label
            )

    pdf.ln(4.5)

    # --------------------------------------------------------
    # Portfolio
    # --------------------------------------------------------

    if site:

        pdf.set_text_color(
            35,
            90,
            150,
        )

        pdf.cell(
            pdf.epw,
            5,
            text=(
                "fabianoresende.github.io/"
                "landing-page-html-css-js/"
            ),
            align=Align.C,
            link=site,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

        pdf.set_text_color(
            0,
            0,
            0,
        )

    pdf.ln(5)


# ============================================================
# FORMAÇÃO
# ============================================================

def add_education(
    pdf: CurriculumPDF,
    data: dict[str, Any],
) -> None:

    pdf.section_title(
        "FORMAÇÃO ACADÊMICA"
    )

    for item in data.get(
        "educacao",
        [],
    ) or []:

        curso = str(
            item.get(
                "curso",
                "",
            )
        ).strip()

        instituicao = str(
            item.get(
                "instituicao",
                "",
            )
        ).strip()

        periodo = str(
            item.get(
                "periodo",
                "",
            )
        ).strip()

        # Curso + instituição
        if curso or instituicao:

            linha = curso

            if instituicao:

                if linha:
                    linha += (
                        f" | {instituicao}"
                    )
                else:
                    linha = instituicao

            pdf.set_font(
                "DejaVu",
                style="B",
                size=BODY_SIZE,
            )

            pdf.set_text_color(
                35,
                35,
                35,
            )

            pdf.set_x(
                pdf.l_margin
            )

            pdf.multi_cell(
                pdf.epw,
                BODY_LINE,
                text=linha,
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )

        # Período
        if periodo:
            pdf.body(
                periodo
            )

        pdf.ln(1.5)


# ============================================================
# COMPETÊNCIAS
# ============================================================

def add_competencies(
    pdf: CurriculumPDF,
    data: dict[str, Any],
) -> None:

    pdf.section_title(
        "COMPETÊNCIAS TÉCNICAS"
    )

    comp = data.get(
        "competencias",
        {},
    ) or {}

    groups = [
        (
            "Front-end",
            comp.get(
                "linguagens",
                [],
            ),
        ),
        (
            "Dados & Back-end",
            comp.get(
                "dados_back_end",
                [],
            ),
        ),
        (
            "IA Aplicada",
            comp.get(
                "ia_aplicada",
                [],
            ),
        ),
        (
            "Controle de Versão",
            [
                "Git",
                "GitHub",
            ],
        ),
    ]

    for label, values in groups:

        values = [
            str(value).strip()
            for value in (
                values or []
            )
            if str(value).strip()
        ]

        if not values:
            continue

        pdf.set_font(
            "DejaVu",
            style="B",
            size=BODY_SIZE,
        )

        pdf.set_text_color(
            35,
            35,
            35,
        )

        pdf.set_x(
            pdf.l_margin
        )

        pdf.write(
            text=f"{label}: "
        )

        pdf.set_font(
            "DejaVu",
            size=BODY_SIZE,
        )

        pdf.write(
            text=", ".join(values)
        )

        pdf.ln(4.8)

    pdf.ln(1)


# ============================================================
# PROJETOS
# ============================================================

def add_projects(
    pdf: CurriculumPDF,
    data: dict[str, Any],
) -> None:

    pdf.section_title(
        "PROJETOS PRÁTICOS E PORTFÓLIO"
    )

    for exp in data.get(
        "experiencia",
        [],
    ) or []:

        empresa = str(
            exp.get(
                "empresa",
                "",
            )
        ).strip()

        if empresa.lower() != "flyrank ai":
            continue

        # ----------------------------------------------------
        # Nome do programa
        # ----------------------------------------------------

        pdf.set_font(
            "DejaVu",
            style="B",
            size=BODY_SIZE,
        )

        pdf.set_text_color(
            35,
            35,
            35,
        )

        pdf.multi_cell(
            pdf.epw,
            BODY_LINE,
            text=(
                "Programa Prático de Engenharia "
                "Front-end com IA | FlyRank AI"
            ),
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

        # ----------------------------------------------------
        # Período
        # ----------------------------------------------------

        periodo = str(
            exp.get(
                "periodo",
                "",
            )
        ).strip()

        if periodo:

            pdf.set_font(
                "DejaVu",
                size=BODY_SIZE,
            )

            pdf.multi_cell(
                pdf.epw,
                BODY_LINE,
                text=periodo,
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT,
            )

        # ----------------------------------------------------
        # Descrição
        # ----------------------------------------------------

        pdf.body(
            "Desenvolvimento de projetos reais integrando "
            "tecnologias web, APIs e ferramentas de IA "
            "durante trilha prática de formação."
        )

        # ----------------------------------------------------
        # Projetos aprovados
        # ----------------------------------------------------

        bullets = [
            (
                "Capstone FE-04: Plataforma de Suporte "
                "Técnico com IA (Next.js, TypeScript e "
                "Claude Code)."
            ),
            (
                "FL-04 Study Notes Pipeline: NotebookLM "
                "+ Claude, com cerca de 3 horas economizadas "
                "por ciclo em 5 execuções reais."
            ),
            (
                "Chatbot Front-end com IA: HTML, CSS e "
                "JavaScript com integração de API de IA."
            ),
            (
                "Gerenciador de Senhas: Python + SQLite "
                "com operações CRUD e armazenamento "
                "criptografado."
            ),
            (
                "Landing Page Responsiva: HTML, CSS e "
                "JavaScript."
            ),
        ]

        for item in bullets:
            pdf.bullet(item)

        pdf.ln(2)

        return


# ============================================================
# EXPERIÊNCIA PROFISSIONAL
# ============================================================

def add_experience(
    pdf: CurriculumPDF,
    data: dict[str, Any],
) -> None:

    pdf.section_title(
        "EXPERIÊNCIA PROFISSIONAL"
    )

    for exp in data.get(
        "experiencia",
        [],
    ) or []:

        empresa = str(
            exp.get(
                "empresa",
                "",
            )
        ).strip()

        # FlyRank já está em Projetos.
        if empresa.lower() == "flyrank ai":
            continue

        cargo = str(
            exp.get(
                "cargo",
                "",
            )
        ).strip()

        periodo = str(
            exp.get(
                "periodo",
                "",
            )
        ).strip()

        resumo = str(
            exp.get(
                "resumo",
                "",
            )
        ).strip()

        # ----------------------------------------------------
        # Cargo | Empresa
        # ----------------------------------------------------

        linha = cargo

        if empresa:

            if linha:
                linha += (
                    f" | {empresa}"
                )
            else:
                linha = empresa

        pdf.set_font(
            "DejaVu",
            style="B",
            size=BODY_SIZE,
        )

        pdf.set_text_color(
            35,
            35,
            35,
        )

        pdf.multi_cell(
            pdf.epw,
            BODY_LINE,
            text=linha,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT,
        )

        # ----------------------------------------------------
        # Período
        # ----------------------------------------------------

        if periodo:
            pdf.body(
                periodo
            )

        # ----------------------------------------------------
        # Resumo em bullets
        # ----------------------------------------------------

        if resumo:

            partes = [
                part.strip()
                for part in resumo.split(". ")
                if part.strip()
            ]

            for item in partes:

                if not item.endswith("."):
                    item += "."

                pdf.bullet(
                    item
                )

        # ----------------------------------------------------
        # Fechamento oficial da experiência Indigo
        # ----------------------------------------------------

        if empresa.lower() == "indigo estacionamento":

            pdf.body(
                "Consolidei nessa experiência habilidades "
                "iniciais em suporte a sistemas e análise "
                "de dados operacionais, competências que "
                "hoje aplico na transição para Tecnologia."
            )

        pdf.ln(1.5)


# ============================================================
# CERTIFICADOS
# ============================================================

def add_certificates(
    pdf: CurriculumPDF,
    data: dict[str, Any],
) -> None:

    # ========================================================
    # IMPORTANTE:
    # SOMENTE O TÍTULO É CLICÁVEL.
    # OS CURSOS INDIVIDUAIS NÃO POSSUEM LINK.
    # ========================================================

    pdf.set_font(
        "DejaVu",
        style="B",
        size=SECTION_SIZE,
    )

    pdf.set_text_color(
        35,
        90,
        150,
    )

    pdf.set_x(
        pdf.l_margin
    )

    pdf.cell(
        pdf.epw,
        6,
        text="CERTIFICADOS E CURSOS",
        link=DRIVE_CERTIFICADOS,
        new_x=XPos.LMARGIN,
        new_y=YPos.NEXT,
    )

    pdf.set_draw_color(
        185,
        185,
        185,
    )

    pdf.line(
        pdf.l_margin,
        pdf.get_y(),
        pdf.w - pdf.r_margin,
        pdf.get_y(),
    )

    pdf.set_text_color(
        35,
        35,
        35,
    )

    pdf.ln(2.5)

    # --------------------------------------------------------
    # Lista sem hyperlinks individuais
    # --------------------------------------------------------

    for cert in data.get(
        "certificados",
        [],
    ) or []:

        nome = str(
            cert.get(
                "nome",
                "",
            )
        ).strip()

        instituicao = str(
            cert.get(
                "instituicao",
                "",
            )
        ).strip()

        ano = str(
            cert.get(
                "ano",
                "",
            )
        ).strip()

        if not nome:
            continue

        linha = nome

        if instituicao:
            linha += (
                f", {instituicao}"
            )

        if ano:
            linha += (
                f" ({ano})"
            )

        pdf.bullet(
            linha
        )


# ============================================================
# GERAÇÃO
# ============================================================

def generate_pdf(
    data: dict[str, Any],
) -> None:

    pdf = CurriculumPDF()

    pdf.register_font()

    pdf.add_page()

    # ========================================================
    # ORDEM OFICIAL APROVADA
    # ========================================================

    # 1. Cabeçalho
    add_header(
        pdf,
        data,
    )

    # 2. Objetivo
    pdf.section_title(
        "OBJETIVO"
    )

    pdf.body(
        str(
            data.get(
                "objetivo",
                "",
            )
        ).strip()
    )

    pdf.ln(2)

    # 3. Perfil
    pdf.section_title(
        "PERFIL"
    )

    pdf.body(
        str(
            data.get(
                "sobre",
                "",
            )
        ).strip()
    )

    pdf.ln(2)

    # 4. Formação
    add_education(
        pdf,
        data,
    )

    # 5. Competências
    add_competencies(
        pdf,
        data,
    )

    # 6. Projetos
    add_projects(
        pdf,
        data,
    )

    # 7. Experiência
    add_experience(
        pdf,
        data,
    )

    # 8. Certificados
    add_certificates(
        pdf,
        data,
    )

    # ========================================================
    # SAÍDA
    # ========================================================

    pdf.output(
        str(OUTPUT_FILE)
    )

    print(
        f"PDF gerado com sucesso: {OUTPUT_FILE}"
    )


# ============================================================
# MAIN
# ============================================================

def main() -> None:

    data = load_data()

    generate_pdf(
        data
    )


if __name__ == "__main__":
    main()
