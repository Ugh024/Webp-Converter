from tkinter import Tk, messagebox, Button, Checkbutton, IntVar, Frame
from tkinter.ttk import Progressbar
import threading
from PIL import Image
from pathlib import Path  # Use pathlib instead of os
import easygui

# Global variables to track progress and completion
images_processed = 0
total_images = 0
lock = threading.Lock()  # To safely update shared variables across threads

def update_progress(progress, total):
    global images_processed
    with lock:
        images_processed += 1
        progress_value = (images_processed / total) * 100
        progress['value'] = progress_value
        if images_processed == total:
            progress.grid_remove()  # Remove progress bar after all images are processed
            # Show success message only once after all images are converted
            messagebox.showinfo("Ζήτω!", "Όλες οι εικόνες μετατράπηκαν σε WebP!")

def convert_image_to_webp(image_path, save_directory, progress, total):
    img_path = Path(image_path)  # Convert string path to Path object
    if img_path.suffix.lower() in ('.jpg', '.jpeg', '.png', '.bmp', '.gif'):
        with Image.open(img_path) as img:
            if save_directory and Path(save_directory).is_dir():
                output_path = Path(save_directory) / (img_path.stem + '.webp')
            else:
                output_path = img_path.with_suffix('.webp')
                
            img.save(output_path, 'WEBP')
            
            # Update progress and possibly show completion message
            update_progress(progress, total)
    else:
        print("Εμ, δεν υποστηρίζεται αυτό το είδος αρχείου.")

def select_files(progress, use_custom_location):
    global images_processed, total_images
    filenames = easygui.fileopenbox(
        default="*.*",
        filetypes=["*.jpg", "*.jpeg", "*.png", "*.bmp", "*.gif"],
        multiple=True
    )
    if filenames:
        images_processed = 0  # Reset the processed counter
        total_images = len(filenames)  # Set total number of images selected

        save_directory = None
        if use_custom_location.get() == 1:
            save_directory = easygui.diropenbox(title="Πάτα εδώ αν θες να αποθηκευθούν σε συγκεκριμένο φάκελο αντί για τον ίδιο")
            if not save_directory:  # If the user canceled the directory selection
                return
                
        progress['value'] = 0  # Reset progress bar
        progress.grid()  # Make progress bar visible

        for filename in filenames:
            threading.Thread(target=convert_image_to_webp, args=(filename, save_directory, progress, total_images)).start()

root = Tk()
root.title("Εικόνα σε WebP")
root.geometry("450x150")

frame = Frame(root)
frame.pack(pady=20)

use_custom_location = IntVar()

open_file_btn = Button(frame, text="Επίλεξε μια ή περισσότερες εικόνες", command=lambda: select_files(progress, use_custom_location))
open_file_btn.grid(row=0, column=0, pady=10, padx=10)

save_location_chk = Checkbutton(frame, text="Πάτα εδώ αν θες να αποθηκευτούν σε άλλον φάκελο", variable=use_custom_location)
save_location_chk.grid(row=1, column=0, pady=10, padx=10)

progress = Progressbar(frame, orient='horizontal', length=280, mode='determinate')

root.mainloop()
