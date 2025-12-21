## 2024-04-20 - Clickable Checkbox Labels
**Learning:** Separate labels for checkboxes reduce accessibility and usability because users must click the exact small box to toggle.
**Action:** Always use the `text` attribute of `ttk.Checkbutton` (or similar native widgets) to ensure the label is part of the clickable area and programmatically associated with the control.
