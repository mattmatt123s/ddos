import asyncio
import aiohttp
import tkinter as tk
from tkinter import Text, ttk

async def request_url(session, url):
    try:
        async with session.get(url) as response:
            print(f"Request to {url} - Status: {response.status}")
            return response.status
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

async def main(url, num_requests, result_label):
    async with aiohttp.ClientSession() as session:
        tasks = [request_url(session, url) for _ in range(num_requests)]
        statuses = await asyncio.gather(*tasks)
        success_count = statuses.count(200) if statuses else 0
        result_label.config(text=f"Requests sent: {num_requests}\nSuccess count: {success_count}")

def execute_script(url_entry, num_requests_entry, result_label):
    try:
        url = url_entry.get("1.0", tk.END).strip()
        num_requests = int(num_requests_entry.get())
    except ValueError:
        print("Invalid input. Please enter a valid URL and number.")
        return

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(url, num_requests, result_label))


app = tk.Tk()
app.title("Script Executor")


app.geometry("400x400")


app.configure(bg="#333333")


frame = ttk.Frame(app, style="TFrame")
frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)


style = ttk.Style()
style.configure("TFrame", background="#333333")  
style.configure("TLabel", background="#1E90FF", foreground="white", font=("Helvetica", 12))

label_author = ttk.Label(frame, text="Coded by Splatdev1", style="TLabel")
label_author.pack(pady=5)

url_label = ttk.Label(frame, text="URL:")
url_label.pack()

url_entry = Text(frame, font=("Helvetica", 12), wrap=tk.WORD, height=1)
url_entry.pack(fill=tk.X)

num_requests_label = ttk.Label(frame, text="Number of Requests:")
num_requests_label.pack()

num_requests_entry = ttk.Entry(frame, font=("Helvetica", 12))
num_requests_entry.pack()


canvas = tk.Canvas(frame, bg="#1E90FF", width=100, height=40, highlightbackground="black", highlightthickness=1)
canvas.pack(pady=10)

execute_button = canvas.create_text(50, 20, text="Execute", font=("Helvetica", 12, "bold"), fill="white")


result_label = ttk.Label(frame, text="", style="TLabel")
result_label.pack(side="bottom", pady=10)


canvas.bind("<Button-1>", lambda event: execute_script(url_entry, num_requests_entry, result_label))


app.mainloop()
