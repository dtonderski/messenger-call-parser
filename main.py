import datetime
import customtkinter
from customtkinter import filedialog
import json
import pandas as pd
calls = []
def button_load(textbox: customtkinter.CTkTextbox):
    filenames = filedialog.askopenfilename(filetypes=[('json file', '*.json',)], multiple=True)
    calls.clear()
    for name in filenames:
        with open(name, 'r') as f:
            json_dict = json.load(f)
            calls.extend([x for x in json_dict['messages'] if 'call_duration' in x.keys()])
    textbox.configure(state=customtkinter.NORMAL)
    textbox.delete(1.0, "end-1c")
    textbox.insert("end-1c", text=f"Loaded {len(calls)} calls!")
    textbox.configure(state=customtkinter.DISABLED)

def button_function_2(textbox: customtkinter.CTkTextbox):
    filename = filedialog.asksaveasfilename(defaultextension='.csv')

    df = pd.DataFrame(columns=["Start time", "Duration [s]"])

    for call in calls:
        start_datetime = datetime.datetime.fromtimestamp(call['timestamp_ms'] / 1000.)
        call_duration = call['call_duration']
        if call_duration > 0:
            df.loc[len(df)] = [start_datetime, call_duration]
    df = df.sort_values("Start time")
    df.to_csv(filename)

    textbox.configure(state=customtkinter.NORMAL)
    textbox.delete(1.0, "end-1c")
    textbox.insert("end-1c", text=f"Saved {len(calls)} calls to {filename}!")
    textbox.configure(state=customtkinter.DISABLED)

def main():
    customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    app = customtkinter.CTk()
    app.title("Messenger Call Log Parser")
    app.geometry("600x100")

    # Create the textbox and make it fill the grid cell
    textbox = customtkinter.CTkTextbox(app, height=20)
    textbox.configure(state=customtkinter.DISABLED)
    textbox.grid(row=0, column=0, columnspan=3, sticky="nsew")  # make textbox fill the cell

    # Create buttons and make them fill their grid cells
    load_button = customtkinter.CTkButton(master=app, text="Load .json", command=lambda: button_load(textbox))
    load_button.grid(row=1, column=0)

    button_1 = customtkinter.CTkButton(master=app, text="Save to .csv", command=lambda: button_function_2(textbox))
    button_1.grid(row=1, column=1)

    # Set grid column and row configurations to allow for resizing
    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)  # allow the textbox row to expand
    app.grid_rowconfigure(1, weight=0)  # allow the button row to expand

    app.mainloop()


if __name__ == '__main__':
    main()



