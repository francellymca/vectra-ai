"""
Vectra AI - Corporate PDF Generator

Converts every Markdown file in docs/source into a standardized
corporate PDF stored in docs/pdf.

Usage:
    python scripts/generate_docs.py
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path
from typing import Iterable

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = PROJECT_ROOT / "docs" / "source"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "pdf"

NAVY = colors.HexColor("#0B1F3A")
OCEAN = colors.HexColor("#0077B6")
LIGHT_BLUE = colors.HexColor("#EAF7FD")
PALE_BLUE = colors.HexColor("#F7FBFF")
TEXT = colors.HexColor("#25364D")
MUTED = colors.HexColor("#65758B")
BORDER = colors.HexColor("#B8D8F0")
WHITE = colors.white

PAGE_WIDTH, PAGE_HEIGHT = A4


def inline_markup(text: str) -> str:
    """Convert a limited Markdown subset into ReportLab paragraph markup."""
    escaped = html.escape(text.strip())
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", escaped)
    escaped = re.sub(r"`(.+?)`", r"<font name='Courier'>\1</font>", escaped)
    return escaped


def build_styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()

    return {
        "cover_code": ParagraphStyle(
            "CoverCode",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=16,
            textColor=OCEAN,
            alignment=TA_CENTER,
            spaceAfter=8,
        ),
        "cover_title": ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=31,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=14,
        ),
        "cover_meta": ParagraphStyle(
            "CoverMeta",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=10,
            leading=15,
            textColor=MUTED,
            alignment=TA_CENTER,
            spaceAfter=4,
        ),
        "h1": ParagraphStyle(
            "Heading1",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=16,
            leading=21,
            textColor=NAVY,
            spaceBefore=12,
            spaceAfter=8,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "Heading2",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=OCEAN,
            spaceBefore=10,
            spaceAfter=6,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "Heading3",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11,
            leading=15,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=5,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.5,
            leading=14.2,
            textColor=TEXT,
            alignment=TA_LEFT,
            spaceAfter=7,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.3,
            leading=13.5,
            textColor=TEXT,
            leftIndent=4,
        ),
        "table_header": ParagraphStyle(
            "TableHeader",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.5,
            leading=11,
            textColor=WHITE,
            alignment=TA_LEFT,
        ),
        "table_cell": ParagraphStyle(
            "TableCell",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.3,
            leading=11,
            textColor=TEXT,
            alignment=TA_LEFT,
        ),
    }


STYLES = build_styles()


def header_footer(canvas, doc) -> None:
    canvas.saveState()

    # Header
    canvas.setFillColor(NAVY)
    canvas.rect(0, PAGE_HEIGHT - 18 * mm, PAGE_WIDTH, 18 * mm, fill=1, stroke=0)

    canvas.setFillColor(WHITE)
    canvas.setFont("Helvetica-Bold", 10)
    canvas.drawString(18 * mm, PAGE_HEIGHT - 11.5 * mm, "VECTRA LOGISTICS")

    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(
        PAGE_WIDTH - 18 * mm,
        PAGE_HEIGHT - 11.5 * mm,
        "Corporate Knowledge Base",
    )

    # Footer
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.6)
    canvas.line(18 * mm, 15 * mm, PAGE_WIDTH - 18 * mm, 15 * mm)

    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.5)
    canvas.drawString(18 * mm, 9.5 * mm, "Vectra AI - Logistics Knowledge Management")
    canvas.drawRightString(
        PAGE_WIDTH - 18 * mm,
        9.5 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()


def create_document(output_path: Path) -> BaseDocTemplate:
    doc = BaseDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=27 * mm,
        bottomMargin=22 * mm,
        title=output_path.stem.replace("-", " ").title(),
        author="Vectra AI",
        subject="Vectra Logistics Corporate Knowledge Base",
    )

    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id="body",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    doc.addPageTemplates(
        [PageTemplate(id="corporate", frames=[frame], onPage=header_footer)]
    )
    return doc


def find_metadata(lines: list[str], key: str) -> str | None:
    prefix = f"**{key}:**"
    for line in lines[:20]:
        stripped = line.strip()
        if stripped.startswith(prefix):
            return stripped[len(prefix):].strip()
    return None


def add_cover(story: list, lines: list[str], title_line: str) -> None:
    raw_title = title_line.lstrip("#").strip()
    match = re.match(r"([A-Z]{3}-\d{3})\s+[—-]\s+(.+)", raw_title)

    if match:
        code, title = match.groups()
    else:
        code, title = "VECTRA AI", raw_title

    story.extend(
        [
            Spacer(1, 35 * mm),
            Paragraph(code, STYLES["cover_code"]),
            Paragraph(inline_markup(title), STYLES["cover_title"]),
            HRFlowable(
                width="58%",
                thickness=2,
                color=OCEAN,
                spaceBefore=5,
                spaceAfter=18,
                hAlign="CENTER",
            ),
        ]
    )

    metadata = [
        ("Empresa", find_metadata(lines, "Empresa")),
        ("Documento", find_metadata(lines, "Documento")),
        ("Versão", find_metadata(lines, "Versão")),
        ("Última atualização", find_metadata(lines, "Última atualização")),
        ("Departamento responsável", find_metadata(lines, "Departamento responsável")),
    ]

    for label, value in metadata:
        if value:
            story.append(
                Paragraph(
                    f"<b>{html.escape(label)}:</b> {inline_markup(value)}",
                    STYLES["cover_meta"],
                )
            )

    story.extend([Spacer(1, 30 * mm), HRFlowable(color=BORDER, thickness=0.8)])
    story.append(
        Paragraph(
            "Corporate document prepared for the Vectra AI knowledge base.",
            STYLES["cover_meta"],
        )
    )


def parse_table(lines: list[str]) -> Table:
    rows: list[list[str]] = []

    for line in lines:
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        rows.append(cells)

    # Remove Markdown separator row.
    if len(rows) > 1 and all(re.fullmatch(r":?-{3,}:?", c) for c in rows[1]):
        rows.pop(1)

    max_cols = max(len(row) for row in rows)
    normalized = [row + [""] * (max_cols - len(row)) for row in rows]

    converted = []
    for row_index, row in enumerate(normalized):
        style = STYLES["table_header"] if row_index == 0 else STYLES["table_cell"]
        converted.append([Paragraph(inline_markup(cell), style) for cell in row])

    available = PAGE_WIDTH - (36 * mm)
    col_widths = [available / max_cols] * max_cols

    table = Table(converted, colWidths=col_widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), NAVY),
                ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
                ("BACKGROUND", (0, 1), (-1, -1), PALE_BLUE),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE_BLUE]),
            ]
        )
    )
    return table


def flush_paragraph(buffer: list[str], story: list) -> None:
    if not buffer:
        return

    text = " ".join(part.strip() for part in buffer if part.strip())
    if text:
        story.append(Paragraph(inline_markup(text), STYLES["body"]))
    buffer.clear()


def flush_list(items: list[str], ordered: bool, story: list) -> None:
    if not items:
        return

    list_items = [
        ListItem(Paragraph(inline_markup(item), STYLES["bullet"]))
        for item in items
    ]
    story.append(
        ListFlowable(
            list_items,
            bulletType="1" if ordered else "bullet",
            start="1",
            leftIndent=16,
            bulletFontName="Helvetica",
            bulletFontSize=8,
            bulletColor=OCEAN,
            spaceAfter=7,
        )
    )
    items.clear()


def markdown_to_story(markdown_text: str) -> list:
    lines = markdown_text.splitlines()
    story: list = []

    first_heading_index = next(
        (i for i, line in enumerate(lines) if line.startswith("# ")),
        None,
    )

    if first_heading_index is not None:
        add_cover(story, lines, lines[first_heading_index])
        lines = lines[first_heading_index + 1:]

    paragraph_buffer: list[str] = []
    list_items: list[str] = []
    list_is_ordered = False
    i = 0

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        # Table detection
        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph(paragraph_buffer, story)
            flush_list(list_items, list_is_ordered, story)
            table_lines = []
            while i < len(lines):
                candidate = lines[i].strip()
                if not (candidate.startswith("|") and candidate.endswith("|")):
                    break
                table_lines.append(candidate)
                i += 1
            story.extend([parse_table(table_lines), Spacer(1, 8)])
            continue

        bullet_match = re.match(r"^[-*]\s+(.+)$", stripped)
        ordered_match = re.match(r"^\d+\.\s+(.+)$", stripped)

        if bullet_match or ordered_match:
            flush_paragraph(paragraph_buffer, story)
            current_ordered = bool(ordered_match)
            if list_items and current_ordered != list_is_ordered:
                flush_list(list_items, list_is_ordered, story)
            list_is_ordered = current_ordered
            list_items.append(
                (ordered_match or bullet_match).group(1)
            )
            i += 1
            continue
        else:
            flush_list(list_items, list_is_ordered, story)

        if not stripped:
            flush_paragraph(paragraph_buffer, story)
            i += 1
            continue

        if stripped == "---":
            flush_paragraph(paragraph_buffer, story)
            story.append(
                HRFlowable(
                    width="100%",
                    thickness=0.6,
                    color=BORDER,
                    spaceBefore=4,
                    spaceAfter=9,
                )
            )
            i += 1
            continue

        heading_match = re.match(r"^(#{1,3})\s+(.+)$", stripped)
        if heading_match:
            flush_paragraph(paragraph_buffer, story)
            level = len(heading_match.group(1))
            text = inline_markup(heading_match.group(2))
            style = STYLES[{1: "h1", 2: "h2", 3: "h3"}[level]]
            story.append(Paragraph(text, style))
            i += 1
            continue

        # Skip metadata block because it is displayed on the cover.
        if re.match(
            r"^\*\*(Empresa|Documento|Versão|Última atualização|Departamento responsável):\*\*",
            stripped,
        ):
            i += 1
            continue

        paragraph_buffer.append(stripped)
        i += 1

    flush_paragraph(paragraph_buffer, story)
    flush_list(list_items, list_is_ordered, story)
    return story


def markdown_files() -> Iterable[Path]:
    return sorted(SOURCE_DIR.glob("*.md"))


def generate_pdf(source_path: Path, output_path: Path) -> None:
    markdown_text = source_path.read_text(encoding="utf-8")
    story = markdown_to_story(markdown_text)
    doc = create_document(output_path)
    doc.build(story)


def main() -> int:
    if not SOURCE_DIR.exists():
        print(f"ERROR: source directory not found: {SOURCE_DIR}", file=sys.stderr)
        return 1

    files = list(markdown_files())
    if not files:
        print(f"ERROR: no Markdown files found in {SOURCE_DIR}", file=sys.stderr)
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("Generating Vectra Logistics PDFs...\n")
    generated = 0

    for source_path in files:
        output_path = OUTPUT_DIR / f"{source_path.stem}.pdf"
        try:
            generate_pdf(source_path, output_path)
            print(f"[OK] {output_path.relative_to(PROJECT_ROOT)}")
            generated += 1
        except Exception as exc:
            print(f"[ERROR] {source_path.name}: {exc}", file=sys.stderr)
            return 1

    print(f"\nCompleted: {generated} PDF file(s) generated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())