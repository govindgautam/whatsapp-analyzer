from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
extractor = URLExtract()
def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    num_messages = df.shape[0]
    
    # Count words
    words = []  
    for message in df['message']:
        words.extend(message.split())
    
    # Count media messages (moved outside the loop)
    num_media_message = df[df['message'] == '<Media omitted>'].shape[0]
    
    #fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))
    num_links = len(links)

    return num_messages, len(words), num_media_message , num_links

def most_busy_users(df):
    x = df['user'].value_counts().head()
    new_df=round(df['user'].value_counts()/df.shape[0]*100,2).reset_index().rename(columns={'index':'name' , 'user':'perecent'})  # average messages per user
    return x,new_df

def create_wordcloud(selected_user, df):
                  if selected_user != 'Overall':
                      df = df[df['user'] == selected_user]
                  
                  wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
                  df_wc = wc.generate(df['message'].str.cat(sep=" "))
                  return df_wc
def most_common_words(selected_user, df):
                  if selected_user != 'Overall':
                      df = df[df['user'] == selected_user]
                  
                  f = open('stop_hinglish.txt', 'r' , encoding='utf-8')
                  stop_words = f.read().split('\n')

                  df = df[df['user'] != 'group_notification']
                  df = df[df['message'] != '<Media omitted>']
                  df.reset_index(drop=True, inplace=True)
                  
                  words = []
                  for message in df['message']:
                      for word in message.lower().split():
                          if word not in stop_words:
                              words.append(word)
                  
                  from collections import Counter
                  most_common_df = pd.DataFrame(Counter(words).most_common(20))
                  return most_common_df
def emoji_helper(selected_user, df, top_n=20):
    import emoji
    from collections import Counter
    import pandas as pd
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emoji_list = []
    for message in df['message']:
        emoji_list.extend([c for c in message if c in emoji.EMOJI_DATA])
    
    emoji_counter = Counter(emoji_list)
    emoji_df = pd.DataFrame(emoji_counter.most_common(top_n), columns=['Emoji', 'Count'])
    
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # This line should be OUTSIDE the if block
    timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()
    
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + " " + str(timeline['year'][i]))
    
    timeline['time'] = time
    return timeline  # Return the DataFrame, not the time list
