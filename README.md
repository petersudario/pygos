# Pygos
> Pip and Python 3.12 required
> Project in Google Cloud with a Service account created and Google Drive's API enabled
> A Spreadsheet in Google Spreadsheets shared with the service account's email


# Steps to install the project (terminal)

> python -m venv venv
>
> .\venv\Scripts\activtte
>
> pip install -r requirements.txt

# Steps to execute the scripts

> Fill "quiet-cider.json" with your info of the Service account;

> In line 18: spreadsheet = client.open_by_url("file").....
>
>   Change "file" to your spreadsheet's URL.


