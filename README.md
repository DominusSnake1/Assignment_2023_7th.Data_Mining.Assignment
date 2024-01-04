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
pip3 install -r ./Utils/requirements.txt
```

## <u>Step 3</u>:<br>Run the program in either Normal or DEMO mode.
* Normal Mode (Full Dataset)
```bash
python ./main.py
```
* DEMO Mode (Sample) 
```bash
python ./main.py -demo NUM_OF_ROWS
```

## <u>Step 4</u>:<br>View the results.
1. <u>KNeighborsClassifier (3 Neighbors)</u>:<br>
Accuracy: 0.98<br>
Cross-Validation Accuracy: 0.9464870360955769<br>
Predictions for 'Oscar Winners': [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0]
Number of 'Predicted' Winners: 1

|         	          | **precision** 	 | **recall** 	 | **f1-score** 	 | **support** 	 |
|:------------------:|:---------------:|:------------:|:--------------:|:-------------:|
|    **0**      	    |   1.00     	    |  0.98    	   |   0.99     	   |   50     	    |
|    **1**      	    |   0.00     	    |  1.00    	   |   0.00     	   |   0      	    |
|         	          |        	        |      	       |       	        |       	       |
|  **accuracy**   	  |        	        |      	       |   0.98     	   |   50     	    |
|  **macro avg**  	  |   0.50     	    |  0.99    	   |   0.49     	   |   50     	    |
| **weighted avg** 	 |   1.00     	    |  0.98    	   |   0.99     	   |   50     	    |

2. <u>Logistic Regression</u>:<br>
Accuracy: 0.94<br>
Cross-Validation Accuracy: 0.9600610066090493<br>
Predictions for 'Oscar Winners': [0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 1 0]
Number of 'Predicted' Winners: 3

|         	          | **precision** 	 | **recall** 	 | **f1-score** 	 | **support** 	 |
|:------------------:|:---------------:|:------------:|:--------------:|:-------------:|
|    **0**      	    |   1.00     	    |  0.94    	   |   0.97     	   |   50     	    |
|    **1**      	    |   0.00     	    |  1.00    	   |   0.00     	   |   0      	    |
|         	          |        	        |      	       |       	        |       	       |
|  **accuracy**   	  |        	        |      	       |   0.94     	   |   50     	    |
|  **macro avg**  	  |   0.50     	    |  0.97    	   |   0.48     	   |   50     	    |
| **weighted avg** 	 |   1.00     	    |  0.94    	   |   0.97     	   |   50     	    |

3. <u>Decision Trees</u>:<br>
Accuracy: 0.72<br>
Cross-Validation Accuracy: 0.945775292323335<br>
Predictions for 'Oscar Winners': [0 1 1 1 0 1 0 1 0 0 0 1 0 0 0 0 0 1 1 0 0 0 0 1 0 0 0 1 1 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0]
Number of 'Predicted' Winners: 14

|         	          | **precision** 	 | **recall** 	 | **f1-score** 	 | **support** 	 |
|:------------------:|:---------------:|:------------:|:--------------:|:-------------:|
|    **0**      	    |   1.00     	    |  0.72    	   |   0.84     	   |   50     	    |
|    **1**      	    |   0.00     	    |  1.00    	   |   0.00     	   |   0      	    |
|         	          |        	        |      	       |       	        |       	       |
|  **accuracy**   	  |        	        |      	       |   0.94     	   |   50     	    |
|  **macro avg**  	  |   0.50     	    |  0.97    	   |   0.48     	   |   50     	    |
| **weighted avg** 	 |   1.00     	    |  0.94    	   |   0.97     	   |   50     	    |

4. <u>Random Forest</u>:<br>
Accuracy: 0.98<br>
Cross-Validation Accuracy: 0.9657600406710728<br>
Predictions for 'Oscar Winners': [0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0]
Number of 'Predicted' Winners: 1

|         	          | **precision** 	 | **recall** 	 | **f1-score** 	 | **support** 	 |
|:------------------:|:---------------:|:------------:|:--------------:|:-------------:|
|    **0**      	    |   1.00     	    |  0.98    	   |   0.99     	   |   50     	    |
|    **1**      	    |   0.00     	    |  1.00    	   |   0.00     	   |   0      	    |
|         	          |        	        |      	       |       	        |       	       |
|  **accuracy**   	  |        	        |      	       |   0.98     	   |   50     	    |
|  **macro avg**  	  |   0.50     	    |  0.99    	   |   0.49     	   |   50     	    |
| **weighted avg** 	 |   1.00     	    |  0.98    	   |   0.99     	   |   50     	    |