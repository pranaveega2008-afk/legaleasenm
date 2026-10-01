"""
pdf_exporter.py - PDF Document Generator for LegalEase
Generates beautifully formatted, printable PDF documents from legal text.
Includes automatic font detection for Unicode / Tamil characters on Windows.
"""

import io
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def register_best_font():
    """
    Attempts to register a Unicode-capable font from the system.
    Falls back gracefully to Helvetica if no system font is found.
    """
    font_name = "Helvetica"
    font_bold = "Helvetica-Bold"

    candidate_fonts = [
        # Nirmala UI (Default Windows Indic/Tamil font)
        ("NirmalaUI", "C:/Windows/Fonts/Nirmala.ttc", 0),
        ("NirmalaUI-Bold", "C:/Windows/Fonts/NirmalaB.ttc", 0),
        # Arial
        ("CustomArial", "C:/Windows/Fonts/arial.ttf", None),
        ("CustomArial-Bold", "C:/Windows/Fonts/arialbd.ttf", None),
        # Latha (Old Windows Tamil)
        ("Latha", "C:/Windows/Fonts/latha.ttf", None),
    ]

    for name, path, subindex in candidate_fonts:
        if os.path.exists(path):
            try:
                if subindex is not None:
                    pdfmetrics.registerFont(TTFont(name, path, subfontIndex=subindex))
                else:
                    pdfmetrics.registerFont(TTFont(name, path))

                if "Bold" in name:
                    font_bold = name
                else:
                    font_name = name
            except Exception:
                pass

    return font_name, font_bold


def create_pdf_from_text(title: str, text_content: str, language: str = "en") -> io.BytesIO:
    """
    Creates a styled PDF document from legal text.
    Returns an in-memory BytesIO buffer ready for download.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    base_font, bold_font = register_best_font()

    # Custom styles
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'LegalDocTitle',
        parent=styles['Normal'],
        fontName=bold_font,
        fontSize=15,
        leading=19,
        textColor=colors.HexColor('#0f172a'),
        alignment=1,  # Center
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'LegalDocSubtitle',
        parent=styles['Normal'],
        fontName=base_font,
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor('#64748b'),
        alignment=1,  # Center
        spaceAfter=12
    )

    heading_style = ParagraphStyle(
        'LegalSectionHeading',
        parent=styles['Normal'],
        fontName=bold_font,
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor('#1e293b'),
        spaceBefore=8,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'LegalBodyText',
        parent=styles['Normal'],
        fontName=base_font,
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )

    signature_style = ParagraphStyle(
        'LegalSignature',
        parent=styles['Normal'],
        fontName=base_font,
        fontSize=9,
        leading=12,
        textColor=colors.HexColor('#475569')
    )

    elements = []

    # Title & Header
    elements.append(Paragraph(title.upper(), title_style))
    elements.append(Paragraph("LEGALEASE AI • FORMALLY GENERATED LEGAL INSTRUMENT", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#cbd5e1'), spaceBefore=2, spaceAfter=14))

    # Parse lines
    lines = text_content.split("\n")
    skip_header = False

    for line in lines:
        stripped = line.strip()

        # Skip decorative separators
        if stripped.startswith("===") or stripped.startswith("---"):
            continue

        if stripped.lower() == title.lower() and not skip_header:
            skip_header = True
            continue

        if not stripped:
            elements.append(Spacer(1, 5))
            continue

        # Check for headings
        is_heading = (
            (stripped.isupper() and len(stripped) > 3 and not stripped.startswith("_"))
            or stripped.startswith("விதிமுறைகள்")
            or stripped.startswith("முக்கிய விதிமுறைகள்")
            or stripped.startswith("TERMS AND CONDITIONS")
            or stripped.startswith("RECITALS:")
            or stripped.startswith("SIGNATURES:")
            or stripped.startswith("கையொப்பங்கள்:")
        )

        safe_text = stripped.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        if is_heading:
            elements.append(Paragraph(safe_text, heading_style))
        elif "____" in stripped:
            elements.append(Paragraph(safe_text, signature_style))
        else:
            elements.append(Paragraph(safe_text, body_style))

    # Footer note
    elements.append(Spacer(1, 20))
    elements.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor('#e2e8f0'), spaceBefore=10, spaceAfter=8))
    elements.append(
        Paragraph(
            "<i>Note: This document was drafted using LegalEase. Please review local statutory and stamp duty requirements before final execution.</i>",
            ParagraphStyle(
                'Disclaimer',
                fontName=base_font,
                fontSize=7.5,
                leading=10,
                textColor=colors.HexColor('#94a3b8'),
                alignment=1
            )
        )
    )

    # Build PDF into memory buffer
    doc.build(elements)
    buffer.seek(0)
    return buffer
