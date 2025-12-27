## 2024-05-23 - [Consolidated Checkbox Controls]
**Learning:** Separate labels for checkboxes are a common anti-pattern in Tkinter apps that creates tiny, frustrating click targets. Combining them into a single  with the  attribute instantly fixes hit-testing and accessibility (screen reader association).
**Action:** Always refactor  +  pairs into a single widget.
## 2024-05-23 - [Consolidated Checkbox Controls]
**Learning:** Separate labels for checkboxes are a common anti-pattern in Tkinter apps that creates tiny, frustrating click targets. Combining them into a single `ttk.Checkbutton` with the `text` attribute instantly fixes hit-testing and accessibility (screen reader association).
**Action:** Always refactor `Checkbutton` + `Label` pairs into a single widget.
