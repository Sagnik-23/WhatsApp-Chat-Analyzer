import streamlit as st
import preprocess
import helper
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="WhatsApp Chat Analyzer", layout="wide")
st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload your WhatsApp chat file", type=["txt"])
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocess.preprocess(data)

    # st.dataframe(df)

    user_list = df['user'].unique().tolist()
    user_list.remove('Group Notification')
    user_list.sort()

    selected_user = st.sidebar.selectbox("Select User", options=["All"] + user_list, key="user_filter")

    if st.sidebar.button("Analyze"):
        num_messages, words , num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.subheader(num_messages) 
        with col2:
            st.header("Total Words")
            st.subheader(words)
        with col3:
            st.header("Media Shared")
            st.subheader(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.subheader(num_links)


        # Monthly Timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots()

        ax.plot(timeline['time'], timeline['message'], marker='o')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Daily Timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(daily_timeline['only_date'], daily_timeline['message'], color='black')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Finding busiest day
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.subheader("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        # heatmap
        st.title("Activity Heatmap")
        heatmap = helper.activity_heatmap(selected_user, df)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax = sns.heatmap(heatmap)
        plt.title("Activity Heatmap")
        st.pyplot(fig)

        # finding busiest users
        if selected_user == 'All':
            st.subheader("Most Busy Users")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index, x.values)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        # Word Cloud
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        st.title("Most Common Words")
        common_words = helper.most_Common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.barh(common_words[0],common_words[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.dataframe(common_words)

        st.title("Emoji Analysis")
        emoji_df = helper.emoji_analysis(selected_user, df)
        def is_emoji_supported(char):
            try:
                test_fig, test_ax = plt.subplots()
                test_ax.text(0.5, 0.5, char, fontsize=20)
                plt.close(test_fig)
                return True
            except:
                return False

        emoji_df = emoji_df[emoji_df['Emoji'].apply(is_emoji_supported)]
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)
        with col2:
            plt.rcParams['font.family'] = 'Segoe UI Emoji'

            fig, ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(5), labels=emoji_df['Emoji'].head(5) , autopct='%0.2f%%', startangle=140)
            st.pyplot(fig)