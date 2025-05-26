# AML Final Project

## Project Stucture

```bash
PlayerMarketValueProject/
├── .gitignore             ← files and folders Git should ignore
├── README.md              ← project overview and instructions
├── data/                  ← The football transfermarket dataset CSVs
│   └── .gitkeep           ← keeps the empty `data/` folder in Git
├── notebooks/             ← Jupyter notebooks for each experiment
│   ├── PlayerMarketValuePrediction_NN_v1.ipynb  ← neural network version
│   └── PlayerMarketValuePrediction_RF_v1.ipynb  ← random forest version (example)
├── src/                   ← reusable code modules
│   ├── utils.py           ← helper functions
│   └── __init__.py        ← package initializer
├── models/                ← saved model artifacts
│   ├── nn_model_v1.h5     ← neural network weights
│   └── rf_model_v1.pkl    ← random forest pickle
├── reports/               ← figures, slides, and other outputs
│   └── figures/           ← exported images for reports
└── requirements.txt       ← pinned Python dependencies
```

