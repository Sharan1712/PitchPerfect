from langchain_community.document_loaders import PyPDFLoader
from huggingface_hub import InferenceClient
from openai import OpenAI
from utils.constants import system_prompt

def pdf_loader(file):
    loader = PyPDFLoader(file)
    cv_data = ""

    for page in loader.lazy_load():
        cv_data += page.page_content
    # print(cv_data)

    return cv_data

class PitchPerfect:
    
    def __init__(self, model, model_family, token, system_prompt = system_prompt):
        
        self.system_prompt = system_prompt
        self.model = model
        
        if model_family == "gpt":
            self.client = OpenAI(api_key = token)
        elif model_family == "together":
            self.client = InferenceClient(provider = "together", api_key = token)
        else:
            self.client = InferenceClient(provider="hf-inference", api_key = token)
            
        
            
    def prepare_user_prompt(self, job_title, company, job_desc, cv_data, word_limit):
        
        user_prompt = (
            f"Job Title: {job_title}\n"
            f"Company Name: {company}\n"
            f"Job Description: {job_desc}\n\n"
            f"CV Data: {cv_data}\n\n"
            f"""
            Instructions:
            Based on the job description and the CV Data, write a concise cover letter in under {word_limit} words, following this format and structure and using a positive and humble tone.

            Include in Your Cover Letter:
            Start with: "Hi [hiring manager's name],"

            Introduce yourself as a graduate from [name of your university], looking for a role as a [Job Title]. Add 2 lines of brief introduction of my profile.

            Begin a new paragraph with: "Here are reasons that make me a great fit for the role:". 

            List at least 4 reasons based on the requirements from the job description, where these should be in the order that are in the job description. Explain how my skills align with the role's requirements (Include impactful numbers and results from my CV to show alignment)

            Conclude with: "Please find my CV attached below. I look forward to hearing from you."
            End with: "Best wishes, [Your Name]"


            Example Cover Letter:

            Hi [Hiring Manager's Name],

            I am a recent MSc Management graduate from [University Name], looking for a role as a [Job Title].

            Here are the reasons that make me a great fit for the role:

            [First reason, based on experience or passion related to the job. Include the quantifiable impact I made]
            [Second reason, highlighting skills or achievements. Include the quantifiable impact I made]
            [Third reason, highlighting skills or achievements. Include the quantifiable impact I made]
            [Fourth reason, highlighting skills or achievements. Include the quantifiable impact I made]
            Please find my CV attached below. I look forward to hearing from you.

            Best wishes,
            [Your Name]

            """
        )
        
        return user_prompt
    
    def generate_cover_letter(self, job_title, company, job_desc, cv_data, word_limit = 400, temp = 0.7, top_p = 0.9):
        
        user_prompt = self.prepare_user_prompt(job_title, company, job_desc, cv_data, word_limit)
        
        messages = [
            {"role" : "system", "content" : self.system_prompt},
            {"role" : "user", "content" : user_prompt}
        ]
        
        response = self.client.chat.completions.create(
            model = self.model, 
            messages = messages,
            temperature = temp,
            top_p = top_p
        )
        
        cover_letter = response.choices[0].message.content
        
        if "<think>" in cover_letter:
            reason = cover_letter.split("</think>")[0].replace("<think>","")
            cover_letter = cover_letter.split("</think>")[1]
        else:
            reason = "This model doesn't offer reasoning."
        
        return cover_letter, reason
        
        

    