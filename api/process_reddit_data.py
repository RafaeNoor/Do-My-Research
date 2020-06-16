
from process_tweet_data import process_gender, process_sentiment

def do_complete_analysis(df,parent_dir,topic):

    print("REDDIT,DF",df)
    males, females = process_gender(df)

    file_paths = []

    print('###males',males)
    print('###females',females)

    file_paths.append(process_sentiment(males,"Males",parent_dir,topic))
    file_paths.append(process_sentiment(males,"Females",parent_dir,topic))

    df = df[:10]
    df = df.transpose()

    return {"file_paths":file_paths,"table_data":df.to_dict()}