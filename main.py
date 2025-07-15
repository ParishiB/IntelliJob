from flask import Flask, request, jsonify
from datetime import datetime

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
        insert_message_into_db(thread_id, user_id, user_input, 1 , datetime.now(), datetime.now())
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
            agents = ['Booking_Agent', 'Broker_Agent', 'Default_Agent', 'Profile_Agent']
            for agent in agents:
                if agent in s:
                    messages = s[agent].get('messages', [])
                    print(f"Messages from {agent}: {messages}")  
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
        print(f"==========================================Combined response to be saved: {combined_response}==========================================")

        connection = get_db_connection()
        if connection is None:
            print("Failed to establish a database connection.")
            return jsonify({"error": "Database connection error."}), 500
        save_chat_messages(thread_id, user_id, user_input, combined_response)    
        return jsonify({"content": combined_response})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
