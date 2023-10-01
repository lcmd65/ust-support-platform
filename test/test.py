from app.api.openai import api_getting
import openai

def main():
    openai.api_key = api_getting()
    message = "hey"
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        return completion['choices'][0]['message']['content']
    except Exception as e:
        # Handle the exception gracefully
        return f"Failed to generate response: {e}"
    
if __name__ =="__main__":
    print(main())

