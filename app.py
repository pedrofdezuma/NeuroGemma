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
    from src.utils.styles import load_custom_css
    st.markdown(load_custom_css(), unsafe_allow_html=True)

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
                options=["axial_flair", "sagittal_t1"],
                format_func=lambda x: "Axial-FLAIR (Positive)" if x == "axial_flair" else "Sagittal-T1 (Skipped)",
                help="Choose a pre-defined radiology scenario to simulate pipeline behavior."
            )
            if st.button("Load Mock Data", width="stretch"):
                from src.logic.logic_gate import run_mock_inference
                run_mock_inference(dataset_option)
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

    inference = st.session_state.inference

    # Pipeline Breadcrumbs
    stages = ["ID", "GATE", "SYNTHESIS", "COMPLETE"]
    current_stage_val = inference.current_stage.value
    
    cols = st.columns(len(stages))
    for i, stage in enumerate(stages):
        is_active = (stage == current_stage_val)
        is_done = False
        # Simple logic for "done" stages based on current_stage
        stage_order = {"ID": 0, "GATE": 1, "SYNTHESIS": 2, "COMPLETE": 3}
        if stage_order[current_stage_val] > stage_order[stage]:
            is_done = True
        
        color = "#007BFF" if (is_active or is_done) else "#CED4DA"
        label = f"**{stage}**" if is_active else stage
        cols[i].markdown(f'<div style="text-align: center; color: {color}; border-bottom: 3px solid {color}; padding-bottom: 5px;">{label}</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tab Layout
    tab_diag, tab_logs = st.tabs(["📋 Diagnostic View", "⚙️ Technical Logs"])

    with tab_diag:
        st.header("Diagnostic Pipeline")
        
        if inference.current_stage == PipelineStage.COMPLETE:
            st.success("Analysis Complete")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Plane", inference.results["plane"])
                st.metric("Sequence", inference.results["sequence"])
            with col2:
                st.metric("Confidence", f"{inference.results['confidence']:.2%}")
                st.metric("VLM Status", "Active" if inference.results["narrative"] else "Skipped")
            
            if inference.results["narrative"]:
                st.markdown("#### Clinical Narrative")
                st.info(inference.results["narrative"])
        
        # Image Upload Section (Visible if no results yet or explicitly at ID stage)
        if not inference.results:
            if not inference.uploaded_image:
                st.markdown('<div class="upload-container">', unsafe_allow_html=True)
                st.markdown('<p class="upload-text">Drag & Drop Brain Scan Here or Click to Upload</p>', unsafe_allow_html=True)
                uploaded_file = st.file_uploader(
                    "Upload MRI Scan (FLAIR/T2)", 
                    type=["png", "jpg", "jpeg"],
                    label_visibility="collapsed"
                )
                st.markdown('</div>', unsafe_allow_html=True)
                
                if uploaded_file:
                    from src.utils.file_handler import validate_and_load_image
                    try:
                        image = validate_and_load_image(uploaded_file)
                        
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
                        st.success(f"Image '{uploaded_file.name}' validated successfully.")
                        st.rerun()
                    except Exception as e:
                        st.error(str(e))
            else:
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.subheader("Image Preview")
                    st.image(inference.uploaded_image, width="stretch")
                with col2:
                    st.subheader("Image Metadata")
                    st.json(inference.image_metadata)
                    if st.button("Change Image", width="stretch"):
                        inference.uploaded_image = None
                        inference.image_metadata = {}
                        st.rerun()
                
                st.markdown("---")
                if st.button("🚀 Run Diagnostic Pipeline", width="stretch"):
                    from src.logic.logic_gate import run_pipeline
                    with st.status("🧠 Processing MRI Scan...", expanded=True) as status:
                        run_pipeline(inference.uploaded_image)
                        status.update(label="✅ Analysis Complete!", state="complete", expanded=False)
                    st.rerun()
                st.info("System ready for inference. Click the button above to start the automated clinical pipeline.")

    with tab_logs:
        st.header("Technical Decision Journal")
        if inference.step_logs:
            for log in inference.step_logs:
                with st.expander(f"{log['stage']} - {log['event']}"):
                    st.json(log)
        else:
            st.code("--- Pipeline initialized ---\n[INFO] Waiting for user input...", language="text")

if __name__ == "__main__":
    main()
