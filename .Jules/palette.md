## 2024-12-24 - Accessible Checkbuttons in Tkinter
**Learning:** Separate Label and Checkbutton widgets in Tkinter create poor accessibility because clicking the text label doesn't toggle the checkbox. This is especially problematic for users with motor impairments.
**Action:** Use `ttk.Checkbutton` with the `text` attribute instead of a separate Label widget. This ensures the entire label area is clickable and follows standard OS behaviors.
