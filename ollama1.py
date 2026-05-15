import ollama

response = ollama.chat(
    model='deepseek-r1:1.5b',
    messages=[
        {
            'role': 'system',
            'content': (
                'You are a thinking assistant. '
                'Show your thinking before the final answer.'
            )
        },
        {
            'role': 'user',
            'content': (
                'are UFOs real '
            )
        }
    ]
)

print(response['message']['content'])