"""
Utility for loading custom CSS styles for the NeuroGemma application.
Follows the 'Relieved' aesthetic with Medical Blue accents.
"""

from src.logic.state import PipelineStage
from src.utils.localization import get_text

def render_breadcrumbs(stage: PipelineStage, lang: str = "English") -> str:
    """
    Render the breadcrumb HTML based on the current pipeline stage.
    
    Args:
        stage: The current PipelineStage to highlight.
        lang: The language to use for labels.
        
    Returns:
        A string of HTML representing the breadcrumbs.
    """
    stages = [
        ("ID", get_text("stage_id", lang)),
        ("GATE", get_text("stage_gate", lang)),
        ("SYNTHESIS", get_text("stage_synthesis", lang)),
        ("COMPLETE", get_text("stage_complete", lang))
    ]
    current_stage_val = stage.value
    
    stage_order = {"ID": 0, "GATE": 1, "SYNTHESIS": 2, "COMPLETE": 3}
    current_idx = stage_order.get(current_stage_val, 0)
    
    breadcrumb_html = '<div class="breadcrumb-container">'
    for s_val, s_label in stages:
        is_active = (s_val == current_stage_val)
        is_done = (stage_order[s_val] < current_idx)
        
        class_name = "breadcrumb-step"
        if is_active:
            class_name += " active"
        elif is_done:
            class_name += " done"
            
        breadcrumb_html += f'<div class="{class_name}">{s_label}</div>'
    breadcrumb_html += '</div>'
    return breadcrumb_html

def load_custom_css(lang: str = "English") -> str:
    """
    Returns a string of custom CSS for Streamlit.
    Follows the 'Relieved' aesthetic with Medical Blue accents.
    Primary colors:
    - Clinical Blue: #007BFF
    - Dark Contrast: #2C3E50
    - Light Background: #F8F9FA
    - Success Green: #28A745
    """
    browse_text = get_text("browse_files", lang)
    drag_drop_text = get_text("drag_drop", lang)
    limit_text = get_text("limit_info", lang)
    fullscreen_text = get_text("ui_fullscreen", lang)

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

        /* Internal Widget Translation (st.file_uploader) */
        [data-testid="stFileUploadDropzone"] button {{
            font-size: 0 !important;
        }}
        [data-testid="stFileUploadDropzone"] button::after {{
            content: "{browse_text}";
            font-size: 16px;
        }}
        [data-testid="stFileUploadDropzone"] section > div > div > span {{
            display: none !important;
        }}
        [data-testid="stFileUploadDropzone"] section > div > div::before {{
            content: "{drag_drop_text}";
        }}
        [data-testid="stFileUploadDropzone"] section > div > div > small {{
            display: none !important;
        }}
        [data-testid="stFileUploadDropzone"] section > div > div::after {{
            content: "{limit_text}";
            font-size: 0.8em;
        }}

        /* Localize Image Fullscreen Button */
        [data-testid="stImageHoverToolbar"] button {{
            width: auto !important;
            padding-right: 10px !important;
        }}
        [data-testid="stImageHoverToolbar"] button::after {{
            content: "{fullscreen_text}";
            margin-left: 5px;
            font-size: 14px;
        }}

        /* Global Spacing & Typography */
        html, body, [data-testid="stAppViewContainer"] {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #F8F9FA;
        }}

        .block-container {{
            padding: 2rem !important;
            max-width: 100% !important;
        }}

        /* Sidebar Styling */
        [data-testid="stSidebar"] {{
            background-color: #F8F9FA;
            border-right: 1px solid #E9ECEF;
            padding: 2rem 1rem;
        }}
        
        .sidebar-header {{
            color: #2C3E50;
            font-size: 1.4rem;
            font-weight: 600;
            margin-bottom: 1.5rem;
            border-bottom: 2px solid #007BFF;
            padding-bottom: 0.5rem;
        }}

        /* Tabs Styling */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 2rem;
            background-color: transparent;
        }}

        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            white-space: pre-wrap;
            background-color: transparent;
            border-radius: 4px 4px 0px 0px;
            gap: 1rem;
            font-weight: 500;
            color: #2C3E50;
        }}

        .stTabs [aria-selected="true"] {{
            background-color: transparent !important;
            border-bottom: 3px solid #007BFF !important;
            color: #007BFF !important;
        }}

        /* Diagnostic Result Cards */
        .result-card {{
            background-color: #FFFFFF;
            border: 1px solid #E9ECEF;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            margin-bottom: 1rem;
            transition: all 0.2s ease;
        }}

        .result-card.plane {{ border-left: 4px solid #007BFF; }}
        .result-card.sequence {{ border-left: 4px solid #6C757D; }}
        .result-card.depth {{ border-left: 4px solid #17A2B8; }}
        .result-card.error {{ border-left: 4px solid #DC3545; background-color: #FFF5F5; }}

        .result-label {{
            color: #6C757D;
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05rem;
            margin-bottom: 0.5rem;
        }}

        .status-badge {{
            font-size: 0.65rem;
            font-weight: 700;
            padding: 0.1rem 0.4rem;
            border-radius: 4px;
            text-transform: uppercase;
            float: right;
            margin-top: -0.2rem;
        }}
        .status-badge.processing {{ background-color: #E9ECEF; color: #495057; border: 1px solid #CED4DA; }}
        .status-badge.complete {{ background-color: #D4EDDA; color: #155724; border: 1px solid #C3E6CB; }}
        .status-badge.error {{ background-color: #F8D7DA; color: #721C24; border: 1px solid #F5C6CB; }}
        .status-badge.skipped {{ background-color: #FFF3CD; color: #856404; border: 1px solid #FFEEBA; }}
        .status-badge.pending {{ background-color: #F8F9FA; color: #ADB5BD; border: 1px solid #E9ECEF; }}

        .result-value {{
            color: #2C3E50;
            font-size: 1.25rem;
            font-weight: 600;
        }}

        .confidence-tag {{
            display: inline-block;
            padding: 0.2rem 0.6rem;
            background-color: #F1F3F5;
            color: #495057;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-top: 0.5rem;
        }}

        .confidence-tag.high {{ background-color: #D4EDDA; color: #155724; }}
        .confidence-tag.med {{ background-color: #FFF3CD; color: #856404; }}
        .confidence-tag.low {{ background-color: #F8D7DA; color: #721C24; }}

        /* VLM Status Indicators */
        .vlm-status {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            color: #28A745;
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            padding: 0.5rem 1rem;
            background-color: #E6F4EA;
            border-radius: 8px;
            width: fit-content;
        }}

        .vlm-status.skipped {{
            color: #6C757D;
            background-color: #F8F9FA;
            border: 1px solid #E9ECEF;
        }}

        /* Pipeline Breadcrumbs */
        .breadcrumb-container {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 2rem;
            padding: 1rem 0;
            border-bottom: 1px solid #E9ECEF;
        }}

        .breadcrumb-step {{
            text-align: center;
            flex: 1;
            font-size: 0.8rem;
            font-weight: 600;
            color: #CED4DA;
            position: relative;
        }}

        .breadcrumb-step.active {{
            color: #007BFF;
        }}

        .breadcrumb-step.done {{
            color: #28A745;
        }}

        /* Floating Action Button (FAB) */
        .fab-container {{
            position: fixed;
            bottom: 3rem;
            right: 3rem;
            z-index: 1000;
        }}

        /* Target both st.button and st.download_button inside FAB */
        .fab-container button, .fab-container a {{
            border-radius: 50px !important;
            padding: 0.8rem 1.8rem !important;
            background-color: #007BFF !important;
            color: white !important;
            border: none !important;
            box-shadow: 0 6px 16px rgba(0, 123, 255, 0.3) !important;
            font-weight: 600 !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            text-decoration: none !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
        }}

        .fab-container button:hover, .fab-container a:hover {{
            background-color: #0056b3 !important;
            box-shadow: 0 8px 24px rgba(0, 123, 255, 0.5) !important;
            transform: translateY(-3px) !important;
        }}

        .fab-container button:active, .fab-container a:active {{
            transform: translateY(-1px) !important;
        }}

        .stButton > button {{
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
        }}

        /* Enhanced Upload Area */
        .upload-container {{
            border: 2px dashed #007BFF;
            border-radius: 12px;
            padding: 3rem 2rem;
            text-align: center;
            background-color: #FFFFFF;
            transition: all 0.3s ease;
            margin-bottom: 2rem;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }}

        .upload-container:hover {{
            border-color: #0056b3;
            background-color: #F0F7FF;
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 123, 255, 0.1);
        }}

        .upload-icon {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}

        .upload-text {{
            color: #2C3E50;
            font-size: 1.25rem;
            font-weight: 500;
            margin-bottom: 1.5rem;
        }}

        .upload-subtext {{
            color: #6C757D;
            font-size: 0.85rem;
            margin-top: 1rem;
        }}

        .success-pulse {{
            animation: pulse-green 2s infinite;
            border-color: #28A745 !important;
        }}

        @keyframes pulse-green {{
            0% {{ box-shadow: 0 0 0 0 rgba(40, 167, 69, 0.4); }}
            70% {{ box-shadow: 0 0 0 10px rgba(40, 167, 69, 0); }}
            100% {{ box-shadow: 0 0 0 0 rgba(40, 167, 69, 0); }}
        }}

        /* Clinical Narrative Area */
        .narrative-container {{
            background-color: #FFFFFF;
            border-left: 4px solid #007BFF;
            padding: 1.5rem;
            font-size: 1.1rem;
            line-height: 1.7;
            color: #2C3E50;
            border-radius: 0 8px 8px 0;
        }}

        /* Decision Journal Styling */
        .journal-container {{
            background-color: #FFFFFF;
            border: 1px solid #E9ECEF;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            margin-bottom: 2rem;
        }}

        .journal-entry {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 0.75rem 1.25rem;
            border-bottom: 1px solid #F1F3F5;
            transition: background-color 0.2s ease;
        }}

        .journal-entry:last-child {{
            border-bottom: none;
        }}

        .journal-entry:hover {{
            background-color: #F8F9FA;
        }}

        .journal-timestamp {{
            font-family: 'Inter', monospace;
            font-size: 0.75rem;
            color: #ADB5BD;
            min-width: 65px;
        }}

        .journal-badge {{
            font-size: 0.65rem;
            font-weight: 700;
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            text-transform: uppercase;
            min-width: 75px;
            text-align: center;
            letter-spacing: 0.02rem;
        }}

        .journal-badge.id {{ background-color: #E7F3FF; color: #007BFF; border: 1px solid #BEE3F8; }}
        .journal-badge.gate {{ background-color: #F8F9FA; color: #6C757D; border: 1px solid #E9ECEF; }}
        .journal-badge.synthesis {{ background-color: #E6F4EA; color: #28A745; border: 1px solid #C3E6CB; }}

        .journal-event {{
            flex-grow: 1;
            font-size: 0.9rem;
            color: #2C3E50;
            font-weight: 500;
        }}

        .journal-outcome {{
            font-size: 0.85rem;
            font-weight: 600;
            color: #495057;
            background-color: #F1F3F5;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
        }}

        .journal-outcome.triggered {{ color: #007BFF; background-color: #E7F3FF; }}
        .journal-outcome.skipped {{ color: #6C757D; background-color: #F8F9FA; }}
        .journal-outcome.success {{ color: #28A745; background-color: #E6F4EA; }}

        .journal-confidence {{
            font-size: 0.85rem;
            font-weight: 700;
            color: #007BFF;
            min-width: 60px;
            text-align: right;
        }}

        .journal-metadata {{
            background-color: #F8F9FA;
            padding: 1rem;
            border-top: 1px solid #F1F3F5;
            font-size: 0.8rem;
        }}
    </style>
    """
