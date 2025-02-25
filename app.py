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

def plot_consonant_vowel_ratio(consonants, vowels):
    """Create a pie chart showing consonant/vowel distribution."""
    fig = go.Figure(go.Pie(
        labels=['Consonants', 'Vowels'],
        values=[consonants, vowels],
        hole=0.4,
        marker=dict(colors=['#6C63FF', '#FF6F61'])
    ))
    fig.update_layout(
        title="Consonant vs Vowel Distribution",
        template="plotly_white",
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig

def display_results(profile):
    """Display analysis results."""
    results = profile.get_report()
    
    # Custom CSS for styling
    st.markdown("""
        <style>
        [data-testid="stMetricValue"] {
            font-size: 2.2rem !important;
            font-weight: bold !important;
        }
        [data-testid="stMetricLabel"] {
            font-size: 1.1rem !important;
            font-weight: 600 !important;
        }
        .stAlert {
            background-color: rgba(108, 99, 255, 0.1) !important;
            border: none !important;
        }
        [data-testid="stMarkdownContainer"] > div > div {
            padding: 0.5rem !important;
        }
        [data-testid="stHeader"] {
            background-color: transparent !important;
        }
        [data-testid="stTabsHeader"] {
            background-color: transparent !important;
            margin-bottom: 2rem !important;
        }
        [data-testid="stVerticalBlock"] {
            gap: 2rem !important;
        }
        .stTabs [data-testid="stMarkdownContainer"] p {
            font-size: 1rem !important;
            margin-bottom: 1rem !important;
        }
        .element-container {
            margin-bottom: 1rem !important;
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
    
    # Create tabs for organized results
    tab1, tab2, tab3 = st.tabs(["📊 Analysis", "🔮 Interpretation", "📈 Visualizations"])

    with tab1:
        st.markdown("### Name Analysis Results")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Create two-column layout for metrics
        col1, col2 = st.columns(2)
        
        # Combined Numerological & Phonetic Analysis
        with col1:
            st.markdown("#### 🔢 Numerology & Phonetics")
            col1a, col1b = st.columns(2)
            with col1a:
                st.metric("Destiny Number", 
                         results['analyses']['numerology'].get('destiny_number', 'Unknown'))
            with col1b:
                phonetics = results['analyses']['phonetics']
                st.metric("Consonants/Vowels",
                         f"{phonetics.get('consonant_count', '0')}/{phonetics.get('vowel_count', '0')}")
        
        # Vibrational Analysis
        with col2:
            st.markdown("#### 🌊 Vibrational Analysis")
            col2a, col2b = st.columns(2)
            with col2a:
                st.metric("Base Frequency",
                        f"{results['analyses']['vibration'].get('base_frequency', 'Unknown')} Hz")
            with col2b:
                if 'resonance_strength' in results['analyses']['vibration']:
                    st.metric("Resonance Profile",
                            results['analyses']['vibration'].get('resonance_strength', 'Unknown'))
        
        # LLM Insights in a container
        with st.container():
            st.markdown("---")
            st.markdown("#### 🤖 AI-Generated Interaction Insights")
            st.info("""
            Based on the name analysis above, this section will provide personalized suggestions for:
            - Communication style preferences
            - Potential interaction approaches
            - Relationship building strategies
            """)

    with tab2:
        interpretation = str(results['analyses'].get('interpretation', ''))
        if interpretation:
            try:
                # Split the text into sections
                sections = interpretation.split('\n\n')
                
                # Overall Impression
                st.markdown("### ✨ Overall Impression")
                for section in sections:
                    if 'Overall Impression:' in section:
                        content = section.split('Overall Impression:', 1)[1].strip()
                        st.markdown(content)
                
                # Two-column layout for strengths and growth areas
                col1, col2 = st.columns(2)
                
                # Key Strengths
                with col1:
                    st.markdown("### 💪 Key Strengths")
                    for section in sections:
                        if 'Key Strengths:' in section:
                            content = section.split('Key Strengths:', 1)[1].strip()
                            for line in content.split('\n'):
                                if line.strip() and line.strip()[0].isdigit():
                                    bullet_text = line.split('.', 1)[1].strip()
                                    st.markdown(f"• {bullet_text}")
                
                # Growth Areas
                with col2:
                    st.markdown("### 🌱 Growth Areas")
                    for section in sections:
                        if 'Growth Areas:' in section:
                            content = section.split('Growth Areas:', 1)[1].strip()
                            for line in content.split('\n'):
                                if line.strip() and line.strip()[0].isdigit():
                                    bullet_text = line.split('.', 1)[1].strip()
                                    st.markdown(f"• {bullet_text}")
                
                # Additional Insights
                st.markdown("---")
                
                # Life Path and Deeper Analysis in columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("### 🌊 Life Path Insights")
                    for section in sections:
                        if 'Life Path Insights:' in section:
                            content = section.split('Life Path Insights:', 1)[1].strip()
                            st.markdown(content)
                
                with col2:
                    st.markdown("### 🔮 Deeper Analysis")
                    for section in sections:
                        if 'Deeper Analysis:' in section:
                            content = section.split('Deeper Analysis:', 1)[1].strip()
                            st.markdown(content)
                            
            except Exception as e:
                st.error(f"Error parsing interpretation: {str(e)}")
                st.write(interpretation)
        else:
            st.warning("No interpretation available.")

    with tab3:
        st.subheader("Visual Analysis")
        
        # Create two-column layout for charts
        col1, col2 = st.columns(2)
        
        with col1:
            # Consonant/Vowel Distribution
            phonetics = results['analyses']['phonetics']
            consonants = phonetics.get('consonant_count', 0)
            vowels = phonetics.get('vowel_count', 0)
            st.plotly_chart(plot_consonant_vowel_ratio(consonants, vowels), use_container_width=True)
        
        with col2:
            # Frequency Pattern
            if 'frequencies' in results['analyses'].get('vibration', {}):
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
