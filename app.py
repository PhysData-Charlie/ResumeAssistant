import streamlit as st
import openai
import json
from datetime import datetime
import os
from io import StringIO, BytesIO

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

        - When possible, rearrange or rephrase sentences so that the resume aligns as closely as poss