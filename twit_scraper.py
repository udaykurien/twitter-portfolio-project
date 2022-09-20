#!/usr/bin/env python
# coding: utf-8

import tweepy, twit_auth_cred, os, json, time
import pandas as pd

def twit_client():
    ''' 
    Authenticate and create instance of twitter client.
    '''
    print("Starting authentication.")
    client = tweepy.Client(
        bearer_token = twit_auth_cred.bearer_token,
        consumer_key = twit_auth_cred.api_key,
        consumer_secret = twit_auth_cred.api_key_secret,
        access_token = twit_auth_cred.access_token,
        access_token_secret = twit_auth_cred.access_token_secret,
    )
    print("Authentication complete.")
    return client

def get_user_info(lst_author_id):
    '''
    Get twitter usernames corresponding to their user ids.
    '''
    client = twit_client()
    user_name = []
    for author_id in lst_author_id:
        user_name.append(client.get_user(author_id = author_id))
    return user

def search_tweets(str_query, int_max_results, list_expansions, list_tweet_fields, 
                  list_user_fields,paginator_limit):
    '''
    Scrape tweets based on certain filters and parameters.
    '''
    print("Starting tweet retrieval.")
    paginator = tweepy.Paginator
    client = twit_client()
    search_results = []
    counter = 0
    for iterator in paginator(client.search_recent_tweets,
                              query = str_query, 
                              max_results = int_max_results,
                              expansions = list_expansions,
                              tweet_fields = list_tweet_fields,
                              user_fields = list_user_fields).flatten(
                              limit = paginator_limit):
        counter += 1   
        print("Retrieval loop number: {number}%".format(
            number = round((counter/paginator_limit)*100,2)),end='',flush=True)        
#         time.sleep(0.3)
        search_results.append(iterator)
        print('\r', end='')
    print('\r', end='')
    print("Tweet retrieval complete.")
#     print(search_results)
    return search_results

def tweets_to_file(data_file, search_results):
    '''
    Save tweets to file using a custom json/dictionary type format.
    '''
    print("Starting write to file, {data_file}.".format(data_file=data_file))
    with open(data_file,'w') as fhandle:
        for tweet in search_results:
            tmp_dict  = {
                "tweet_id" : tweet.id,
                "tweet_text" : tweet.text,
                "tweet_time" : str(tweet.created_at),
                "tweet_author_id" : tweet.author_id,
#                 "tweet_username" : tweet.username,
                "tweet_language" : tweet.lang,
                "tweet_public_metrics" : tweet.public_metrics,
                "tweet_source" : tweet.source
            }
            json.dump(tmp_dict, fhandle)
            fhandle.write("\n")
    print("Write to file, {data_file}, completed.".format(data_file=data_file))
    return 0

def tweetfile_2_dataframe(data_file):
    '''
    Import custom json data file into dataframe.
    '''
    print("Converting file to dataframe.")
    with open(data_file, 'r') as fhandle:
        lines = fhandle.readlines()
        dict_lst = []   
        for line in lines:
            organized_dict = {}
            tmp_dict = json.loads(line.strip())
            for key in tmp_dict:
                if key == 'tweet_public_metrics':
                    for key2 in tmp_dict['tweet_public_metrics']:
                        organized_dict[key2] = tmp_dict['tweet_public_metrics'][key2]
                else:
                    organized_dict[key] = tmp_dict[key]
            dict_lst.append(organized_dict)
    df = pd.DataFrame(dict_lst)
    print("File to dataframe conversion completed.")
    return df

def main():
    # Application Options
    fetch_new_data = 'y' # value 'y' for yes
    write_data_to_file = 'y'
    read_from_file = 'y' # value 'y' for yes
    f_path = 'data'
    f_name = 'test'
    data_file = os.path.join(f_path,f_name)
    # Fetch new data
    if fetch_new_data == 'y':
        # Parameters
        str_query_1 = '((Roe Wade) OR (roe wade)) -is:retweet -is:reply -is:quote'
        int_max_results = 20
        list_expansions = ['author_id','entities.mentions.username'] 
        list_tweet_fields = ['created_at','lang','public_metrics', 'source','id']
        list_user_fields = ['username']
        paginator_limit = 30
        # Retrieve tweets as a list
        search_results = search_tweets(
            str_query_1, 
            int_max_results, 
            list_expansions, 
            list_tweet_fields,
            list_user_fields,
            paginator_limit
        )
        # Write tweet data to file
    if write_data_to_file == 'y':
        tweets_to_file(data_file, search_results)
    # Read data from file
    if read_from_file == 'y':
        # Import file as pandas data frame
        df = tweetfile_2_dataframe(data_file)
        print(df)
    
if __name__ == "__main__":
    main()

