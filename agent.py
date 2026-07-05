import os
import json
import ollama
from dotenv import load_dotenv
from tools import generate_docx

# Load environment variables (if any needed for other parts, though Ollama runs locally)
load_dotenv()

SYSTEM_PROMPT = """
You are an autonomous AI engineering assistant. Your ONLY job is to draft business documents and save them by calling the `generate_docx` tool.

CRITICAL INSTRUCTIONS:
1. Figure out a good title for the document based on the request.
2. Draft the full content (sections, headings, paragraphs) and format it as a JSON string.
3. IMMEDIATELY call the `generate_docx` tool to save the document. 
"""

def process_request(request: str) -> dict:

    
    augmented_request = request + "\n\nCRITICAL: Do NOT ask me for the title or content. Make it up yourself and call `generate_docx`!"
    
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': augmented_request}
    ]
    
    print(f"Sending request to Ollama: {augmented_request}")
    try:
        response = ollama.chat(
            model='llama3.1',
            messages=messages,
            tools=[generate_docx],
        )
    except Exception as e:
        return {
            "agent_message": f"Error communicating with Ollama: {str(e)}\n\nMake sure Ollama is running and you have pulled the model (`ollama pull llama3.1`).",
            "document_url": None
        }
    
    document_url = None
    final_message = "Error: The AI did not generate a document."
    
    # Check if the agent called the tool
    if response.get('message', {}).get('tool_calls'):
        for tool_call in response['message']['tool_calls']:
            if tool_call['function']['name'] == 'generate_docx':
                args = tool_call['function']['arguments']
                title = args.get("title", "Generated_Document")
                sections = args.get("sections_json_string", "")
                
                # Execute our tool to actually create the docx file
                document_url = generate_docx(title, sections)
                
                final_message = f"Success! The document '{title}' has been generated locally by Ollama and saved at {document_url}."
                break 
    else:
        text_resp = response.get('message', {}).get('content', 'No text response')
        final_message = f"Warning: Agent failed to call the document generation tool. Ollama replied: {text_resp}"

    return {
        "agent_message": final_message,
        "document_url": document_url
    }
