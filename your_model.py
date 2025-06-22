class DummyChat:
    def __init__(self):
        self.history = [{"role": "system", "parts": [{"text": "Hello! I'm Buzaato AI."}]}]

    def send_message(self, message):
        self.history.append({"role": "user", "parts": [{"text": message}]})
        response = {"role": "assistant", "parts": [{"text": f"Echo: {message}"}]}
        self.history.append(response)
        return type("Response", (), {"text": response["parts"][0]["text"]})

    def start_chat(self, history=None):
        return self

model = DummyChat()
BUZAATO_CONTEXT = "You're Buzaato AI — a helpful assistant for menus, delivery, discounts, and more!"
