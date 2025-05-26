# _AML Final Project_
<p>
This is our final project in the AML course. We will analyse a dataset that provides detailed info on players, clubs, matches, and player market values from around 2012, and it's updated regularly regarding football. We will analyse it and make some predictions e.g player valuation in transfermarket, club successrate for next match and so on 
</p>


Dataset used: https://www.kaggle.com/datasets/davidcariboo/player-scores/versions/602
___

## Project Stucture

```bash
├── .gitignore             ← files and folders Git should ignore
├── README.md              ← project overview and instructions
├── data/                  ← The football transfermarket dataset CSVs
│   └── .gitkeep           ← keeps the empty `data/` folder in Git
├── notebooks/             ← Jupyter notebooks for each experiment
│   ├── PlayerMarketValuePrediction_NN_v1.ipynb  ← neural network version (done)
│   └── PlayerMarketValuePrediction_RF_v1.ipynb  ← random forest version (not done)
├── src/                   ← reusable code modules
│   ├── utils.py           ← helper functions
│   └── __init__.py        ← package initializer
├── models/                ← saved model artifacts
│   ├── nn_model_v1.h5     ← neural network weights (not done)
│   └── rf_model_v1.pkl    ← random forest pickle   (not done)
├── reports/               ← figures, slides, and other outputs
│   └── figures/           ← exported images for reports
└── requirements.txt       ← pinned Python dependencies
```
___
## Setup
1) Download the dataset as a zip from [kaggle](https://www.kaggle.com/datasets/davidcariboo/player-scores/versions/602?resource=download). Extract all the .csv files into the `data` folder.
2) Make sure you have set up a python environment. We used `python 3.12` and `conda`, as per the [course description](https://www.nbi.dk/~petersen/Teaching/AppliedMachineLearning2025.html).
3) Run `pip install -r requirements.txt`, to make sure you are using the correct libraries.
4) Done.

___