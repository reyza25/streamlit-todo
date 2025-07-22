import papermill as pm

# Jalankan notebook dengan parameter
input_notebook = r'C:\Users\rayza.rochmat\PycharmProjects\pythonProject\GCI\Test combine file GCI Sales.ipynb'
output_notebook = r'C:\Users\rayza.rochmat\PycharmProjects\pythonProject\GCI\Test combine file GCI Sales Output.ipynb'


pm.execute_notebook(input_notebook, output_notebook)
