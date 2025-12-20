# Palette's Journal

## 2024-10-25 - Tkinter Checkbox Accessibility
**Learning:** In Tkinter/ttkbootstrap, separating `Checkbutton` and its label (via a separate `Label` widget) destroys the expected behavior of clicking the text to toggle the checkbox. It also complicates layout management.
**Action:** Always use the `text` attribute of `ttk.Checkbutton` instead of a separate label. This improves click target size (Fitts's Law) and simplifies the grid layout code.
