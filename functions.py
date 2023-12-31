
import os,uuid,json,PyPDF2
import numpy as np
from openai import OpenAI
import time
client = OpenAI()


assistant_id = "<assistantID>"
thread_id = '<ThreadID>'

def save_uploaded_file(uploaded_file):
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
       

def get_assistant_response(query):

    threadId = thread_id
    assistantId = assistant_id

    message = client.beta.threads.messages.create(
    thread_id=threadId,
    role="user",
    content=query
        )
    
    run = client.beta.threads.runs.create(
    thread_id=threadId,
    assistant_id=assistantId,
    instructions="Use the user uploaded file to provide answer. Do not answer if you couldn't find any context in the knowledgebase. Just say I don't know"
    )
    
    while True:

        ###### Check Run Status ######
        run = client.beta.threads.runs.retrieve(thread_id=threadId,run_id=run.id)
        time.sleep(1)
        
        ###### Perform Actions based on run status #####
        ###### If Run status is 'completed' it means return the recent output #####
        if run.status == 'completed':
            messages_ = client.beta.threads.messages.list(thread_id=threadId)
            response = messages_.data[0].content[0].text.value
            return response
        
       

def update_assistant_knowledgebase(filepath):

    my_assistant = client.beta.assistants.retrieve(assistant_id)
    file_ids = my_assistant.file_ids

    file = client.files.create(
    file=open(filepath, "rb"),
    purpose='assistants'
    )

    file_ids.append(file.id)

    my_updated_assistant = client.beta.assistants.update(
    assistant_id,
    tools=[{"type": "retrieval"}],
    file_ids=file_ids,
    )
    print("assistant_knowledgebase_updated")
    