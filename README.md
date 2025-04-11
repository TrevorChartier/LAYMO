# Setting up virtual environment and installing dependencies

## Create Virtual Environment

Create the virtual environment from within the project directory with the following command

```bash
python3 -m venv --system-site-packages laymo_venv
```
## Activate Virtual Environment

```bash
source laymo_venv/bin/activate
```

You should see the environment name (`laymo_venv`) at the beginning of your terminal prompt:

```bash
(laymo_venv) your-username@your-computer:~$
```

## Install Dependencies

```bash
pip install -r requirements.txt
```
