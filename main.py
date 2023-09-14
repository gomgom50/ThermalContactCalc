import tkinter as tk
from tkinter import ttk
from math import sqrt
import matplotlib.pyplot as plt
import io
from PIL import Image, ImageTk
import webbrowser

def compute_hc(*args):
    try:
        m_u_asp = float(m_u_asp_var.get())
        m_d_asp = float(m_d_asp_var.get())
        sigma_u_asp = float(sigma_u_asp_var.get())
        sigma_d_asp = float(sigma_d_asp_var.get())
        k_u = float(k_u_var.get())
        k_d = float(k_d_var.get())
        P = float(P_var.get())
        H_c = float(H_c_var.get())

        m_asp = sqrt(m_u_asp ** 2 + m_d_asp ** 2)
        sigma_asp = sqrt(sigma_u_asp ** 2 + sigma_d_asp ** 2)
        k_contact = (2 * k_u * k_d) / (k_u + k_d)
        hc = 1.25 * k_contact * m_asp / sigma_asp * (P/H_c) ** 0.95

        hc_var.set(f"{hc:.10f}")
    except ValueError:
        hc_var.set("Invalid input!")


def latex_to_image(latex_str):
    fig, ax = plt.subplots(figsize=(1, 0.5))  # Adjust the size to fit your needs
    ax.text(0.5, 0.5, '$%s$' % latex_str, size=12, ha='center', va='center', color="black")

    # Set the background color to match tkinter's default gray
    fig.patch.set_facecolor('#f0f0f0')
    ax.set_facecolor('#f0f0f0')

    ax.axis('off')
    buf = io.BytesIO()

    # Ensure that the saved image has a transparent background
    plt.savefig(buf, format="png", bbox_inches='tight', pad_inches=0, facecolor=fig.get_facecolor())
    buf.seek(0)

    img = Image.open(buf)
    return ImageTk.PhotoImage(img)

def open_webpage(event):
    """Callback to open the provided link in a web browser"""
    webbrowser.open("https://doc.comsol.com/5.5/doc/com.comsol.help.heat/heat_ug_theory.07.66.html")




app = tk.Tk()
app.title("Cooper-Mikic-Yovanovich (CMY) Correlation")


# Adding a title label above the grid
title_label = ttk.Label(text="Cooper-Mikic-Yovanovich (CMY) Correlation", font=("Arial", 16))
title_label.grid(column=0, row=0, columnspan=2, pady=(0, 5))

# Add the clickable link below the top label
link_label = tk.Label(app, text="Documentation Link", fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
link_label.grid(column=0, row=1, columnspan=2, pady=(0, 5))
link_label.bind("<Button-1>", open_webpage)


frame = ttk.Frame(app, padding="15")
frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))


# Variables with trace
m_u_asp_var = tk.StringVar()
m_u_asp_var.trace("w", compute_hc)

m_d_asp_var = tk.StringVar()
m_d_asp_var.trace("w", compute_hc)

sigma_u_asp_var = tk.StringVar()
sigma_u_asp_var.trace("w", compute_hc)

sigma_d_asp_var = tk.StringVar()
sigma_d_asp_var.trace("w", compute_hc)

k_u_var = tk.StringVar()
k_u_var.trace("w", compute_hc)

k_d_var = tk.StringVar()
k_d_var.trace("w", compute_hc)

P_var = tk.StringVar()
P_var.trace("w", compute_hc)

H_c_var = tk.StringVar()
H_c_var.trace("w", compute_hc)

hc_var = tk.StringVar()


# Sample image for the tooltip:
sample_img = latex_to_image(r'E=mc^2')  # Use any equation you want

# Entry widgets for inputs
entries = [
    (r'm_{u,asp}:', m_u_asp_var),
    (r'm_{d,asp}:', m_d_asp_var),
    (r'\sigma_{u,asp}:', sigma_u_asp_var),
    (r'\sigma_{d,asp}:', sigma_d_asp_var),
    (r'k_u:', k_u_var),
    (r'k_d:', k_d_var),
    (r'P:', P_var),
    (r'H_c:', H_c_var)
]

for i, (label, var) in enumerate(entries):
    label_img = latex_to_image(label)
    lbl = ttk.Label(frame, image=label_img)
    lbl.image = label_img  # keep a reference to the image to prevent garbage collection
    lbl.grid(column=0, row=i, sticky=tk.W, padx=5, pady=5)


    ttk.Entry(frame, textvariable=var).grid(column=1, row=i, padx=5, pady=5, sticky=tk.EW)

# Render the hc label using LaTeX and display it
hc_label_latex = r'h_c'
hc_label_img = latex_to_image(hc_label_latex)
hc_lbl = ttk.Label(frame, image=hc_label_img)
hc_lbl.image = hc_label_img  # keep a reference to the image to prevent garbage collection
hc_lbl.grid(column=0, row=len(entries), sticky=tk.W, padx=5, pady=5)
ttk.Entry(frame, textvariable=hc_var, state="readonly").grid(column=1, row=len(entries), padx=5, pady=5, sticky=tk.EW)

frame.columnconfigure(1, weight=1)

app.mainloop()
