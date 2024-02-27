import tkinter as tk
from openai import OpenAI

class QuerriUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Querri Chatbot")
        
        # Create OpenAI instance
        self.openai_client = OpenAI(api_key='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')

        # Create UI components
        self.label = tk.Label(master, text="How can Querri help you today?")
        self.label.pack()

        self.user_input = tk.Entry(master, width=50)
        self.user_input.pack()

        self.response_label = tk.Label(master, text="")
        self.response_label.pack()

        self.submit_button = tk.Button(master, text="Submit", command=self.get_user_response)
        self.submit_button.pack()

        self.terminate_button = tk.Button(master, text="Exit", command=self.terminate_chat)
        self.terminate_button.pack()

    def get_user_response(self):
        user_response = self.user_input.get()
        user_message = {"role": "user", "content": user_response}

        completion_response = self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[user_message],
        )

        bot_response = completion_response.choices[0].message.content
        self.response_label.config(text=bot_response)

    def terminate_chat(self):
        self.master.destroy()

def main():
    root = tk.Tk()
    querri_ui = QuerriUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
