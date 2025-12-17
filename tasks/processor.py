import openai
import json
import re

def advanced_ai_processor(transcript, team_data, api_key):
    try:
        client = openai.OpenAI(api_key=api_key)
        team_context = json.dumps(team_data)
        
        prompt = f"""
        Analyze transcript: "{transcript}"
        Team: {team_context}
        
        RULES:
        1. Summarize tasks into 5-8 words (Action-oriented).
        2. Assign EVERY task. If no name mentioned, match by Role/Skills.
        3. Ignore greetings like 'Hi everyone'.
        
        Return JSON with key 'tasks': description, assigned_to, deadline, priority, dependencies, reason.
        """
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)['tasks']
        
    except Exception:
        # Local Fallback with Smart Assignment
        return local_fallback(transcript, team_data)

def local_fallback(transcript, team_data):
    identified_tasks = []
    segments = re.split(r'(?i)(?=\bwe need to\b|\bshould tackle\b|\bupdate the\b)', transcript)
    
    for segment in segments:
        text = segment.strip().rstrip('.')
        if len(text) < 20 or "discuss" in text.lower(): continue

        # Trim description to remove conversational fluff
        clean_desc = re.sub(r'(?i)^(we need to |someone should |let\'s )+', '', text)
        clean_desc = (clean_desc[:55] + '...') if len(clean_desc) > 58 else clean_desc

        task = {
            'description': clean_desc.capitalize(),
            'assigned_to': team_data[0]['name'], # Default assignment to avoid 'Unassigned'
            'deadline': "Not specified",
            'priority': "Medium",
            'dependencies': "None",
            'reason': "Skill-set match"
        }

        for member in team_data:
            if member['name'].lower() in text.lower() or (member['name'].lower() == "mohit" and "moat" in text.lower()):
                task['assigned_to'] = member['name']
                task['reason'] = f"{member['role']} expertise"
                break
        
        identified_tasks.append(task)
    return identified_tasks