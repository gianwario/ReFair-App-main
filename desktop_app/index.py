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
        label.config(text=f"{file_name}", fg="black")
    else:
        # Se non è un file .xlsx, mostra un messaggio di errore
        label.config(text="Errore: Il file selezionato non è un file .xlsx", fg="red")
        file_path = ""
        user_stories.clear()  # Cancella le user stories salvate

def load_file():
    global user_stories, user_story_labels
    if not file_path:
        # Se non è stato selezionato alcun file valido, mostra un messaggio di errore
        error_label = Label(root, text="Errore: Nessun file .xlsx selezionato!", fg="red")
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
        error_label = Label(root, text="Errore: Colonna 'User Story' non trovata!", fg="red")
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
        user_story_label = Label(root, text=cell.value)
        user_story_label.grid(row=row_index, column=0, columnspan=2, padx=10, pady=2, sticky="w")
        row_index += 1
        user_stories.append(cell.value)  # Aggiungi la user story alla lista
        
        # Aggiungi la Label alla lista per poterla rimuovere in seguito
        user_story_labels.append(user_story_label)

def save_as_json():
    if not user_stories:
        # Se non ci sono user stories caricate, mostra un messaggio di errore
        error_label = Label(root, text="Errore: Nessuna User Story da salvare!", fg="red")
        error_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)
        return
    
    # Apri la finestra di dialogo per salvare il file JSON
    save_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    
    if save_path:
        # Scrivi le user stories nel file JSON
        with open(save_path, 'w') as json_file:
            json.dump(user_stories, json_file, indent=4)
        success_label = Label(root, text=f"File salvato: {save_path}", fg="green")
        success_label.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

root = Tk()  # Una nuova finestra è definita
root.title("ReFair desktop app")
root.geometry("600x400")  # Dimensioni della finestra
root.iconbitmap('desktop_app/icons/right_arrow_icon.ico')

# Bottone per aprire il file
button = Button(root, text="Apri File", command=open_file)
button.grid(row=0, column=0, padx=10, pady=20)

# Bottone per caricare il contenuto del file
load_button = Button(root, text="Load", command=load_file)
load_button.grid(row=1, column=0, padx=10, pady=10)

# Bottone per salvare il contenuto come JSON
save_button = Button(root, text="Save as JSON", command=save_as_json)
save_button.grid(row=2, column=0, padx=10, pady=10)

# Label che verrà aggiornata dal bottone "Apri File"
label = Label(root, text="")
label.grid(row=0, column=1, padx=10, pady=20)

root.mainloop()  # Necessario per rendere la finestra visibile