import streamlit as st
import openai
from utils.constants import model_family_mapping, model_name_mapping
from utils.utils import PitchPerfect, pdf_loader

st.set_page_config(
    page_title = "Pitch Perfect",
    page_icon = "📝",
    layout = "wide"
)

def initialize_session_state():
    
    if 'api_configured' not in st.session_state:
        st.session_state.api_configured = False
        
    if 'pitch_perfect' not in st.session_state:
        st.session_state.pitch_perfect = None

initialize_session_state()        

with st.sidebar:
    st.title("Model API Configuration")
    
    model_options = [
        "GPT-4o mini",
        "GPT-4o",
        "o1",
        "o3-mini",
        "Deepseek-V3",
        "Deepseek-r1",
        "Mistral Small 24B",
        "LLaMa 3.3 70B",
        "DeepSeek R1 Distill",
        "Mistral 7B v0.3"
    ]
    selected_model = st.selectbox("Select which LLM to use", model_options, key = "selected_model")
    model_name = model_name_mapping.get(selected_model)
    model_family = model_family_mapping.get(selected_model)
    
    if model_family == "gpt":
        token = st.text_input("OpenAI API Key", type="password", key="openai_key")
    else:
        token = st.text_input("Hugging Face Token", type="password", key="hf_token")
    
    if token != "":
        if st.button("Initialize with the provided keys"):
            try:
                st.session_state.pitch_perfect = PitchPerfect(model = model_name, model_family = model_family, token = token)
                if st.session_state.pitch_perfect.client == "INVALID":
                    st.error(st.session_state.pitch_perfect.error)
                else:
                    st.session_state.api_configured = True
                    st.success("Successfully configured the API clients with provided keys!")
            
            except Exception as e:
                st.error(f"Error initializing API clients: {str(e)}")
                st.session_state.api_configured = False
            
    if st.session_state.api_configured:
        upload_cv = st.file_uploader("Upload CV in PDF format", type=["pdf"])
        if upload_cv is not None:
            st.success(f"File uploaded successfully: {upload_cv.name}")
    
            temp_file = "./temp.pdf"
            with open(temp_file, "wb") as file:
                file.write(upload_cv.getvalue())
                file_name = upload_cv.name
    
            cv_data  = pdf_loader(temp_file)
    
if not st.session_state.api_configured:
    st.warning("Please configure the models in the sidebar to proceed")
    st.stop()
    
st.title("Pitch Perfect")
st.subheader("A cutting-edge app that crafts the perfect cover letter, tailored to land your dream job effortlessly!")

col1, col2 = st.columns(2)

# with col1:
#     upload_cv = st.file_uploader("Upload CV in PDF format", type=["pdf"])
#     if upload_cv is not None:
#         st.success(f"File uploaded successfully: {upload_cv.name}")
        
#         temp_file = "./temp.pdf"
#         with open(temp_file, "wb") as file:
#             file.write(upload_cv.getvalue())
#             file_name = upload_cv.name
        
#         cv_data  = pdf_loader(temp_file)
    
with col1:
    job_title = st.text_input("Job Title", key="job_title")
    
with col2:
    company_name = st.text_input("Company Name", key="company_name")

# if upload_cv:
#     st.write(cv_data)

job_description = st.text_area("Please paste the entire job description here:")

if st.button("Generate Cover Letter"):
    with st.spinner("Generating Cover Letter....."):
        client = st.session_state.pitch_perfect
        cover_letter, reason = client.generate_cover_letter(job_title = job_title, 
                                                    company = company_name, 
                                                    job_desc = job_description,
                                                    cv_data = cv_data)
    
    st.success("Cover Letter Generated")
    st.markdown(cover_letter)
    with st.expander("Model Reasoning:"):
        st.write(reason) 