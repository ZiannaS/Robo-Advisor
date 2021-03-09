# ROBO ADVISOR APPLICATION

OVERVIEW: This simple application which allows users to track the stock prices of whichever stock they would like to find. They can also compare multiple different stocks and see the fluctuation in prices of stocks in the last 100 days. 

FEATURES
- Input a stock symbol/ multiple stock symbols as a comma separated list to get information about the stock. 
- See a line chart of the price trajectory of the stock over the last 100 days. 

ENVIRONMENT VARIABLE SET UP
- Create a .env file in the app directory of the project.
- Ensure that this file is named “.env”
- Within the env file add the following fields:
- ALPHAVANTAGE_API_KEY=***************

ALPHAVANTAGE SET UP
- Visit the webpage https://www.alphavantage.co/
- Click on "GET YOUR FREE API KEY TODAY"
- Fill up the questionaire and click "GET FREE API KEY"
- You will be presented with an API KEY. 

SETTING UP THE ENVIRONMENT
- cd in to the root directory Robo-Advisor
- Before running the python script it is necessary to set up the conda environment by typing into terminal 
    - conda create -n stocks-env python=3.8 # (first time only)
    - conda activate stocks-env
- There after you must cd into the app directory and install the requirements using the command 
    - pip3 install -r requirements.txt
- You can now run your program using the command 
    - python3 robo_advisor.py

RULES OF USAGE
- Type in a symbol for a stock 
- If you are typing multiple symbols make sure it is a comma separated list without any spaces
- You will need to close the graph which appears in order to continue
- To exit the program you can type "DONE"