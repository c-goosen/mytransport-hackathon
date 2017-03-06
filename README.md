API is based on Falcon framework

pip install -r requirements.txt

Before you run the api, register for API keys on https://developer.whereismytransport.com/clients#

Then add shell environment variablesi (unix based systems):
export MY_TRANSPORT_CLIENT_ID='xxxxxxx'
export MY_TRANSPORT_CLIENT_SECRET='MY_TRANSPORT_CLIENT_ID' 

To run falcon you can use python app.py (this is ideal for dev with stdout)

or 

gunicorn app:app --reload (This will automatically reload changes in .py files in project)
