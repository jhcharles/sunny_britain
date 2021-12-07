# Team
- John Henry Charles
- Edison Yi
- Alexandre Schmitt
- Seon Kim

# Data analysis
- Project Name: Sunny Britain
- Description: This project aims to develop a predictive model that is able to alert solar power operators of imminent inverter failures. Our current best model is able to predict inverter failures in the upcoming week 57.4% of the time.
- Data Source: LightSource BP
- Type of analysis: Predictive Modelling



# Startup the project

The initial setup.

Create virtualenv and install the project:
```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv ~/venv ; source ~/venv/bin/activate ;\
    pip install pip -U; pip install -r requirements.txt
```

Unittest test:
```bash
make clean install test
```

Check for sunny_britain in gitlab.com/{group}.
If your project is not set please add it:

- Create a new project on `gitlab.com/{group}/sunny_britain`
- Then populate it:

```bash
##   e.g. if group is "{group}" and project_name is "sunny_britain"
git remote add origin git@github.com:{group}/sunny_britain.git
git push -u origin master
git push -u origin --tags
```

Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
sunny_britain-run
```

# Install

Go to `https://github.com/{group}/sunny_britain` to see the project, manage issues,
setup you ssh public key, ...

Create a python3 virtualenv and activate it:

```bash
sudo apt-get install virtualenv python-pip python-dev
deactivate; virtualenv -ppython3 ~/venv ; source ~/venv/bin/activate
```

Clone the project and install it:

```bash
git clone git@github.com:{group}/sunny_britain.git
cd sunny_britain
pip install -r requirements.txt
make clean install test                # install and test
```
Functionnal test with a script:

```bash
cd
mkdir tmp
cd tmp
sunny_britain-run
```
