from ollama import chat


def conceptNet_synonyme(word):
    response = chat(model='rcra_synonyme', messages=[{'role': 'user', 'content': word}])
    return response['message']['content']
def conceptNet_resume(text):
    response = chat(model='rcra_resume', messages=[{'role' : 'user', 'content' : text}])
    return response['message']['content']



def synonyme(user_input):
    messages = [
    {
        'role': 'user',
        'content': 'car',
    },
    {
        'role': 'assistant',
        'content': "car",
    },
    {
        'role': 'user',
        'content': 'car',
    },
    {
        'role': 'assistant',
        'content': 'car',
    },
    ]
    response = chat(
        'rcra_synonyme',
        messages=messages
        + [
        {'role': 'user', 'content': user_input},
        ],
    )

    # Add the response to the messages to maintain the history
    messages += [
        {'role': 'user', 'content': user_input},
        {'role': 'assistant', 'content': response.message.content},
    ]
    return response.message.content + '\n'