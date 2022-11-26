# Transcription program

Transcription program using [AssemblyAI](https://www.assemblyai.com/).

Program supports these languages:

* English
* Spanish
* French
* German
* Italian
* Portuguese
* Dutch

## How to run

Install newest Python v3.
Install dependencies with:

```
pip install -r requirements.txt
```

and then create file **configure.py** with the following content:

```py
auth_key = "YOUR_API_KEY"
```

Replace YOUR_API_KEY with a key that can be found in the account settings on AssemblyAI's website.
Run program with Python, enter number of seconds that your recording will last. Then speak for previously selected time. After this procedure program will automatically transcribe your speech and save it into output.txt file.