import streamlit as st
from analyzers.name_analyzer import NameAnalyzer
import plotly.graph_objects as go
import pandas as pd
from dotenv import load_dotenv

# Load environment variables at the start
load_dotenv(override=True)

# Set page config
st.set_page_config(
    page_title="Name Analysis Tool",
    page_icon="🔮",
    layout="wide"
)

# Initialize analyzer
@st.cache_resource
def get_analyzer():
    return NameAnalyzer()

def create_frequency_chart(frequencies):
    """Create an interactive frequency chart."""
    fig = go.Figure()
    
    # Add frequency plot
    fig.add_trace(go.Scatter(
        y=frequencies,
        mode='lines+markers',
        name='Frequency',
        line=dict(color='#6C63FF')
    ))
    
    fig.update_layout(
        title="Name Frequency Pattern",
        xaxis_title="Letter Position",
        yaxis_title="Frequency (Hz)",
        template="plotly_white"
    )
    
    return fig

def display_results(profile):
    """Display analysis results."""
    results = profile.get_report()
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] {
            font-size: 2.5rem !important;
            font-weight: bold !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 1.2rem !important;
            font-weight: 600 !important;
        }
        .main-header {
            font-size: 2rem !important;
            font-weight: bold !important;
            margin-bottom: 1rem !important;
        }
        .category-header {
            font-size: 1.5rem !important;
            font-weight: bold !important;
            margin-bottom: 0.5rem !important;
        }
        .interpretation-section {
            background-color: rgba(28, 31, 48, 0.1);
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            height: 100%;
        }
        .interpretation-text {
            font-size: 1.1rem !important;
            line-height: 1.6 !important;
        }
        .bullet-header {
            font-size: 1.2rem !important;
            font-weight: bold !important;
            color: #6C63FF !important;
            margin-bottom: 0.5rem !important;
        }
        .bullet-content {
            font-size: 1.1rem !important;
            margin-left: 1.5rem !important;
            margin-bottom: 1rem !important;
            line-height: 1.6 !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Analysis Categories with Metrics
    st.markdown('<p class="main-header">Analysis Results</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<p class="category-header">🔢 Numerological Analysis</p>', unsafe_allow_html=True)
        st.metric("Destiny Number", 
                 results['analyses']['numerology'].get('destiny_number', 'Unknown'))
    
    with col2:
        st.markdown('<p class="category-header">🌊 Vibrational Analysis</p>', unsafe_allow_html=True)
        st.metric("Base Frequency",
                 f"{results['analyses']['vibration'].get('base_frequency', 'Unknown')} Hz")
        if 'resonance_strength' in results['analyses']['vibration']:
            st.metric("Resonance Profile",
                     results['analyses']['vibration'].get('resonance_strength', 'Unknown'))
    
    with col3:
        st.markdown('<p class="category-header">🔤 Phonetic Analysis</p>', unsafe_allow_html=True)
        phonetics = results['analyses']['phonetics']
        st.metric("Consonants/Vowels",
                 f"{phonetics.get('consonant_count', '0')}/{phonetics.get('vowel_count', '0')}")
    
    # Name Interpretation Section
    st.markdown('<p class="main-header">👤 Name Interpretation</p>', unsafe_allow_html=True)
    
    interpretation = str(results['analyses'].get('interpretation', ''))
    if interpretation:
        try:
            # Split the text into sections
            sections = interpretation.split('\n\n')
            
            # Create two rows with three columns each
            row1_col1, row1_col2, row1_col3 = st.columns(3)
            row2_col1, row2_col2, row2_col3 = st.columns(3)
            
            # Overall Impression
            with row1_col1:
                st.markdown('<div class="interpretation-section">', unsafe_allow_html=True)
                st.markdown("### ✨ Overall Impression")
                for section in sections:
                    if 'Overall Impression:' in section:
                        content = section.split('Overall Impression:', 1)[1].strip()
                        st.markdown(f'<div class="interpretation-text">{content}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Key Strengths
            with row1_col2:
                st.markdown('<div class="interpretation-section">', unsafe_allow_html=True)
                st.markdown("### 💪 Key Strengths")
                for section in sections:
                    if 'Key Strengths:' in section:
                        content = section.split('Key Strengths:', 1)[1].strip()
                        for line in content.split('\n'):
                            if line.strip() and line.strip()[0].isdigit():
                                bullet_text = line.split('.', 1)[1].strip()
                                if ':' in bullet_text:
                                    header, desc = bullet_text.split(':', 1)
                                    st.markdown(f'<div class="bullet-header">{header}:</div>', unsafe_allow_html=True)
                                    st.markdown(f'<div class="bullet-content">{desc}</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f'<div class="bullet-content">• {bullet_text}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Growth Areas
            with row1_col3:
                st.markdown('<div class="interpretation-section">', unsafe_allow_html=True)
                st.markdown("### 🌱 Growth Areas")
                for section in sections:
                    if 'Growth Areas:' in section:
                        content = section.split('Growth Areas:', 1)[1].strip()
                        for line in content.split('\n'):
                            if line.strip() and line.strip()[0].isdigit():
                                bullet_text = line.split('.', 1)[1].strip()
                                if ':' in bullet_text:
                                    header, desc = bullet_text.split(':', 1)
                                    st.markdown(f'<div class="bullet-header">{header}:</div>', unsafe_allow_html=True)
                                    st.markdown(f'<div class="bullet-content">{desc}</div>', unsafe_allow_html=True)
                                else:
                                    st.markdown(f'<div class="bullet-content">• {bullet_text}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Life Path Insights
            with row2_col1:
                st.markdown('<div class="interpretation-section">', unsafe_allow_html=True)
                st.markdown("### 🌊 Life Path Insights")
                for section in sections:
                    if 'Life Path Insights:' in section:
                        content = section.split('Life Path Insights:', 1)[1].strip()
                        st.markdown(f'<div class="interpretation-text">{content}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
            
            # Deeper Analysis
            with row2_col2:
                st.markdown('<div class="interpretation-section">', unsafe_allow_html=True)
                st.markdown("### 🔮 Deeper Analysis")
                for section in sections:
                    if 'Deeper Analysis:' in section:
                        content = section.split('Deeper Analysis:', 1)[1].strip()
                        st.markdown(f'<div class="interpretation-text">{content}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error parsing interpretation: {str(e)}")
            st.write(interpretation)  # Fallback: display raw text
    else:
        st.warning("No interpretation available.")
    
    # Display frequency chart if available
    if 'frequencies' in results['analyses'].get('vibration', {}):
        st.subheader("📈 Frequency Pattern")
        frequencies = results['analyses']['vibration']['frequencies']
        st.plotly_chart(create_frequency_chart(frequencies), use_container_width=True)

def main():
    st.title("🔮 Name Analysis Tool")
    st.write("Discover the hidden patterns and meanings in names through numerology, phonetics, and vibration analysis.")
    
    # Get analyzer instance
    analyzer = get_analyzer()
    
    # Create input form
    with st.form("name_analysis_form"):
        name = st.text_input("Enter a name to analyze:")
        submitted = st.form_submit_button("Analyze")
    
    if submitted:
        if name and any(c.isalpha() for c in name):
            with st.spinner("Analyzing name patterns..."):
                try:
                    # Perform analysis
                    profile = analyzer.analyze_name(name)
                    
                    # Display results
                    display_results(profile)
                    
                except Exception as e:
                    st.error(f"An error occurred during analysis: {str(e)}")
        else:
            st.warning("Please enter a valid name containing letters.")
    
    # Add information about the tool
    with st.expander("About this tool"):
        st.write("""
        This tool combines various methods of name analysis:
        - **Numerology**: Calculates destiny numbers and life path numbers
        - **Vibration**: Analyzes the sound frequencies and resonance patterns
        - **Phonetics**: Examines the sound structure and pronunciation patterns
        
        The results are enhanced with AI-powered interpretation to provide meaningful insights.
        """)

if __name__ == "__main__":
    main()
