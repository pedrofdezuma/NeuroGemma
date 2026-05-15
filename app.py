import streamlit as st
from src.logic.state import init_state, reset_state, PipelineStage
from datetime import datetime

def main() -> None:
    """
    Main entry point for the NeuroGemma application.
    Configures the Streamlit UI layout and handles high-level orchestration.
    """
    # Global Page Configuration - MUST be the first Streamlit command
    st.set_page_config(
        page_title="NeuroGemma | AI-Powered Radiology Assistant",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Initialize session state
    init_state()

    # Load Custom CSS
    from src.utils.styles import load_custom_css, render_breadcrumbs
    st.markdown(load_custom_css(), unsafe_allow_html=True)

    inference = st.session_state.inference

    # Pipeline Breadcrumbs - Dynamic Placeholder (Defined early for sidebar access)
    breadcrumb_placeholder = st.empty()
    breadcrumb_placeholder.markdown(render_breadcrumbs(inference.current_stage), unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-header">NeuroGemma</div>', unsafe_allow_html=True)
        
        st.subheader("Control Center")
        
        # Mock Mode toggle synced with state
        st.session_state.inference.is_mock_mode = st.toggle(
            "Mock Mode", 
            value=st.session_state.inference.is_mock_mode, 
            help="Simulate AI model outputs without local GPU inference. Ideal for demonstrations and testing UI logic."
        )

        if st.session_state.inference.is_mock_mode:
            st.markdown("---")
            st.write("#### Golden Datasets")
            dataset_option = st.selectbox(
                "Select Clinical Scenario",
                options=["axial_flair", "sagittal_t1", "error_scenario"],
                format_func=lambda x: {
                    "axial_flair": "Axial-FLAIR (Positive)",
                    "sagittal_t1": "Sagittal-T1 (Skipped)",
                    "error_scenario": "Simulated Pipeline Error"
                }.get(x, x),
                help="Choose a pre-defined radiology scenario to simulate pipeline behavior."
            )
            if st.button("Load Mock Data", width="stretch"):
                from src.logic.logic_gate import run_mock_inference
                try:
                    # Execute generator for real-time state updates in background
                    for stage in run_mock_inference(dataset_option):
                        breadcrumb_placeholder.markdown(render_breadcrumbs(stage), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"❌ Pipeline Failure: {str(e)}")
                st.rerun()
        
        st.markdown("---")
        # Privacy Reset
        if st.button("Clear Session", width="stretch", help="Wipe all results, logs, and clinical image data from the current session."):
            reset_state()
            st.rerun()
            
        st.write("---")
        st.info("System Status: Ready")

    # Main Header
    st.title("🧠 NeuroGemma")
    st.markdown("### Advanced MRI Analysis & Clinical Decision Support")

    st.markdown("<br>", unsafe_allow_html=True)

    # Tab Layout
    tab_diag, tab_logs = st.tabs(["📋 Diagnostic View", "⚙️ Technical Logs"])

    with tab_diag:
        if not inference.uploaded_image:
            # Welcome & Upload Stage
            st.info("👋 Welcome to NeuroGemma. Please upload a brain scan to begin analysis.")
            
            uploaded_file = st.file_uploader(
                "Drag and drop or click to upload MRI Scan", 
                type=["png", "jpg", "jpeg"],
                help="Supported formats: JPG, PNG • Max size: 20MB"
            )
            
            if uploaded_file:
                from src.utils.file_handler import validate_and_load_image
                try:
                    with st.status("🩺 Validating Scan...", expanded=False) as status:
                        image = validate_and_load_image(uploaded_file)
                        status.update(label="✅ Scan Validated", state="complete")
                    
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
                    
                    st.toast("✅ Image Validated Successfully")
                    st.success("Redirecting to analysis dashboard...")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Upload Error: {str(e)}")
        else:
            # Split-Screen Dashboard
            col_img, col_res = st.columns([1.2, 1])

            with col_img:
                st.markdown('<div class="result-card" style="background-color: #000; text-align: center;">', unsafe_allow_html=True)
                st.image(inference.uploaded_image, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Image Controls
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Change Image", use_container_width=True):
                        reset_state()
                        st.rerun()
                with c2:
                    if not inference.results:
                        if st.button("🚀 Run Pipeline", use_container_width=True):
                            from src.logic.logic_gate import run_pipeline
                            with st.status("🧠 Orchestrating Models...", expanded=True) as status:
                                try:
                                    # Iterate through the generator to push real-time breadcrumb updates
                                    for stage in run_pipeline(inference.uploaded_image):
                                        breadcrumb_placeholder.markdown(render_breadcrumbs(stage), unsafe_allow_html=True)
                                    status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                                except Exception as e:
                                    status.update(label="❌ Pipeline Error", state="error", expanded=True)
                                    st.error(f"Critical failure during inference: {str(e)}")
                            st.rerun()

            with col_res:
                if inference.results:
                    # CNN Results
                    st.markdown("#### Quantitative Analysis")
                    res_cols = st.columns(3)
                    
                    try:
                        depth_val = float(inference.results.get("depth", 0.0))
                        depth_display = f"{depth_val:.2f}"
                    except (ValueError, TypeError):
                        depth_display = str(inference.results.get("depth", "N/A"))

                    metrics = [
                        ("Plane", inference.results.get("plane", "N/A"), inference.results.get("plane_conf", 1.0), "plane", inference.model_status.get("plane", "Pending")),
                        ("Sequence", inference.results.get("sequence", "N/A"), inference.results.get("sequence_conf", 1.0), "sequence", inference.model_status.get("sequence", "Pending")),
                        ("Depth", depth_display, inference.results.get("depth_conf", 1.0), "depth", inference.model_status.get("depth", "Pending"))
                    ]
                    
                    for i, (label, value, conf, css_class, status) in enumerate(metrics):
                        conf_level = "high" if conf >= 0.8 else "med" if conf >= 0.5 else "low"
                        status_class = status.lower()
                        # Only show confidence for non-depth metrics (Regression models don't have classification confidence)
                        conf_html = f'<div class="confidence-tag {conf_level}">{conf:.1%} Conf.</div>' if css_class != "depth" else ""
                        
                        with res_cols[i]:
                            st.markdown(f"""
                            <div class="result-card {css_class} {status_class}">
                                <div class="status-badge {status_class}">{status}</div>
                                <div class="result-label">{label}</div>
                                <div class="result-value">{value}</div>
                                {conf_html}
                            </div>
                            """, unsafe_allow_html=True)
                    
                    # Narrative
                    st.markdown("#### Clinical Narrative")
                    narrative = inference.results.get("narrative")
                    narr_status = inference.model_status.get("narrative", "Pending")
                    
                    if narr_status == "Processing":
                        st.info("✨ MedGemma VLM is analyzing the scan...")
                    elif narr_status == "Error":
                        st.error("❌ VLM Synthesis Error. Check logs for details.")
                    elif narr_status == "Complete":
                        st.markdown(f"""
                        <div class="vlm-status">
                            <span>✨</span> VLM Triggered: Narrative Generated
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
                            <span>🚫</span> VLM Skipped: {narrative or "Non-Axial-FLAIR scan detected"}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.info("Waiting for logic gate decision...")

                    # FAB - Floating Action Button for PDF Export
                    if inference.current_stage == PipelineStage.COMPLETE:
                        from src.reports.report_engine import generate_report, get_report_filename
                        
                        st.markdown('<div class="fab-container">', unsafe_allow_html=True)
                        try:
                            # Generate report data
                            report_bytes = generate_report(inference)
                            report_filename = get_report_filename(inference)
                            
                            st.download_button(
                                label="📄 Generate Radiology Note",
                                data=report_bytes,
                                file_name=report_filename,
                                mime="application/pdf",
                                key="fab_pdf_download",
                                on_click=reset_state,
                                help="Download the professional radiology report as a PDF."
                            )
                        except Exception as e:
                            st.error(f"Failed to prepare report: {str(e)}")
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.info("Ready for inference. Click 'Run Pipeline' to start.")
                    st.json(inference.image_metadata)

    with tab_logs:
        st.markdown("### ⚙️ Technical Decision Journal")
        
        if not inference.step_logs:
            st.markdown("""
                <div style="text-align: center; padding: 3rem; color: #6C757D;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🕒</div>
                    <div style="font-weight: 500;">No activity recorded yet.</div>
                    <div style="font-size: 0.85rem;">Start the inference pipeline to generate a technical audit trail.</div>
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
                    <div class="journal-event">{event}</div>
                    <div class="journal-outcome {outcome_class}">{outcome}</div>
                    {conf_html}
                </div>
                """, unsafe_allow_html=True)
                
                # 4. Inspector / Metadata (AC #7)
                with st.expander(f"🔍 Technical Metadata: {event}", expanded=False):
                    st.json(log.get('metadata', {}))
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
