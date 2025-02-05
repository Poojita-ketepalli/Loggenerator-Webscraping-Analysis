import pandas as pd
import random
import logging
import string
import numpy as np
import matplotlib.pyplot as plt

def generate_log_entry():
    """
    Generates a random log entry with a timestamp, log level, action and user
    """
    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    log_level = random.choice(["INFO","DEBUG","ERROR","WARNING"])
    action = random.choice(["Login","Logout","Data Request","File Upload","Download","Error"])
    user = "".join(random.choices(string.ascii_letters+string.digits,k=6)) #random username of length 6 will be generated
    return f"{timestamp} - {log_level} - {action} - USER: {user}"

# Funtion to write logs to a file
def write_logs_to_file(log_filename,num_entries=100):
    """
    Write the specified number of random logs to the given file
    """
    try:
        with open(log_filename,'w') as file:
            for _ in range(num_entries):
                log = generate_log_entry()
                file.write(log+'\n')
        print(f"Logs have been sucessfully written to {log_filename}")
    except Exception as e:
        logging.error(f"Error in writing logs to files: {e}")
        print("Error occured while writing logs to the file")

# Function to read the log file and process it
def load_and_process_logs(log_filename="generated_logs.txt"):
    """
    Loads and process the logs from the given file, cleaning and parsing in the timestamp
    """
    try:
        # Read the log file into pandas dataframe, splitting by the '-' seperator
        df = pd.read_csv(log_filename,sep=' - ',header=None,names=["Timestamp","Log_Level","Action","User"],engine='python')
        
        # Clean and trim spaces around the timestamp
        df['Timestamp'] = df["Timestamp"].str.strip()
        #Convert the timestamp column to datetime
        df["Timestamp"] = pd.to_datetime(df["Timestamp"],errors='coerce')
        #drop rows with invalid timestamps
        df = df.dropna(subset=["Timestamp"])

        if(df.empty):
            print("No valid data found after timestamp conversation")
        else:
            print("Data after timestamp conversion")
            print(df.head()) #shows data after cleaning
        
        #Set the Timestamp column as the index for time-based operation/calculations
        df.set_index('Timestamp',inplace=True)

        return df
    except Exception as e:
        print(f"Error in processing log file: {e}")
        return None
    
# Funtion to perform basic statistical analysis
def analyze_data(df):
    """
    Performs the basic analysis, such as counting log levels and actions, computing basic statistics such as mean, max etc.
    """
    try:
        if df is None or df.empty:
            print("No data available for analysis")
            return None,None
        #count the occurance of of each log level
        log_level_counts = df["Log_Level"].value_counts()

        #count the occurences of each action
        action_counts = df['Action'].value_counts()

        log_count = len(df) #Total number of logs
        unique_users = df['User'].nunique() #number of unique users
        logs_per_day = df.resample('D').size() #number of logs per day

        #Average of actions per day
        average_logs_per_day = logs_per_day.mean()

        #Max logs per day
        max_logs_per_day = logs_per_day.max()

        #Display summary statistics
        print(f"\nLog Level Counts:{log_level_counts}")
        print("\nAction counts:",action_counts)
        print("\nTotal number of logs:",log_count)
        print("\nNumber of unique users:",unique_users)
        print(f"\nAverage number of logs per day:{average_logs_per_day:.2f}")
        print("\nMax logs per day:",max_logs_per_day)

        # Create dictionary to return the analysis results
        stats = {
            "log_level_counts":log_level_counts,
            "action_counts":action_counts,
            "log_count":log_count,
            "unique_users":unique_users,
            "average_logs_per_day":average_logs_per_day,
            "max_logs_per_day":max_logs_per_day

        }
        return stats
    except Exception as e:
        print(f"Error analyzing data:{e}")
        return None

def visualize_trends(df):
    """
    Visualises log frequency trends over time using matplotlib
    """
    try:
        #Resample data to get the number of logs per day
        logs_by_day = df.resample('D').size()

        #Plotting log frequency over time using matplotlib
        plt.figure(figsize=(10,5))
        plt.plot(logs_by_day.index,logs_by_day.values,marker='o',linestyle='-',color='b')

        #customize the plot
        plt.title("Log frequency over time")
        plt.xlabel('Date')
        plt.ylabel("Number of logs")
        plt.xticks(rotation=45)
        plt.grid(True)

        #show the plot
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error visualizing the data:{e}")

log_filename = 'generated_logs.txt'
#step 1: write random logs to the file
write_logs_to_file(log_filename,num_entries=200)

#step 2: Load and process the logs from the file
df_logs = load_and_process_logs(log_filename)

#step 3: Perform basic analysis on log data
if df_logs is not None:
    stats = analyze_data(df_logs)

    #step 4: visualize trends over time
    visualize_trends(df_logs)

