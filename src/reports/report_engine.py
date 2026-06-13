from fpdf import FPDF
from fpdf.enums import XPos, YPos
from src.logic.state import InferenceState
from datetime import datetime
import os
from PIL import Image
import io

from src.utils.localization import get_text

class RadiologyReport(FPDF):
    """Base class for professional radiology PDF reports."""
    
    def __init__(self, lang: str = "English", **kwargs):
        super().__init__(**kwargs)
        self.lang = lang

    def header(self):
        """Header with branding and title."""
        # Medical Blue accent
        self.set_fill_color(0, 123, 255) 
        self.rect(0, 0, 210, 30, 'F')
        
        self.set_font('Helvetica', 'B', 20)
        self.set_text_color(255, 255, 255)
        self.cell(0, 15, get_text("report_header", self.lang), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        
        self.set_font('Helvetica', 'I', 12)
        self.cell(0, 5, get_text("report_subheader", self.lang), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
        self.ln(10)

    def footer(self):
        """Footer with page numbers and confidentiality notice."""
        self.set_y(-25)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, get_text("report_footer", self.lang), align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        page_label = get_text("report_page_label", self.lang)
        self.cell(0, 10, f'{page_label} {self.page_no()}/{{nb}}', align='C')

def generate_report(state: InferenceState, compress: bool = True) -> bytes:
    """
    Synthesizes a professional PDF report from the InferenceState.
    
    Args:
        state: The current InferenceState containing results and images.
        compress: Whether to compress the PDF content. Default is True.
        
    Returns:
        bytes: The generated PDF as a byte stream.
    """
    lang = state.language
    pdf = RadiologyReport(lang=lang)
    pdf.compress = compress
    pdf.alias_nb_pages()
    pdf.add_page()
    
    # 1. Clinical Information Header
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 123, 255)
    pdf.cell(0, 10, get_text("report_summary", lang), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_draw_color(0, 123, 255)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(50, 7, get_text("report_date", lang), border=0)
    pdf.cell(0, 7, datetime.now().strftime("%Y-%m-%d %H:%M"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(50, 7, get_text("report_filename", lang), border=0)
    pdf.cell(0, 7, state.image_metadata.get('filename', 'N/A'), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    # 2. Image and CNN Results
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 123, 255)
    pdf.cell(0, 10, get_text("report_cnn", lang), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    # Embed Image
    if state.uploaded_image:
        temp_img_path = "temp_report_img.png"
        state.uploaded_image.save(temp_img_path)
        pdf.image(temp_img_path, x=10, y=pdf.get_y(), w=60)
        # Shift cursor to the right of the image
        img_bottom = pdf.get_y() + 60
        y_start = pdf.get_y()
        
        # Classification details
        pdf.set_font('Helvetica', 'B', 11)
        pdf.set_text_color(0, 0, 0)
        
        results = state.results
        
        # Localize values for report
        plane_val = results.get('plane', 'N/A')
        seq_val = results.get('sequence', 'N/A')
        
        # If Spanish, we might want to translate these common terms if they are technical strings
        if lang == "Español":
            plane_mapping = {"axial": "axial", "sagittal": "sagital", "coronal": "coronal"}
            seq_mapping = {"flair": "flair", "t1": "t1", "t2": "t2"}
            plane_val = plane_mapping.get(str(plane_val).lower(), plane_val)
            seq_val = seq_mapping.get(str(seq_val).lower(), seq_val)

        # Format Depth
        try:
            depth_raw = float(results.get('depth', 0.0))
            # Use absolute depth for sagittal scans (symmetric hemispheres)
            if str(results.get('plane', '')).lower() == "sagittal":
                depth_raw = abs(depth_raw)
            depth_val = f"{depth_raw:.3f}"
        except (ValueError, TypeError):
            depth_val = str(results.get('depth', 'N/A'))

        pdf.set_xy(80, y_start)
        pdf.cell(50, 7, get_text("report_plane", lang), border=0)
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 7, f"{plane_val} ({results.get('plane_conf', 0)*100:.1f}%)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.set_x(80)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(50, 7, get_text("report_sequence", lang), border=0)
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 7, f"{seq_val} ({results.get('sequence_conf', 0)*100:.1f}%)", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.set_x(80)
        pdf.set_font('Helvetica', 'B', 11)
        pdf.cell(50, 7, get_text("report_depth", lang), border=0)
        pdf.set_font('Helvetica', '', 11)
        pdf.cell(0, 7, depth_val, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        pdf.set_y(max(pdf.get_y(), img_bottom) + 10)
        # Cleanup temp image
        if os.path.exists(temp_img_path):
            os.remove(temp_img_path)
    else:
        pdf.set_font('Helvetica', 'I', 10)
        pdf.cell(0, 10, 'No image available for report.', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(5)

    # 3. MedGemma Findings (VLM)
    pdf.set_font('Helvetica', 'B', 14)
    pdf.set_text_color(0, 123, 255)
    pdf.cell(0, 10, get_text("report_vlm", lang), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    
    pdf.set_font('Helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)
    pdf.multi_cell(0, 7, state.results.get('narrative', get_text("report_no_narrative", lang)), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(10)
    
    # 4. Clinical Disclaimer & Validation
    pdf.set_fill_color(245, 245, 245)
    pdf.rect(10, pdf.get_y(), 190, 45, 'F')
    pdf.set_y(pdf.get_y() + 5)
    
    pdf.set_font('Helvetica', 'B', 10)
    pdf.set_text_color(200, 0, 0)
    pdf.set_x(15)
    pdf.cell(0, 5, get_text("report_disclaimer_title", lang), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.set_text_color(0, 0, 0)
    pdf.set_x(15)
    pdf.multi_cell(180, 5, get_text("report_disclaimer_body", lang), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_x(15)
    pdf.cell(0, 10, f'{get_text("report_validated_by", lang)} ________________________________', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_x(15)
    pdf.cell(0, 10, f'{get_text("report_validation_date", lang)} ___________________________', new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return bytes(pdf.output())

def get_report_filename(state: InferenceState) -> str:
    """Generates a standardized filename for the report."""
    orig_name = state.image_metadata.get('filename', 'scan')
    base_name = os.path.splitext(orig_name)[0]
    plane = state.results.get('plane', 'unknown').lower()
    timestamp = datetime.now().strftime("%Y%m%d%H%M")
    return f"{base_name}_{plane}_{timestamp}.pdf"
