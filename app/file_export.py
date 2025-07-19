# app/file_export.py
import os
from docx import Document

class ProposalExporter:
    @staticmethod
    def export_pdf(content: str, filename: str, output_dir: str) -> str:
        """
        Exports the proposal content as a PDF.
        This is a placeholder. PDF generation is complex and often requires external libraries or services.
        For a simple solution, you might consider converting markdown to HTML and then using a library
        like WeasyPrint or a headless browser (e.g., Playwright/Puppeteer) to print to PDF.
        """
        filepath = os.path.join(output_dir, filename)
        # Dummy PDF creation - in a real app, this would involve a PDF library
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(f"PDF content for:\n\n{content}")
        print(f"Dummy PDF saved to {filepath}")
        return filepath

    @staticmethod
    def export_docx(content: str, filename: str, output_dir: str) -> str:
        """
        Exports the proposal content as a DOCX file.
        Requires 'python-docx' library.
        """
        filepath = os.path.join(output_dir, filename)
        document = Document()
        # Basic parsing: split by lines and add as paragraphs
        for line in content.split('\n'):
            if line.strip().startswith('#'): # Simple heading detection
                if line.strip().startswith('###'):
                    document.add_heading(line.replace('#','').strip(), level=3)
                elif line.strip().startswith('##'):
                    document.add_heading(line.replace('#','').strip(), level=2)
                else:
                    document.add_heading(line.replace('#','').strip(), level=1)
            elif line.strip(): # Avoid adding empty paragraphs
                document.add_paragraph(line.strip())
        document.save(filepath)
        return filepath

    @staticmethod
    def export_markdown(content: str, filename: str, output_dir: str) -> str:
        """
        Exports the proposal content as a Markdown (.md) file.
        """
        filepath = os.path.join(output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return filepath