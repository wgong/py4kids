# necessary imports
# https://gist.github.com/thatguyfig/b52ac1a33f94a9bf89e78e8dff24fda2
import boto3
import datetime as dt
import pandas as pd
import time


# function to create a client with aws for a specific service and region
def create_client(service, region):
    return boto3.client(service, region_name=region)

# function to load data from CSV
def load_data(filename):
    df = pd.read_csv(filename)
    return df

# function to correctly display numbers in 2 value format (i.e. 06 instead of 6)
def lengthen(value):
    if len(value) == 1:
        value = "0" + value
    return value

# function for generating new runtime to be used for timefield in ES
def get_date():

    today = str(dt.datetime.today()) # get today as a string
    year = today[:4]
    month = today[5:7]
    day = today[8:10]

    hour = today[11:13]
    minutes = today[14:16]
    seconds = today[17:19]

    # return a date string in the correct format for ES
    return "%s/%s/%s %s:%s:%s" % (year, month, day, hour, minutes, seconds)

# function to modify the date time to be correctly formatted
def modify_date(data):
    
    dates = data['cdatetime'] # get the datetime field
    
    new_dates = [] # create empty lists
    load_times = [] 
    
    load_time = get_date() # get current time
    
    # loop over all records
    for date in dates:
        
        date = date.replace('/','-') # replace the slash with dash
        date = date + ":00" # add seconds to the datetime
        
        split = date.split(" ") # split the datetime
        
        date = split[0] # get just date 
        
        months = date.split('-')[0] # get months
        days = date.split('-')[1] # days
        years = "20" + date.split('-')[2] # years
        
        time = split[1] # get just time
        
        hours = time.split(':')[0] # get hours
        minutes = time.split(':')[1] # get minutes
        seconds = time.split(':')[2] # get seconds
        
        # build up a string in the right format
        new_datetime = years + "/" + lengthen(months) + "/" + lengthen(days) + " " + lengthen(hours) + ":" + lengthen(minutes) + ":" + seconds
        
        # add it the list
        new_dates.append(new_datetime)
        load_times.append(load_time)
    
    # update the datetime with our transformed version
    data['cdatetime'] = new_dates
    data['loadtime'] = load_times
    
    # return the dataframe
    return data

# function for sending data to Kinesis at the absolute maximum throughput
def send_kinesis(kinesis_client, kinesis_stream_name, kinesis_shard_count, data):

    kinesisRecords = [] # empty list to store data

    (rows, columns) = data.shape # get rows and columns off provided data

    currentBytes = 0 # counter for bytes

    rowCount = 0 # as we start with the first

    totalRowCount = rows # using our rows variable we got earlier

    sendKinesis = False # flag to update when it's time to send data
    
    shardCount = 1 # shard counter

    # loop over each of the data rows received 
    for _, row in data.iterrows(): 

        values = '|'.join(str(value) for value in row) # join the values together by a '|'

        encodedValues = bytes(values, 'utf-8') # encode the string to bytes

        # create a dict object of the row
        kinesisRecord = {
            "Data": encodedValues, # data byte-encoded
            "PartitionKey": str(shardCount) # some key used to tell Kinesis which shard to use
        }


        kinesisRecords.append(kinesisRecord) # add the object to the list
        stringBytes = len(values.encode('utf-8')) # get the number of bytes from the string
        currentBytes = currentBytes + stringBytes # keep a running total

        # check conditional whether ready to send
        if len(kinesisRecords) == 500: # if we have 500 records packed up, then proceed
            sendKinesis = True # set the flag

        if currentBytes > 50000: # if the byte size is over 50000, proceed
            sendKinesis = True # set the flag

        if rowCount == totalRowCount - 1: # if we've reached the last record in the results
            sendKinesis = True # set the flag

        # if the flag is set
        if sendKinesis == True:
            
            # put the records to kinesis
            response = kinesis_client.put_records(
                Records=kinesisRecords,
                StreamName = kinesis_stream_name
            )
            
            # resetting values ready for next loop
            kinesisRecords = [] # empty array
            sendKinesis = False # reset flag
            currentBytes = 0 # reset bytecount
            
            # increment shard count after each put
            shardCount = shardCount + 1
        
            # if it's hit the max, reset
            if shardCount > kinesis_shard_count:
                shardCount = 1
            
        # regardless, make sure to incrememnt the counter for rows.
        rowCount = rowCount + 1
        
    
    # log out how many records were pushed
    print('Total Records sent to Kinesis: {0}'.format(totalRowCount))

# main function
def main(file_csv, region):
    
    # start timer
    start = time. time()
    
    # create a client with kinesis
    kinesis = create_client('kinesis',region)
    
    # load in data from the csv
    data = load_data(file_csv)
    
    # modify the date and add loadtime field
    data = modify_date(data)
    
    # send it to kinesis data stream
    stream_name = "DataStream"
    stream_shard_count = 1
    
    send_kinesis(kinesis, stream_name, stream_shard_count, data) # send it!
    
    # end timer
    end = time. time()
    
    # log time
    print("Runtime: " + str(end - start))
    
if __name__ == "__main__":
    
    # run main
    file_csv = "SacramentocrimeJanuary2006.csv"
    region = "us-east-1"
    main(file_csv, region)