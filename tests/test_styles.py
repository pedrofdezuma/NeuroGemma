import pytest
from src.utils.styles import load_custom_css, render_breadcrumbs
from src.logic.state import PipelineStage

def test_load_custom_css_returns_string():
    """Test that load_custom_css returns a non-empty string containing expected colors."""
    css = load_custom_css()
    assert isinstance(css, str)
    # Clinical Blue
    assert "#007BFF" in css
    # Darker contrast
    assert "#2C3E50" in css
    # Light background
    assert "#F8F9FA" in css

def test_load_custom_css_contains_relieved_classes():
    """Test that the CSS includes all required 'Relieved' aesthetic classes."""
    css = load_custom_css()
    classes = [
        ".block-container",
        ".result-card",
        ".narrative-container",
        ".breadcrumb-container",
        ".breadcrumb-step",
        ".upload-container",
        ".upload-icon",
        ".upload-subtext",
        ".success-pulse",
        ".fab-container",
        "border-radius: 50px",
        "box-shadow: 0 6px 16px rgba(0, 123, 255, 0.3)"
    ]
    for css_class in classes:
        assert css_class in css

def test_load_custom_css_font_import():
    """Test that the CSS imports the Inter font."""
    css = load_custom_css()
    assert "@import url('https://fonts.googleapis.com/css2?family=Inter" in css

def test_render_breadcrumbs_id():
    """Test breadcrumbs for the ID stage."""
    html = render_breadcrumbs(PipelineStage.ID)
    assert 'class="breadcrumb-step active">IDENTIFICATION</div>' in html
    assert 'class="breadcrumb-step">LOGIC GATE</div>' in html
    assert 'class="breadcrumb-step">SYNTHESIS</div>' in html
    assert 'class="breadcrumb-step">COMPLETE</div>' in html

def test_render_breadcrumbs_gate():
    """Test breadcrumbs for the GATE stage."""
    html = render_breadcrumbs(PipelineStage.GATE)
    assert 'class="breadcrumb-step done">IDENTIFICATION</div>' in html
    assert 'class="breadcrumb-step active">LOGIC GATE</div>' in html
    assert 'class="breadcrumb-step">SYNTHESIS</div>' in html

def test_render_breadcrumbs_synthesis():
    """Test breadcrumbs for the SYNTHESIS stage."""
    html = render_breadcrumbs(PipelineStage.SYNTHESIS)
    assert 'class="breadcrumb-step done">IDENTIFICATION</div>' in html
    assert 'class="breadcrumb-step done">LOGIC GATE</div>' in html
    assert 'class="breadcrumb-step active">SYNTHESIS</div>' in html

def test_render_breadcrumbs_complete():
    """Test breadcrumbs for the COMPLETE stage."""
    html = render_breadcrumbs(PipelineStage.COMPLETE)
    assert 'class="breadcrumb-step done">IDENTIFICATION</div>' in html
    assert 'class="breadcrumb-step done">LOGIC GATE</div>' in html
    assert 'class="breadcrumb-step done">SYNTHESIS</div>' in html
    assert 'class="breadcrumb-step active">COMPLETE</div>' in html

def test_render_breadcrumbs_spanish():
    """Test breadcrumbs rendering in Spanish."""
    html = render_breadcrumbs(PipelineStage.ID, lang="Español")
    assert 'class="breadcrumb-step active">IDENTIFICACIÓN</div>' in html
    assert 'class="breadcrumb-step">COMPUERTA LÓGICA</div>' in html
    assert 'class="breadcrumb-step">SÍNTESIS</div>' in html
    assert 'class="breadcrumb-step">COMPLETADO</div>' in html
