# Omelia (HackTX 2020)

Omelia is a Chrome Extension that our group created using JavaScript and HTML/CSS that modifies a Google spreadsheet
using voice commands recorded by a user. Whenever you have a Google spreadsheet open, you should be able to see a
bright red record button and a box that depicts what you have said. With a simple click of the button, you can speak
whatever command you'd like, and the changes should automatically be shown on the spreadsheet.

We implemented a real-time speech-to-text translation by utilizing the WebSpeech API. In addition, we created our own
Natural Language Processing classification model and trained it with 50 dimensional GloVe vectors to recognize the text.
This model is able to interpret what we speak and classify it correctly. With this, you can add/subtract rows to each other,
add/subtract/multiply/divide constants to a cell, add/subtract/multiply/divide cells to each other, change the background
color of cells, insert new rows and columns, bold cells, find the average of rows and columns, as well as filter rows and columns.

We built a Python RESTful API using Flask that we eventually deployed to Google Cloud Functions. This API takes in the output of
our NLP model and uses the Google Sheets API to make respective changes to the spreadsheet.

We haven't released our Chrome Extension yet. To use this, you can clone the repository. Go to chrome://extensions, enter developer
mode, click on load unpacked, and upload the folder that contains this code.