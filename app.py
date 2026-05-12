import streamlit as st
from src.logic.state import init_state, reset_state, PipelineStage

def main() -> None:
    """
    Main entry point for the NeuroGemma application.
    Configures the Streamlit UI layout and handles high-level orchestration.
    """
    # Initialize session state
    init_state()

    # Global Page Configuration
    st.set_page_config(
        page_title="NeuroGemma | AI-Powered Radiology Assistant",
        page_icon="🧠",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Sidebar
    with st.sidebar:
        st.title("NeuroGemma")
        st.write("---")
        
        # Mock Mode toggle synced with state
        st.session_state.inference.is_mock_mode = st.toggle(
            "Mock Mode", 
            value=st.session_state.inference.is_mock_mode, 
            help="Simulate AI model outputs without local GPU inference."
        )

        if st.session_state.inference.is_mock_mode:
            st.write("---")
            st.subheader("Golden Datasets")
            dataset_option = st.selectbox(
                "Select Scenario",
                options=["axial_flair", "sagittal_t1"],
                format_func=lambda x: "Axial-FLAIR (Positive)" if x == "axial_flair" else "Sagittal-T1 (Skipped)"
            )
            if st.button("Load Mock Data", use_container_width=True):
                from src.logic.logic_gate import run_mock_inference
                run_mock_inference(dataset_option)
                st.rerun()
        
        st.write("---")
        # Placeholder for Clear Session (Logic in 1.4)
        if st.button("Clear Session", use_container_width=True):
            reset_state()
            st.rerun()
            
        st.write("---")
        st.info("System Status: Ready")

    # Main Header
    st.title("🧠 NeuroGemma")
    st.markdown("### Advanced MRI Analysis & Clinical Decision Support")

    # Tab Layout
    tab_diag, tab_logs = st.tabs(["📋 Diagnostic View", "⚙️ Technical Logs"])

    inference = st.session_state.inference

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
        else:
            st.info("Upload an MRI image to begin analysis.")
            # Placeholder for upload area
            st.file_uploader("Upload MRI Scan (FLAIR/T2)", type=["png", "jpg", "jpeg", "dcm"])

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
