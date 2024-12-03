import streamlit as st
import preprocessor,helper
import seaborn as sns
import matplotlib.pyplot as plt

st.sidebar.title("Chat Analyser")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)

    st.dataframe(df)

    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.remove('group notification')
    user_list.sort()
    user_list.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):

        #Stat Area
        num_messages, words, num_media_messages,num_links = helper.fetch_stats(selected_user,df)

        st.title("Top Statistics")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)

        #monthly timeline
        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'],timeline['messsage'],color='violet')
        plt.xticks(rotation='vertical')
        plt.grid(True)
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['messsage'],color='green')
        plt.xticks(rotation='vertical')
        plt.grid(True)
        st.pyplot(fig)

        #activity map
        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            sns.barplot(x = busy_day.index, y = busy_day.values, hue = busy_day.index, palette='husl')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Most Busy Month")
            busy_month = helper.month_activity_map(selected_user,df)
            fig,ax = plt.subplots()
            sns.barplot(x = busy_month.index, y = busy_month.values, hue = busy_month.index, palette = 'husl')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
                
        st.title("Weekly Activity Map")
        user_heatmap = helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)       



        #finding the most busy users in a group (Group level)
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            x,new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            
            col1, col2 = st.columns(2)   

            with col1:
                sns.barplot(x = x.index,y = x.values , hue=x, palette="husl",edgecolor='black',linewidth=1.2)
                plt.xticks(rotation='vertical')
                st.pyplot(fig)

            with col2:
                st.dataframe(new_df)    

        #Wordcloud
        st.title("Wordcloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)        

        # most common words
        most_common_df = helper.most_common_words(selected_user,df)

        fig,ax = plt.subplots()
        sns.barplot(y = most_common_df[0], x = most_common_df[1], data = most_common_df, hue = most_common_df[0], palette='husl', orient='h')
        # plt.xticks(rotation='vertical')
        plt.xlabel("Count",fontsize=15)
        plt.ylabel("Words",fontsize=15)
        st.title('Most Common Words')
        st.pyplot(fig)

        #emoji analysis
        emoji_df = helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head())
            st.pyplot(fig)

        