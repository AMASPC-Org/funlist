
import os
import anthropic

def test_anthropic_connection():
    try:
        client = anthropic.Client(api_key=os.getenv('ANTHROPIC_API_KEY'))
        # Test with a simple message
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            messages=[
                {"role": "user", "content": "Hello Claude, please respond with 'Connection successful'"}
            ]
        )
        print("API Connection Test:", message.content)
        return True
    except Exception as e:
        print("Error connecting to Anthropic API:", str(e))
        return False

if __name__ == "__main__":
    test_anthropic_connection()
