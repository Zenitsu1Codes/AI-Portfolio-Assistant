from dotenv import load_dotenv
from groq import Groq
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr


load_dotenv(override=True)
groq = Groq()

def push(message):
    print(f"Push: {message}")
    # Replace 'your_topic' with your actual ntfy topic name
    ntfy_url = "https://ntfy.sh/Harry"
    
    # ntfy takes the message directly in the 'data' parameter
    requests.post(ntfy_url, data=message.encode('utf-8'))


def record_user_details(email, name="Name not provided", notes="not provided"):
    message = f"New Lead: {name} ({email}) - Notes: {notes}"
    

    push(message) # Calling the new ntfy function here
    
    return {"recorded": "ok"}

def record_unknown_question(question):
    # Constructing the message for the notification
    message = f"❓ Unknown Question: {question}"
    

    push(message)
    
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
         {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.groq = Groq()
        self.name = "Asarsa Harsh"
        reader = PdfReader("me/Harsh Asarsa.pdf")
        self.linkedin = ""
        for page in reader.pages:
            text = page.extract_text()
            if text:
                self.linkedin += text
        with open("me/summary.txt", "r", encoding="utf-8") as f:
            self.summary = f.read()


    def handle_tool_calls(self, tool_calls):
        results = []
        
            # Map tool names to class methods using self
        tool_mapping = {
            "record_user_details": self.record_user_details,
            "record_unknown_question": self.record_unknown_question
        }

        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            tool_id = tool_call.id
            arguments = json.loads(tool_call.function.arguments)

            print(f"Executing tool: {tool_name}", flush=True)

            # 1. Check if the tool exists in your mapping
            if tool_name in tool_mapping:
                try:
                    # Execute the class method with unpacked arguments
                    execution_result = tool_mapping[tool_name](**arguments)

                    # Ensure result is a string before passing to OpenAI
                    if isinstance(execution_result, (dict, list)):
                        content_string = json.dumps(execution_result)
                    else:
                        content_string = str(execution_result)

                except Exception as e:
                    # Catch internal function errors gracefully
                    content_string = json.dumps({"status": "error", "message": str(e)})
            else:
                # Handle cases where OpenAI hallucinates a tool name
                content_string = json.dumps({"status": "error", "message": f"Tool {tool_name} not found"})

            # 2. Append standard OpenAI tool response format
            results.append({
                "role": "tool", 
                "tool_call_id": tool_id,
                "content": content_string 
            })

        return results


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
        particularly questions related to {self.name}'s career, background, skills and experience. \
        Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
        You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
        Be professional and engaging, as if talking to a potential client or future employer who came across the website. "
        
        system_prompt += f"make sure to use your record_unknown_question tool if you don't know the answer to any question, . "
        system_prompt += f"If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        history = [{"role": h["role"], "content": h["content"]} for h in history]
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.groq.chat.completions.create(model="llama-3.3-70b-versatile", messages=messages, tools=tools)

            finish_reason = response.choices[0].finish_reason
            # if response.choices[0].finish_reason=="tool_calls":
            if finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    
    
if __name__ == "__main__":
    me = Me()
    gr.ChatInterface(me.chat, type="messages").launch()