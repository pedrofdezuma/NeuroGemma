import streamlit as st
from src.logic.state import init_state, reset_state, PipelineStage
from datetime import datetime
from typing import Any

from src.utils.localization import get_text

def localize_metadata(metadata: dict[str, Any], lang: str, event_type: str = "") -> dict[str, Any]:
    """
    Translate metadata keys and format values for user-friendly display.
    Maps raw scores to localized class labels based on the event_type.
    """
    localized = {}
    for key, value in metadata.items():
        # Translate main keys
        loc_key = get_text(f"meta_{key}", lang)
        
        # 1. Special handling for 'size'
        if key == "size" and isinstance(value, (list, tuple)) and len(value) >= 2:
            localized[loc_key] = {
                get_text("meta_width", lang): value[0],
                get_text("meta_height", lang): value[1]
            }
        # 2. Localize 'raw_scores' based on event type
        elif key == "raw_scores" and isinstance(value, list):
            labels = []
            if "PLANE" in event_type:
                labels = ['axial', 'coronal', 'sagittal', 'non_brain_mri']
            elif "SEQUENCE" in event_type:
                labels = ['t1-w', 't1-ce', 't2-w', 'flair', 'others']
            elif "DEPTH" in event_type:
                labels = ['depth']
            
            if labels:
                score_dict = {}
                for i, score in enumerate(value):
                    if i < len(labels):
                        label_key = f"val_{labels[i]}" if labels[i] != "depth" else "meta_depth"
                        score_dict[get_text(label_key, lang)] = score
                localized[loc_key] = score_dict
            else:
                localized[loc_key] = value

        # 3. Translate technical values for plane and sequence
        elif key in ["plane", "sequence"] and isinstance(value, str):
            localized[loc_key] = get_text(f"val_{value.lower()}", lang)
        # 4. Recursive localization for nested dicts
        elif isinstance(value, dict):
            localized[loc_key] = localize_metadata(value, lang, event_type)
        else:
            localized[loc_key] = value
            
    return localized

def main() -> None:
    """
    Main entry point for the NeuroGemma application.
    Configures the Streamlit UI layout and handles high-level orchestration.
    """
    # Initialize session state early to access language preference
    init_state()
    lang = st.session_state.inference.language

    # Global Page Configuration - MUST be the first Streamlit command
    st.set_page_config(
        page_title=get_text("page_title", lang),
        page_icon="src/assets/icon.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Load Custom CSS
    from src.utils.styles import load_custom_css, render_breadcrumbs
    st.markdown(load_custom_css(lang), unsafe_allow_html=True)

    inference = st.session_state.inference

    # Pipeline Breadcrumbs - Dynamic Placeholder (Defined early for sidebar access)
    breadcrumb_placeholder = st.empty()
    breadcrumb_placeholder.markdown(render_breadcrumbs(inference.current_stage, lang), unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.image("src/assets/icon.png", width=100)
        st.markdown('<div class="sidebar-header">NeuroGemma</div>', unsafe_allow_html=True)
        
        # Language Selector
        st.session_state.inference.language = st.selectbox(
            get_text("language_label", lang),
            options=["English", "Español"],
            index=0 if lang == "English" else 1
        )
        lang = st.session_state.inference.language # Update local lang variable after potentially changing in state

        st.subheader(get_text("control_center", lang))
        
        # Mock Mode toggle synced with state
        st.session_state.inference.is_mock_mode = st.toggle(
            get_text("mock_mode", lang), 
            value=st.session_state.inference.is_mock_mode, 
            help=get_text("mock_mode_help", lang)
        )

        if st.session_state.inference.is_mock_mode:
            st.markdown("---")
            st.write(f"#### {get_text('select_scenario', lang)}")
            dataset_option = st.selectbox(
                get_text("select_scenario", lang),
                options=["axial_flair", "sagittal_t1"],
                format_func=lambda x: get_text(x, lang),
                help=get_text("select_scenario_help", lang),
                label_visibility="collapsed"
            )
            if st.button(get_text("load_mock_data", lang), width="stretch"):
                from src.logic.logic_gate import run_mock_inference
                try:
                    # Execute generator for real-time state updates in background
                    for stage in run_mock_inference(dataset_option):
                        breadcrumb_placeholder.markdown(render_breadcrumbs(stage), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"{get_text('pipeline_error', lang)}: {str(e)}")
                st.rerun()
        
        st.markdown("---")
        # Privacy Reset
        if st.button(get_text("clear_session", lang), width="stretch", help=get_text("clear_session_help", lang)):
            reset_state()
            st.rerun()
            
        st.write("---")
        st.info(get_text("system_status_ready", lang))

    # Main Header
    logo_col, title_col = st.columns([0.06, 0.94])
    with logo_col:
        st.image("src/assets/icon.png", width=60)
    with title_col:
        st.title("NeuroGemma")
    st.markdown(f"### {get_text('app_subtitle', lang)}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tab Layout
    tab_diag, tab_logs = st.tabs([get_text("tab_diagnostic", lang), get_text("tab_logs", lang)])

    with tab_diag:
        if not inference.uploaded_image:
            # Welcome & Upload Stage
            st.info(get_text("welcome_message", lang))
            
            uploaded_file = st.file_uploader(
                get_text("uploader_label", lang), 
                type=["png", "jpg", "jpeg"],
                help=get_text("uploader_help", lang)
            )
            
            if uploaded_file:
                from src.utils.file_handler import validate_and_load_image
                try:
                    with st.status(get_text("validating_scan", lang), expanded=False) as status:
                        image = validate_and_load_image(uploaded_file)
                        status.update(label=get_text("scan_validated", lang), state="complete")
                    
                    # Update state
                    inference.uploaded_image = image
                    inference.image_metadata = {
                        "filename": uploaded_file.name,
                        "format": image.format,
                        "size": image.size,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    # Log Event
                    log_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "stage": "ID",
                        "event": "UPLOAD_SUCCESS",
                        "model_id": "user_input",
                        "outcome": "IMAGE_VALIDATED",
                        "confidence": 1.0,
                        "metadata": inference.image_metadata
                    }
                    inference.step_logs.append(log_entry)
                    inference.current_stage = PipelineStage.ID
                    
                    st.toast(get_text("scan_validated", lang))
                    st.success(get_text("redirecting", lang))
                    st.rerun()
                except Exception as e:
                    st.error(f"{get_text('upload_error', lang)}: {str(e)}")
        else:
            # Split-Screen Dashboard
            col_img, col_res = st.columns([1.2, 1])

            with col_img:
                st.markdown('<div class="result-card" style="background-color: #000; text-align: center; padding: 0; overflow: hidden;">', unsafe_allow_html=True)
                st.image(inference.uploaded_image, width="stretch")
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Image Controls
                c1, c2 = st.columns(2)
                with c1:
                    if st.button(get_text("change_image", lang), width="stretch"):
                        reset_state()
                        st.rerun()
                with c2:
                    if not inference.results:
                        if st.button(get_text("run_pipeline", lang), width="stretch"):
                            from src.logic.logic_gate import run_pipeline
                            with st.status(get_text("orchestrating_models", lang), expanded=True) as status:
                                try:
                                    # Iterate through the generator to push real-time breadcrumb updates
                                    for stage in run_pipeline(inference.uploaded_image):
                                        breadcrumb_placeholder.markdown(render_breadcrumbs(stage), unsafe_allow_html=True)
                                    status.update(label=get_text("analysis_complete", lang), state="complete", expanded=False)
                                except Exception as e:
                                    status.update(label=get_text("pipeline_error", lang), state="error", expanded=True)
                                    st.error(f"Critical failure during inference: {str(e)}")
                            st.rerun()

            with col_res:
                if inference.results:
                    # CNN Results
                    st.markdown(get_text("quantitative_analysis", lang))
                    res_cols = st.columns(3)
                    
                    # Localize technical values for UI display
                    plane_val = inference.results.get("plane", "N/A")
                    seq_val = inference.results.get("sequence", "N/A")
                    
                    if lang == "Español":
                        val_map = {
                            "axial": "Axial", "sagittal": "Sagital", "coronal": "Coronal",
                            "flair": "FLAIR", "t1": "T1", "t2": "T2"
                        }
                        plane_val = val_map.get(str(plane_val).lower(), plane_val)
                        seq_val = val_map.get(str(seq_val).lower(), seq_val)

                    try:
                        depth_raw = float(inference.results.get("depth", 0.0))
                        # Use absolute depth for sagittal scans (symmetric hemispheres)
                        is_sagittal = str(inference.results.get("plane", "")).lower() == "sagittal"
                        if is_sagittal:
                            depth_raw = abs(depth_raw)
                        depth_display = f"{depth_raw:.3f}"
                    except (ValueError, TypeError):
                        depth_display = str(inference.results.get("depth", "N/A"))
                        is_sagittal = False

                    metrics = [
                        (get_text("plane", lang), plane_val, inference.results.get("plane_conf", 1.0), "plane", inference.model_status.get("plane", "Pending"), ""),
                        (get_text("sequence", lang), seq_val, inference.results.get("sequence_conf", 1.0), "sequence", inference.model_status.get("sequence", "Pending"), ""),
                        (get_text("depth", lang), depth_display, inference.results.get("depth_conf", 1.0), "depth", inference.model_status.get("depth", "Pending"), get_text("sagittal_depth_help", lang) if is_sagittal else "")
                    ]
                    
                    for i, (label, value, conf, css_class, status, help_text) in enumerate(metrics):
                        conf_level = "high" if conf >= 0.8 else "med" if conf >= 0.5 else "low"
                        status_class = status.lower()
                        # Only show confidence for non-depth metrics (Regression models don't have classification confidence)
                        conf_html = f'<div class="confidence-tag {conf_level}">{conf:.1%} Conf.</div>' if css_class != "depth" else ""
                        
                        # Add help indicator (text-based) if help_text exists
                        label_html = f'{label} <span title="{help_text}" style="cursor: help; text-decoration: underline dotted; font-size: 0.8em;">(info)</span>' if help_text else label

                        with res_cols[i]:
                            st.markdown(f"""
                            <div class="result-card {css_class} {status_class}">
                                <div class="status-badge {status_class}">{status}</div>
                                <div class="result-label">{label_html}</div>
                                <div class="result-value">{value}</div>
                                {conf_html}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Narrative
                    st.markdown(get_text("clinical_narrative", lang))
                    narrative = inference.results.get("narrative")
                    narr_status = inference.model_status.get("narrative", "Pending")
                    
                    if narr_status == "Processing":
                        st.info(get_text("vlm_analyzing", lang))
                    elif narr_status == "Error":
                        st.error(get_text("vlm_error", lang))
                    elif narr_status == "Complete":
                        st.markdown(f"""
                        <div class="vlm-status">
                            {get_text("vlm_triggered", lang)}
                        </div>
                        """, unsafe_allow_html=True)
                        st.markdown(f"""
                        <div class="narrative-container">
                            {narrative}
                        </div>
                        """, unsafe_allow_html=True)
                    elif narr_status == "Skipped":
                        st.markdown(f"""
                        <div class="vlm-status skipped">
                            {get_text("vlm_skipped", lang)}: {narrative or get_text("vlm_skipped_reason", lang)}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info(get_text("waiting_logic", lang))

                    # FAB - Floating Action Button for PDF Export
                    if inference.current_stage == PipelineStage.COMPLETE:
                        from src.reports.report_engine import generate_report, get_report_filename
                        
                        st.markdown('<div class="fab-container">', unsafe_allow_html=True)
                        try:
                            # Generate report data
                            report_bytes = generate_report(inference)
                            report_filename = get_report_filename(inference)
                            
                            st.download_button(
                                label=get_text("generate_report", lang),
                                data=report_bytes,
                                file_name=report_filename,
                                mime="application/pdf",
                                key="fab_pdf_download",
                                on_click=reset_state,
                                help=get_text("generate_report_help", lang)
                            )
                        except Exception as e:
                            st.error(f"Failed to prepare report: {str(e)}")
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info(get_text("ready_inference", lang))
                    st.json(localize_metadata(inference.image_metadata, lang))

    with tab_logs:
        st.markdown(get_text("technical_journal", lang))
        
        if not inference.step_logs:
            st.markdown(f"""
                <div style="text-align: center; padding: 3rem; color: #6C757D;">
                    <div style="font-weight: 500;">{get_text('no_activity', lang)}</div>
                    <div style="font-size: 0.85rem;">{get_text('start_pipeline_hint', lang)}</div>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Container for all journal entries
            st.markdown('<div class="journal-container">', unsafe_allow_html=True)
            
            for log in inference.step_logs:
                # 1. Parse timestamp
                try:
                    ts = datetime.fromisoformat(log['timestamp']).strftime("%H:%M:%S")
                except:
                    ts = "--:--:--"
                
                stage = str(log.get('stage', 'ID'))
                event = str(log.get('event', 'EVENT'))
                outcome = log.get('outcome', 'OUTCOME')
                conf = log.get('confidence')
                
                # Translate Event and Outcome for display
                display_event = get_text(f"log_{event}", lang)
                display_outcome = get_text(f"out_{outcome}", lang)
                
                # 2. Determine Style Classes
                stage_class = stage.lower()
                outcome_class = str(outcome).lower() if outcome is not None else ""
                if "triggered" in outcome_class: outcome_class = "triggered"
                elif "skip" in outcome_class: outcome_class = "skipped"
                elif "success" in outcome_class or "complete" in outcome_class or "validated" in outcome_class: outcome_class = "success"
                
                conf_html = f'<div class="journal-confidence">{conf:.1%}</div>' if conf is not None else '<div class="journal-confidence"></div>'
                
                # 3. Render Entry Row
                st.markdown(f"""
                <div class="journal-entry">
                    <div class="journal-timestamp">{ts}</div>
                    <div class="journal-badge {stage_class}">{stage}</div>
                    <div class="journal-event">{display_event}</div>
                    <div class="journal-outcome {outcome_class}">{display_outcome}</div>
                    {conf_html}
                </div>
                """, unsafe_allow_html=True)
                
                # 4. Inspector / Metadata (AC #7)
                with st.expander(f"{get_text('technical_metadata', lang)}: {display_event}", expanded=False):
                    st.json(localize_metadata(log.get('metadata', {}), lang, event))
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
