from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import openpyxl
import json

# Variabile globale per salvare il percorso del file selezionato e le user stories
user_story_labels = []
file_path = ""
user_stories = []

def open_file():
    global file_path
    # Apri la finestra di dialogo per selezionare un file
    file_path = filedialog.askopenfilename()
    
    # Controlla se il file selezionato è un .xlsx
    if file_path.endswith('.xlsx'):
        # Se è un file .xlsx, crea una label con il nome del file
        file_name = os.path.basename(file_path)
        file_name_label.config(text=f"{file_name}", fg="black")
    else:
        # Se non è un file .xlsx, mostra un messaggio di errore
        file_name_label.config(text="Errore: Il file selezionato non è un file .xlsx", fg="red")
        file_path = ""
        user_stories.clear()  # Cancella le user stories salvate

def load_file():
    global user_stories, user_story_labels
    if not file_path:
        # Se non è stato selezionato alcun file valido, mostra un messaggio di errore
        error_label = Label(main_content, text="Errore: Nessun file .xlsx selezionato!", fg="red")
        error_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        return
    
    # Carica il file .xlsx
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active
    
    # Trova la colonna "User Story"
    user_story_col = None
    for col in sheet.iter_cols(1, sheet.max_column):
        if col[0].value == "User Story":
            user_story_col = col
            break
    
    if user_story_col is None:
        # Se la colonna "User Story" non esiste, mostra un messaggio di errore
        error_label = Label(main_content, text="Errore: Colonna 'User Story' non trovata!", fg="red")
        error_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        return

    # Cancella eventuali user stories precedenti
    user_stories.clear()
    
    # Rimuovi tutte le Label precedentemente create
    for label in user_story_labels:
        label.destroy()
    
    # Svuota la lista delle Label
    user_story_labels.clear()
    
    # Stampa ogni riga della colonna "User Story" in una label differente
    row_index = 3
    for cell in user_story_col[1:]:  # Salta l'intestazione
        user_story_label = Label(main_content, text=cell.value)
        user_story_label.grid(row=row_index, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        row_index += 1
        user_stories.append(cell.value)  # Aggiungi la user story alla lista
        
        # Aggiungi la Label alla lista per poterla rimuovere in seguito
        user_story_labels.append(user_story_label)

def save_as_json():
    if not user_stories:
        # Se non ci sono user stories caricate, mostra un messaggio di errore
        error_label = Label(main_content, text="Errore: Nessuna User Story da salvare!", fg="red")
        error_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        return
    
    # Allows to save the JSON file with a specific name
    save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    
    if save_path:
        # Fills the JSON file with US
        with open(save_path, 'w') as json_file:
            json.dump(user_stories, json_file, indent=4)
        success_label = Label(main_content, text=f"File salvato: {save_path}", fg="green")
        success_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

root = Tk()
root.title("ReFair desktop app")
root.geometry("600x400")  # window dimensions
root.iconbitmap('desktop_app/icons/right_arrow_icon.ico')

sidebar = Frame(root, background='red', width=200)
sidebar.pack(fill=Y, side=LEFT)  

main_content = Frame(root, background='yellow')
main_content.pack(expand=True, fill=BOTH)  

# Select File Button 
button = ttk.Button(main_content, text="Select file", command=open_file)
button.grid(row=0, column=0, padx=10, pady=20)

# Label that shows the name of the file opened
file_name_label = Label(main_content, text="")
file_name_label.grid(row=0, column=1, padx=10, pady=20)

# Load Button
load_button = Button(main_content, text="Load", command=load_file)
load_button.grid(row=1, column=0, padx=10, pady=10)

# Download all Button
save_button = Button(main_content, text="Download all", command=save_as_json)
save_button.grid(row=2, column=0, padx=10, pady=10)

root.mainloop()  # Necessario per rendere la finestra visibile