## ADK01
several examples of an agent, including ones with memory and callbacks

based on https://www.youtube.com/watch?v=RFFcBkSupxk
code downloaded from https://mer.vin/2025/05/google-adk-agents/

## Set up virtual environment

```
rm -rf .venv
virtualenv -p python3.12 .venv
. .venv/bin/activate
pip install --upgrade pip

pip install -r requirements.txt
```

## Usage

Update .env file with your API key

Then run the app with:

```bash
adk web
```

Then run the app at command line with:

```bash
adk run app
```


# Close with deactivation of venv

```
deactivate
```
