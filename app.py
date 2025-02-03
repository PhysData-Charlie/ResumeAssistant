import streamlit as st
import openai
import json
from datetime import datetime
import os

class ResumeAssistant():

    def __init__(self, api_keys, log_id, model='gpt-3.5-turbo', max_tokens=1024, temperature=0.3, log=False, debug=False):
        # openai
        self.api_key = api_keys
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        # job
        self.name = None
        self.field = None
        self.resume = None
        self.job_desc = None
        # misc
        self.log_file = f'log_{log_id}.txt'
        self.log = log
        self.debug = debug # debug mode
        if self.log:
            if not os.path.exists(self.log_file):
                with open(self.log_file, 'w') as f:
                    print('')


    def set_apikey(self, api_key):
        self.api_key = api_key

    def config_model(self, temperature, max_tokens):
        self.temperature = temperature
        self.max_tokens = max_tokens

    def set_info(self, name, field, resume, job_desc):
        self.name = name
        self.field = field
        self.resume = resume
        self.job_desc = job_desc

    def prompt_resume(self):

        prompt = f'''
        Based on the following job description:
    
        {self.job_desc}

        And based on the following resume:

        {self.resume}

        Suggest potential improvements for the CV. You need to consider the following:

        - When possible, rearrange or rephrase sentences so that the resume aligns as closely as possible with the job description.
        - When possible, bullet points should follow the STAR format.
        - Improve wording but do not generate new information, modify only based on the resume.
        - Consider that the CV will be pased through an ATS filter and thus must comply for readability.\
        - Do not increase the maxium word count, resume should fit within 2 pages (between 700 and 1200 words).
        '''

        return prompt

    def prompt_letter(self):

        prompt = f'''
        Based on the following job description:
        
        {self.job_desc}

        And based on the following resume:

        {self.resume}

        Prepare a motivation letter to apply for this job, with applicant name {self.name}. Only write the contents of the letter, do not worry about sender/recipient/adress information.

        '''

        return prompt

    def prompt_question(self):

        prompt = f'''
        Based on the following job description:
        
        {self.job_desc}

        And based on the following resume:

        {self.resume}

        Prepare a total of 9 questions to prepare for a job interview. Provide both the questions and potential answers based on the information from the resume.

        - 3 general questions
        - 3 behavioral questions
        - 3 technical questions
        '''

        return prompt

    def get_response(self, prompt):

        messages = [
            {"role": "system", "content": f"You're a helpful assistant helping a {self.field} candidate prepare for a job application."},
            {"role" : "user", "content": prompt}
        ]
        if not self.debug:
            try:
                client = openai.OpenAI(api_key=self.api_key)
                client.models.list() # check if working API was provided
                try:
                        response = client.chat.completions.create(
                            model=self.model,
                            messages=messages,
                            temperature=self.temperature,
                            max_tokens=self.max_tokens,
                        )
                        response = response.choices[0].message.content
                except Exception as e:
                    self.   logger(f'Error 402: {e}')
                    return 402 # response generation error
            except Exception as e:
                self.logger(f'Error 401: {e}')
                return 401 # client initialization error
        else:
                response = f'''
                This is example test to test the functionality of the app. Here's the prompt used:
                
                {prompt}
                '''
        
        return response
    
    def read_pdf(self):
        return None
    
    def prepare_letter(self):
        return None
    
    def prepare_questions(self):
        return None
    
    def logger(self, message):
        if self.log:
            with open(self.log_file, 'a') as f:
                f.write(message)


# initialization
identifier = datetime.now().strftime('%Y-%m-$d_%H-%M-%S')
assistant = ResumeAssistant(api_keys=None, log_id=identifier, log=False, debug=False)
st.set_page_config(page_title="Resume Assistant App v.1.0")

# sidebar
with st.sidebar:
    st.title('Resume Assistant')
    st.markdown('''
                ## About
                GPT-powered AI assistant to help you streamlit your job application process. Includes:
                - Resume enhancer
                - Cover letter generator
                - Interview Q&A generator
                ''')
    if 'api_key' not in st.session_state:
        api_key = st.text_input('API_KEY (paste and press Enter):', '')
        st.session_state['api_key'] = api_key
    else:
        api_key = st.text_input('API_KEY:', st.session_state['api_key'])
        st.session_state['api_key'] = api_key

    if 'temperature' not in st.session_state:
        temperature = st.slider('Model Creativity (less to more creative):', min_value=0.0, max_value=1.0, step=0.1, value=0.3)
        st.session_state['temperature'] = temperature
    else:
        temperature = st.slider('Model Creativity (less to more creative)   :', min_value=0.0, max_value=1.0, step=0.1, value=st.session_state['temperature'])
        st.session_state['temperature'] = temperature

    if 'max_tokens' not in st.session_state:
        max_tokens = st.slider('Max Output Tokens (4 word approx. 1 token):', min_value=256, max_value=2048, step=64, value=512)
        st.session_state['max_tokens'] = max_tokens
    else:
        max_tokens = st.slider('Max Output Tokens (4 word approx. 1 token):', min_value=256, max_value=2048, step=64, value=st.session_state['max_tokens'])
        st.session_state['max_tokens'] = max_tokens

    st.markdown('''
                ### Recommended parameters:
                - Resume enhancer - (Max Output Tokens: 512-1024), (Temperature: 0.0-0.2)
                - Cover letter generator - (Max Output Tokens: 512-640), (Temperature: 0.2-0.5)
                - Interview Q&A generator - (Max Output Tokens: 1216-2048), (Temperature: 0.3-0.7)
                ''')

    st.write('Made by PhysCharlieData')

    st.text('Warning: generating a new response will overwrite any previous data.')

# main form
st.title('Resume Assistant App v.1.0')

# user input
if 'name' not in st.session_state:
    name = st.text_input("Name: write your name", "John Doe")
    st.session_state['name'] = name
else:
    name = st.text_input("Name: write your name", st.session_state['name'])
if 'field' not in st.session_state:
    field = st.text_input("Title: Specify your job title (e.g. Data Scientist, Data Analyst, Machine Learning Engineer)", "Data Scientist")
    st.session_state['field'] = field
else:
    field = st.text_input("Title: Specify your job title (e.g. Data Scientist, Data Analyst, Machine Learning Engineer)", st.session_state['field'])
if 'resume_txt' not in st.session_state:
    resume_txt = st.text_area("Resume: Copy-and-paste your resume here", '')
    st.session_state['resume_txt'] = resume_txt
else:
    resume_txt = st.text_area("Resume: Copy-and-paste your resume here:", st.session_state['resume_txt'])
if 'job_txt' not in st.session_state:
    job_txt = st.text_area("Job Description: Copy-and-past the job description here:", '')
    st.session_state['job_txt'] = job_txt
else:
    job_txt = st.text_area("Job Description: Copy-and-past the job description here:", st.session_state['job_txt'])


# action buttons
col1, col2, col3 = st.columns(3)

with col1:
    action1 = st.button('How to Improve your Resume')
with col2:
    action2 = st.button('Generate a Cover Letter')
with col3:
    action3 = st.button('Prepare Q&A for an interview')

if action1:
    flag = 0
    
    if api_key == '':
        st.warning('Please enter API key to proceed!')
    else:
        flag += 1 
    if name == '':
        st.warning('Name cannot be empty!')
    else:
        flag += 1
    if field == '':
        st.warning('Title cannot be empty!')
    else:
        flag += 1
    if resume_txt == '':
        st.warning('Resume cannot be empty!')
    else:
        flag += 1
    if job_txt == '':
        st.warning('Job description cannot be empty!')
    else:
        flag += 1

    if flag == 5:
        with st.spinner('Generating...'):
            assistant.set_apikey(st.session_state['api_key'])
            assistant.config_model(st.session_state['temperature'], st.session_state['max_tokens'])
            assistant.set_info(name, field, resume_txt, job_txt)
            prompt = assistant.prompt_resume()
            res = assistant.get_response(prompt)
        if isinstance(res, int):
            if res == 401:
                st.warning('Error connecting with API Key provided. Please check that your API Key is correct and active. (Code error 401)')
                st.warning('API_KEY:'+ st.session_state['api_key'])
            elif res == 402:
                st.warning('Error connection to OpenAI. Please try again later or check OpenAI status. (Code error 402)')
        else:
            st.text_area('Suggestions to improve your resume:', res, height=700)
            if 'response' not in st.session_state:
                st.session_state['response'] = res

if action2:
    flag = 0

    if api_key == '':
        st.warning('Please enter API key to proceed!')
    else:
        flag += 1 
    if name == '':
        st.warning('Name cannot be empty!')
    else:
        flag += 1
    if field == '':
        st.warning('Title cannot be empty!')
    else:
        flag += 1
    if resume_txt == '':
        st.warning('Resume cannot be empty!')
    else:
        flag += 1
    if job_txt == '':
        st.warning('Job description cannot be empty!')
    else:
        flag += 1
    
    if flag == 5:
        with st.spinner('Generating...'):
            assistant.set_apikey(st.session_state['api_key'])
            assistant.config_model(st.session_state['temperature'], st.session_state['max_tokens'])
            assistant.set_info(name, field, resume_txt, job_txt)
            prompt = assistant.prompt_letter()
            res = assistant.get_response(prompt)
            if isinstance(res, int):
                if res == 401:
                    st.warning('Error connecting with API Key provided. Please check that your API Key is correct and active. (Code error 401)')
                    st.warning('API_KEY:'+ st.session_state['api_key'])
                elif res == 402:
                    st.warning('Error connection to OpenAI. Please try again later or check OpenAI status. (Code error 402)')
            else:
                st.text_area('Suggested cover letter:', res, height=700)
                if 'response' not in st.session_state:
                    st.session_state['response'] = res

if action3:
    flag = 0
    
    if api_key == '':
        st.warning('Please enter API key to proceed!')
    else:
        flag += 1 
    if name == '':
        st.warning('Name cannot be empty!')
    else:
        flag += 1
    if field == '':
        st.warning('Title cannot be empty!')
    else:
        flag += 1
    if resume_txt == '':
        st.warning('Resume cannot be empty!')
    else:
        flag += 1
    if job_txt == '':
        st.warning('Job description cannot be empty!')
    else:
        flag += 1
    
    if flag == 5:
        with st.spinner('Generating...'):
            assistant.set_apikey(st.session_state['api_key'])
            assistant.config_model(st.session_state['temperature'], st.session_state['max_tokens'])
            assistant.set_info(name, field, resume_txt, job_txt)
            prompt = assistant.prompt_question()
            res = assistant.get_response(prompt)
            if isinstance(res, int):
                if res == 401:
                    st.warning('Error connecting with API Key provided. Please check that your API Key is correct and active. (Code error 401)')
                    st.warning('API_KEY:'+ st.session_state['api_key'])
                elif res == 402:
                    st.warning('Error connection to OpenAI. Please try again later or check OpenAI status. (Code error 402)')
            else:
                st.text_area("Suggested Q&A for your job interview", res, height=700)
                if 'response' not in st.session_state:
                    st.session_state['response'] = res

# download
if 'response' in st.session_state:
    st.download_button(
        label='Download results as TXT',
        data=st.session_state['response'],
        file_name=f'results_{identifier}.txt',
        mime='text/csv'
    )
