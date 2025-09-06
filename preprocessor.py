import re
import pandas as pd

def preprocess(data):
    # Regex: extract date + time + message together
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})\s-\s(.*)'

    messages = re.findall(pattern, data)

    # Separate date/time and messages
    date_strings = [f"{m[0]}, {m[1]}" for m in messages]
    user_messages = [m[2] for m in messages]

    # Create DataFrame
    df = pd.DataFrame({'message_date': date_strings, 'user_message': user_messages})

    # Convert to datetime
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M', errors='coerce')
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Split user and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 2:   # user + message present
            users.append(entry[1])
            messages.append(entry[2])
        else:   # system notifications
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Add extra time features
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
