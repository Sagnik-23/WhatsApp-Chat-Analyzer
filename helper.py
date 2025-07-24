from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extractor = URLExtract()

english_stopwords = [
    "i", "me", "my", "myself", "we", "our", "ours", "you", "your", "yours",
    "he", "she", "it", "they", "them", "his", "her", "its", "their",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "having", "do", "does", "did", "doing",
    "a", "an", "the", "and", "but", "if", "or", "because", "as", "until",
    "while", "of", "at", "by", "for", "with", "about", "against", "between",
    "into", "through", "during", "before", "after", "above", "below", "to",
    "from", "up", "down", "in", "out", "on", "off", "over", "under",
    "again", "further", "then", "once", "here", "there", "when", "where",
    "why", "how", "all", "any", "both", "each", "few", "more", "most",
    "other", "some", "such", "no", "nor", "not", "only", "own", "same",
    "so", "than", "too", "very", "can", "will", "just", "don", "should",
    "now", "okay", "ok", "hmm", "hm", "yeah", "yes", "no", "na", "huh", "uhh",
    "please", "thanks", "thank", "welcome", "sorry", "well", "oh", "hey", "hi",
    "hello", "bye", "goodbye", "see", "later", "sure", "maybe", "really", "got",
    "get", "gotta", "wanna", "gonna", "didn't", "doesn't", "isn't", "aren't",
    "wasn't", "weren't", "hasn't", "haven't", "hadn't", "won't", "wouldn't",
    "couldn't", "shouldn't", "might", "mightn't", "must", "mustn't", "let", "lets"
]

benglish_stopwords = [
    "ami", "tumi", "amra", "tora", "ora", "se", "oke", "amar", "tomar", "tor", "or",
    "kothay", "keno", "ki", "je", "na", "ha", "haa", "hain", "nai", "ache", "nei",
    "eta", "ota", "ekta", "akta", "onek", "kichu", "jodi", "bar", "abar", "karon",
    "tai", "tahole", "kintu", "kintu", "keno", "kirokom", "kichu", "kichutei",
    "ekhon", "tarpor", "poro", "bujhli", "bol", "bolchi", "bolbo", "bolish",
    "chilo", "chhilo", "chhena", "chena", "korchi", "korbo", "korish", "korse",
    "ja", "jao", "jacchi", "asche", "gesi", "jabe", "kheye", "khacchi",
    "bhalo", "valo", "thik", "thikache", "thikase", "thikase", "thikache", "thik",
    "ki", "keno", "kothay", "kibhabe", "kemon", "kemon", "kisu", "kichu", "kichutei",
    "ekhon", "tarpor", "poro", "bujhli", "bol", "bolchi", "bolbo", "bolish",
    "chilo", "chhilo", "chhena", "chena", "korchi", "korbo", "korish", "korse",
    "ja", "jao", "jacchi", "asche", "gesi", "jabe", "kheye", "khacchi",
    "hoye", "hoy", "holo", "hobe", "hobena", "parbo", "parchi", "parish", "parena",
    "dilam", "dile", "dilo", "diben", "dibi", "diche", "dichhi", "dichhe", "dilam",
    "korte", "korlam", "korle", "korlo", "korben", "korbi", "korche", "korchhi", "korchhe","baahane", "bhalo", "valo", "thik", "thikache", "thikase", "thikache", "thik",
    "kotha", "kothao","bhai","tui","iyee","baje","kor","bero","ghuma","e","toh","ta","kore","r", "ei","te",
    "theke",
    "er",
    "bole",
    "ei",
    "hbe",
    "hoe",
    "nie",
    "toke",
    "besi", "j", "aj", "oi","ke","jai","bye","jani","kal","sei","k","keno"
]
chat_fillers = [
    "😂", "😅", "❤️", "👍", "🥲", "🙂", "🙄", "😁", "🙃", "🤔",
    "ok", "okay", "hmm", "hm", "huh", "nah", "lol", "lmao", "hehe", "uff",
    "haye", "oy", "arre", "re", "arey", "o", "ar"
]


def fetch_stats(selected_user, df):

    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    
    num_messages = df.shape[0]


    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extractor.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(columns={'index': 'user', 'user': 'percentage'})
    return x, df

def create_wordcloud(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]
    
    #removing media messages
    df = df[df['message'] != '<Media omitted>\n']
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['message'].str.cat(sep=" "))

    return df_wc

def most_Common_words(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    temp = df[df['message'] != '<Media omitted>\n']
    temp = temp[temp['message'] != 'group notification\n']

    words = []

    for message in temp['message']:
        for word in message.lower().split():
            if word not in english_stopwords and word not in benglish_stopwords and word not in chat_fillers:
                words.append(word)
    return_df = pd.DataFrame(Counter(words).most_common(20))

    return return_df

def emoji_analysis(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    emoji_df.columns = ['Emoji', 'Count']
    
    return emoji_df

def monthly_timeline(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['message'].reset_index()
    time = []
    for i in range(len(timeline)):
        time.append(str(timeline['Month'][i]) + '-' + str(timeline['Year'][i]))
    timeline['time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()

    return daily_timeline

def week_activity_map(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    return df['day_name'].value_counts()

def month_activity_map(selected_user, df):
    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    return df['Month'].value_counts()

def activity_heatmap(selected_user, df):
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    period_order = ['10-11', '11-12', '12-13', '13-14', '14-15', '15-16', '16-17', '17-18', '18-19', '19-20', '20-21', '21-22', '22-23', '23-00', '00-1', '1-2', '2-3', '3-4', '4-5', '5-6', '6-7', '7-8', '8-9', '9-10']

    if selected_user != 'All':
        df = df[df['user'] == selected_user]

    df['day_name'] = pd.Categorical(df['day_name'], categories=day_order, ordered=True)
    df['period'] = pd.Categorical(df['period'], categories=period_order, ordered=True)

    user_heatmap = df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)
    return user_heatmap