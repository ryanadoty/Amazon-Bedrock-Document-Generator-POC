import boto3
import os
import json
import botocore.config
from dotenv import load_dotenv

# loading environment variables
load_dotenv()
# configure Bedrock client
boto3.setup_default_session(profile_name=os.getenv("profile_name"))
config = botocore.config.Config(connect_timeout=120, read_timeout=120)
bedrock = boto3.client('bedrock-runtime', 'us-east-1', endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com',
                       config=config)




# Invoke LLM - Bedrock - Creates the Docuemnt based on user feedback
def invoke_llm(bedrock, user_input, doc_template):
    # Uses the Bedrock Client, the user input, and the document template as part of the prompt



    ##Setup Prompt
    prompt_data = f"""

Human:

Generate a document based on the user input and the instructions and format provided in the Document Template below  
The tehcnical document should be human readable, well formatted, and broken into the relveant sections.
Response should be in valid Markdown syntax 
###

<Document_Template>
{doc_template}
</Document_Template>
###
<User_Input>
{user_input}
</User_Input>
###

Assistant: Here is a draft based on the provided user input and template

"""
    # Add the prompt to the body to be passed to the Bedrock API
    # Also adds the hyperparameters

    body = json.dumps({"prompt": prompt_data,
                       "max_tokens_to_sample": 5000,
                       "temperature": .2,
                       "stop_sequences": []
                       })

    # Run Inference
    modelId = "anthropic.claude-v2"  # change this to use a different version from the model provider if you want to switch
    accept = "application/json"
    contentType = "application/json"
    # Call the Bedrock API
    response = bedrock.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )

    # Parse the Response
    response_body = json.loads(response.get('body').read())
    llmOutput = response_body.get('completion')

    print(llmOutput)

    # Return the LLM response
    return llmOutput


# Invoke LLM - Bedrock - Specifically for Refining the results based on user feedback
def invoke_llm_refine(bedrock, user_feedback, previous_version, doc_template):
    ##Setup Prompt
    prompt_data = f"""

Human:

Refine and Adjust the provided document based on the user feedback and following structure and format guidelines in the Document Template
Response should be in valid Markdown syntax 

###
<document_to_be_refined>
{previous_version}
</document_to_be_refined>

<User_feedback>
{user_feedback}
</User_feedback>

<Document_Template>
{doc_template}
</Document_Template>
###

Assistant: Here is a modified draft press release based on the provided user feedback

"""

    # Add the prompt to the body to be passed to the Bedrock API
    # Also adds the hyperparameters

    body = json.dumps({"prompt": prompt_data,
                       "max_tokens_to_sample": 5000,
                       "temperature": .2,
                       "stop_sequences": []
                       })

    # Run Inference
    modelId = "anthropic.claude-v2"  # change this to use a different version from the model provider if you want to switch
    accept = "application/json"
    contentType = "application/json"

    # Call Bedrock API
    response = bedrock.invoke_model(
        body=body, modelId=modelId, accept=accept, contentType=contentType
    )
    # Parse Response
    response_body = json.loads(response.get('body').read())
    llmOutput = response_body.get('completion')

    print(llmOutput)
    # Return the LLM response
    return llmOutput


def generate_doc(user_input):
    doc_template = """
    (Press release Style Headline -should be in bold)
    	(Subheader Title: A one sentence summary)
    (LOCATION) - (DATE) - (First paragraph: summary of the service/product/feature "launch")
    (Second Paragraph: The second paragraph explains the opportunity or problem that needs to be solved)
    (The third paragraph gives the approach or the solution.)
    (The fourth paragraph quotes an Internal leader.)
    (The fifth paragraph describes the customer experience - how users will discover and use what you propose)
    (The sixth paragraph includes a specific, believable, human-sounding customer testimonial.)
    (The seventh paragraph directs the reader where to go to get started)
    #

    Customer FAQ's 
    [This section will consist of questions and answers relevant to customers and user]
    1. [Question]
    	A: [Answer to Question]
    2. [Question]
    	A: [Answer to Question]
    …
    X. [Question]
    	A: [Answer to Question]

    StakeHolder FAQ's 
    [This section will consist of questions and answers relevant to customers and user]
    1. [Question - Should be professional and concise]
    	A: [Answer to Question - should be professional and relevant]
    2. [Question]
    	A: [Answer to Question]
    …
    X. [Question]
    	A: [Answer to Question]

    Appendices
    [If you used specific data points or references in the section describing your approach, include more complete data set as an appendix. Add relevant well sourced data points and studies]
    Appendix A: (Studies, statistics and Supporting evidence reference material directly relevant to your Press Release - should be detailed, relevant and well sourced)

    Appendix B: (Studies, statistics and Supporting evidence reference material directly relevant to your Press Release - should be detailed, relevant and well sourced)
    …
    Appendix X: (Studies, statistics and Supporting evidence reference material directly relevant to your Press Release - should be detailed, relevant and well sourced)
    """
    # Setup bedrock client
    # bedrock = boto3.client('bedrock-runtime', 'us-east-1', endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com')

    # invoke LLM
    llmOutput = invoke_llm(bedrock, user_input, doc_template)
    return llmOutput


def refine_doc(llm_output, user_refine):
    doc_template = """
        (Press release Style Headline -should be in bold)
        	(Subheader Title: A one sentence summary)
        (LOCATION) - (DATE) - (First paragraph: summary of the service/product/feature "launch")
        (Second Paragraph: The second paragraph explains the opportunity or problem that needs to be solved)
        (The third paragraph gives the approach or the solution.)
        (The fourth paragraph quotes an Internal leader.)
        (The fifth paragraph describes the customer experience - how users will discover and use what you propose)
        (The sixth paragraph includes a specific, believable, human-sounding customer testimonial.)
        (The seventh paragraph directs the reader where to go to get started)
        #

        Customer FAQ's 
        [This section will consist of questions and answers relevant to customers and user]
        1. [Question]
        	A: [Answer to Question]
        2. [Question]
        	A: [Answer to Question]
        …
        X. [Question]
        	A: [Answer to Question]

        StakeHolder FAQ's 
        [This section will consist of questions and answers relevant to customers and user]
        1. [Question - Should be professional and concise]
        	A: [Answer to Question - should be professional and relevant]
        2. [Question]
        	A: [Answer to Question]
        …
        X. [Question]
        	A: [Answer to Question]

        Appendices
        [If you used specific data points or references in the section describing your approach, include more complete data set as an appendix. Add relevant well sourced data points and studies]
        Appendix A: (Studies, statistics and Supporting evidence reference material directly relevant to your Press Release - should be detailed, relevant and well sourced)

        Appendix B: (Studies, statistics and Supporting evidence reference material directly relevant to your Press Release - should be detailed, relevant and well sourced)
        …
        Appendix X: (Studies, statistics and Supporting evidence reference material directly relevant to your Press Release - should be detailed, relevant and well sourced)
        """
    # Setup Clients
    # bedrock client
    # bedrock = boto3.client('bedrock-runtime', 'us-east-1', endpoint_url='https://bedrock-runtime.us-east-1.amazonaws.com')

    # invoke LLM
    llmOutput = invoke_llm_refine(bedrock,user_refine, llm_output, doc_template)
    return llmOutput