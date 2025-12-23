## 2024-05-23 - Separated Label and Input Control
**Learning:** `ttk.Checkbutton` (and standard `tk.Checkbutton`) supports a `text` attribute that makes the label part of the clickable area. Using a separate `Label` widget next to a `Checkbutton` reduces the hit area and breaks the accessibility association.
**Action:** Always use the `text` attribute of the input widget itself when the label is meant to caption that specific input, instead of a separate label widget.
