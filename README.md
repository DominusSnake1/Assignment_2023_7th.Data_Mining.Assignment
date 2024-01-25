## <u>Step 0</u>:<br>Create a Conda Environment (if it doesn't exist).
```bash
conda create --name py39 python=3.9
```

## <u>Step 1</u>:<br>Activate the Conda Environment.
```bash
conda activate py39
```

## <u>Step 2</u>:<br>Install the required packages.
```bash
pip3 install -r ./Other/requirements.txt
```

## <u>Step 3</u>:<br>Run the program in either Normal or DEMO mode.
* Normal Mode (Full Dataset)
```bash
python ./main.py -alg SELECT_ALGORITHM
```
(Example: `-alg RFC`)
* DEMO Mode (Sample) 
```bash
python ./main.py -alg SELECT_ALGORITHM -demo NUM_OF_ROWS
```
(Example: `-alg RFC -demo 20`)