import streamlit as st
from crew import run_crew_for_url
from tasks import AnalysisOutput
import os

# Page configuration
st.set_page_config(
    page_title="Patrakaarita - News Analysis",
    page_icon="📰",
    layout="wide"
)

# Custom CSS - Works for both light and dark themes
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        opacity: 0.8;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 0.5rem;
    }
    .claim-item {
        background-color: rgba(76, 175, 80, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #4CAF50;
    }
    .red-flag {
        background-color: rgba(244, 67, 54, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #f44336;
    }
    .verification-q {
        background-color: rgba(33, 150, 243, 0.1);
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 0.5rem;
        border-left: 4px solid #2196F3;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">📰 Patrakaarita</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered News Article Analysis</div>', unsafe_allow_html=True)

# Main content
st.divider()

# Input section
url_input = st.text_input(
    "📎 Enter News Article URL",
    placeholder="https://example.com/news-article",
    help="Paste the URL of a news article you want to analyze"
)

analyze_button = st.button("🔍 Analyze Article", type="primary", use_container_width=True)

# Analysis section
if analyze_button:
    if not url_input:
        st.error("⚠️ Please enter a URL")
    else:
        with st.spinner("🔄 Analyzing article... This may take 30-60 seconds"):
            try:
                # Run the crew
                result = run_crew_for_url(url_input)
                
                # Extract the analysis output
                if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
                    analysis = result.tasks_output[-1].pydantic
                    
                    if isinstance(analysis, AnalysisOutput):
                        st.success("✅ Analysis Complete!")
                        
                        # Display results
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            # Core Claims
                            st.markdown('<div class="section-header">💡 Core Claims</div>', unsafe_allow_html=True)
                            for i, claim in enumerate(analysis.core_claims, 1):
                                st.markdown(f'<div class="claim-item"><strong>{i}.</strong> {claim}</div>', unsafe_allow_html=True)
                            
                            # Tone Analysis
                            st.markdown('<div class="section-header">🎯 Tone & Language Analysis</div>', unsafe_allow_html=True)
                            st.write(analysis.tone_analysis)
                            
                            # Red Flags
                            st.markdown('<div class="section-header">🚩 Potential Red Flags</div>', unsafe_allow_html=True)
                            if analysis.red_flags:
                                for i, flag in enumerate(analysis.red_flags, 1):
                                    st.markdown(f'<div class="red-flag"><strong>{i}.</strong> {flag}</div>', unsafe_allow_html=True)
                            else:
                                st.info("No red flags identified")
                            
                            # Verification Questions
                            st.markdown('<div class="section-header">✅ Verification Questions</div>', unsafe_allow_html=True)
                            for i, question in enumerate(analysis.verification_questions, 1):
                                st.markdown(f'<div class="verification-q"><strong>{i}.</strong> {question}</div>', unsafe_allow_html=True)
                        
                        with col2:
                            # Named Entities
                            if analysis.named_entities:
                                st.markdown('<div class="section-header">👥 Named Entities</div>', unsafe_allow_html=True)
                                for entity_type, entities in analysis.named_entities.items():
                                    if entities:
                                        st.write(f"**{entity_type.upper()}:**")
                                        for entity in entities:
                                            st.write(f"- {entity}")
                            
                            # Opposing Viewpoint
                            if analysis.opposing_viewpoint:
                                st.markdown('<div class="section-header">🔄 Opposing Viewpoint</div>', unsafe_allow_html=True)
                                st.info(analysis.opposing_viewpoint)
                        
                        # Download button
                        st.divider()
                        report_text = f"""PATRAKAARITA ANALYSIS REPORT
================================

CORE CLAIMS
-----------
{chr(10).join(f'{i}. {claim}' for i, claim in enumerate(analysis.core_claims, 1))}

TONE ANALYSIS
-------------
{analysis.tone_analysis}

RED FLAGS
---------
{chr(10).join(f'{i}. {flag}' for i, flag in enumerate(analysis.red_flags, 1)) if analysis.red_flags else 'None identified'}

VERIFICATION QUESTIONS
----------------------
{chr(10).join(f'{i}. {q}' for i, q in enumerate(analysis.verification_questions, 1))}
"""
                        if analysis.named_entities:
                            report_text += f"\n\nNAMED ENTITIES\n--------------\n"
                            for entity_type, entities in analysis.named_entities.items():
                                if entities:
                                    report_text += f"{entity_type.upper()}: {', '.join(entities)}\n"
                        
                        if analysis.opposing_viewpoint:
                            report_text += f"\n\nOPPOSING VIEWPOINT\n------------------\n{analysis.opposing_viewpoint}\n"
                        
                        st.download_button(
                            label="📥 Download Report",
                            data=report_text,
                            file_name="analysis_report.txt",
                            mime="text/plain",
                            use_container_width=True
                        )
                    else:
                        st.error("❌ Failed to parse analysis output")
                else:
                    st.error("❌ No output generated")
                    
            except Exception as e:
                error_msg = str(e)
                
                # Handle specific API errors
                if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                    st.error("""
                    ⚠️ **API Rate Limit Exceeded**
                    
                    The Groq API has reached its rate limit.  
                    Free tier limit: 30 requests per minute
                    
                    Please wait 30-60 seconds and try again.
                    """)
                elif "503" in error_msg or "UNAVAILABLE" in error_msg:
                    st.error("""
                    ⚠️ **API Service Unavailable**
                    
                    The Groq API is currently overloaded or unavailable.
                    
                    Please try again in a few moments.
                    """)
                elif "401" in error_msg or "403" in error_msg:
                    st.error("""
                    ⚠️ **Authentication Error**
                    
                    Invalid or missing API key.
                    
                    Please check your GROQ_API_KEY in Streamlit secrets.
                    """)
                else:
                    st.error(f"""
                    ⚠️ **Error**
                    
                    An error occurred while analyzing the article:
                    
                    {error_msg}
                    
                    Please try again or check the logs for details.
                    """)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <a href="https://github.com/Karan-Baid/Patrakaarita">GitHub</a>
</div>
""", unsafe_allow_html=True)
