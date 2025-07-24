import re
import pandas as pd
def preprocess(data):
    print("Preprocessing data...")
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[APMapm]{2})?\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    dates = [d.replace('\u202f', ' ') for d in dates]

    df = pd.DataFrame({'date': dates, 'message': messages})
    sample_date = df['date'].iloc[0].strip()

    if(re.search(r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[AP]M', sample_date)):
        df['date'] = pd.to_datetime(df['date'], format='%m/%d/%y, %I:%M %p - ')
    else:
        df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y, %H:%M - ')
    users= []
    messages = []
    for message in df['message']:
        entry = re.split('([\w\W]+?):\s', message)
    
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('Group Notification')
            messages.append(entry[0])

    df['user'] = users
    df.drop(columns=['message'], inplace=True)
    df['message'] = messages

    df['only_date'] = df['date'].dt.date
    df['Year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['Month'] = df['date'].dt.month_name()
    df['Day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['Hour'] = df['date'].dt.hour
    df['Minute'] = df['date'].dt.minute

    period = []
    for hour in df['Hour']:
        if hour == 23:
            period.append(str(hour) + '-' + str('00'))
        elif hour == 0:
            period.append(str('00') + '-' + str(hour + 1))
        else:
            period.append(str(hour) + '-' + str(hour + 1))

    df['period'] = period
    return df