import os
from fpdf import FPDF


class StudyGuidePDF(FPDF):

    def header(self):
        # Header (Only on pages after the first or on all pages)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, "Guia de Estudos - E-Commerce Sales Analyzer", border=0, align="R")
        self.ln(15)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(128, 128, 128)
        # Page number
        self.cell(0, 10, f"Página {self.page_no()}/{{nb}}", border=0, align="C")


def clean_text(text):
    # Remove emojis and characters outside latin-1
    return text.encode("latin-1", "ignore").decode("latin-1")


def parse_markdown_to_pdf(md_path, pdf_path):
    pdf = StudyGuidePDF()
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Set up basic parameters
    pdf.set_font("Helvetica", size=11)

    if not os.path.exists(md_path):
        print(f"Erro: Arquivo {md_path} não encontrado!")
        return

    with open(md_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    in_code_block = False

    for line in lines:
        stripped = line.strip()

        # Check for code blocks
        if stripped.startswith("```"):
            in_code_block = not in_code_block
            pdf.ln(2)
            continue

        if in_code_block:
            # Monospace text for code
            pdf.set_font("Courier", size=9)
            pdf.set_fill_color(245, 245, 245)
            # Replace tab/spaces for code indentation
            text_line = clean_text(line.replace("\t", "    ").rstrip("\n"))
            pdf.cell(0, 5, text_line, new_x="LMARGIN", new_y="NEXT", fill=True)
            pdf.set_font("Helvetica", size=11)  # Reset font
            continue

        # Ignore horizontal rules
        if stripped == "---":
            pdf.ln(5)
            pdf.set_draw_color(200, 200, 200)
            pdf.line(pdf.get_x(), pdf.get_y(), pdf.get_x() + 190, pdf.get_y())
            pdf.ln(5)
            continue

        # Headers
        if stripped.startswith("# "):
            pdf.ln(10)
            pdf.set_font("Helvetica", "B", 20)
            pdf.set_text_color(10, 30, 80)  # Navy blue title
            pdf.multi_cell(0, 10, clean_text(stripped[2:]), new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", size=11)
            pdf.set_text_color(0, 0, 0)  # Reset color
            pdf.ln(5)
        elif stripped.startswith("## "):
            pdf.ln(8)
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(30, 70, 130)  # Lighter blue for H2
            pdf.multi_cell(0, 8, clean_text(stripped[3:]), new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", size=11)
            pdf.set_text_color(0, 0, 0)  # Reset color
            pdf.ln(3)
        elif stripped.startswith("### "):
            pdf.ln(5)
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 6, clean_text(stripped[4:]), new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", size=11)
            pdf.ln(2)
        # Bullet points
        elif stripped.startswith("- ") or stripped.startswith("* "):
            clean_t = "  - " + clean_text(stripped[2:].replace("**", ""))
            pdf.multi_cell(0, 6, clean_t, new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        # Empty lines
        elif not stripped:
            pdf.ln(3)
        # Normal text
        else:
            # Clean simple markdown bold tags **
            clean_t = clean_text(line.replace("**", "").rstrip("\n"))
            try:
                pdf.multi_cell(0, 6, clean_t, new_x="LMARGIN", new_y="NEXT")
            except Exception as e:
                print(f"DEBUG: Failed rendering line: {repr(line)}")
                print(f"DEBUG: Current X: {pdf.get_x()}, Y: {pdf.get_y()}")
                raise e

    pdf.output(pdf_path)
    print(f"Sucesso! PDF gerado em: {pdf_path}")


if __name__ == "__main__":
    parse_markdown_to_pdf("guia_estudo.md", "guia_estudo.pdf")
