from flask import Flask, request, jsonify
from datetime import datetime
from redis_db import set_user_id
from graph import graph
from langchain_core.messages import HumanMessage, AIMessage

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'user_input' not in data:
            return jsonify({"error": "Invalid input, 'user_input' is required."}), 400
        user_input = data['user_input']
        user_id = data['user_id']
        thread_id = data['user_id']
        set_user_id(user_id)
        config = {
            "configurable": {
                "thread_id": thread_id,
                "user_id": user_id,
            }
        }
        assistant_responses = []
        print("Starting graph stream processing...")
        for s in graph.stream(
            {
                "messages": [
                    HumanMessage(content=user_input),
                ],
            },
            config
        ):
            agents = ['Resume_Agent', 'Job_Agent', 'Study_Agent', 'Default_Agent']
            for agent in agents:
                if agent in s:
                    messages = s[agent].get('messages', [])
                    for message in messages:
                        if isinstance(message, AIMessage):
                            assistant_responses.append(message.content)
                            print(f"Assistant response added: {message.content}") 

            if 'supervisor' in s:
                print(f"[System: {s['supervisor']['next']}]")

        if not assistant_responses:
            default_response = []
            for s in graph.stream(
                {
                    "messages": [
                        HumanMessage(content=user_input),
                    ],
                },
                {**config, "configurable": {"user_id": user_id, "thread_id": thread_id, "agent": "Default_Agent"}}
            ):
                if 'Default_Agent' in s:
                    messages = s['Default_Agent'].get('messages', [])
                    for message in messages:
                        if isinstance(message, AIMessage):
                            default_response.append(message.content)

            assistant_responses = default_response if default_response else ["No response from Default Agent."]

        combined_response = "\n".join(assistant_responses)  
        return jsonify({"content": combined_response})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
