import streamlit as st
import pandas as pd
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    st.dataframe(df)

    # Fetch unique users
    user_list = df['user'].unique().tolist()
    
    # Check if 'group_notification' exists before removing it
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    
    user_list.sort()
    user_list.insert(0, "Overall")
    
    # Get the selected user from the selectbox
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)

    if st.sidebar.button("Show Analysis"):
        col1, col2, col3, col4 = st.columns(4)
        
        # Use the actual selected user value
        num_messages, words, num_media_message, num_links = helper.fetch_stats(selected_user, df)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_message)
        with col4:
            st.header("link Shared")
            st.title(num_links)

        # Finding the user with the most messages group level
        if selected_user == 'Overall':
            st.title('Most Busy Users')
            
            # Get both return values from the function
            x, new_df = helper.most_busy_users(df)
            
            col1, col2 = st.columns(2)
            
            with col1:
                fig, ax = plt.subplots()
                ax.bar(x.index, x.values, color='orange')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            
            with col2:
                # You can also display the percentage dataframe if you want
                st.dataframe(new_df)
        
        # Word cloud - This should be OUTSIDE the if selected_user == 'Overall' block
        st.title("Word Cloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        # Most common words - This should be OUTSIDE the if selected_user == 'Overall' block
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        fig, ax = plt.subplots()
        ax.bar(most_common_df[0], most_common_df[1], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        st.dataframe(most_common_df)

        #emoji analysis
        st.title("Emoji Analysis")
        
        emoji_df = helper.emoji_helper(selected_user,df)
        col1,col2= st.columns(2)
        with col1:
         st.dataframe(emoji_df)
        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df['Count'].head(), labels=emoji_df['Emoji'].head(),autopct="%0.2f")  # Use column names
            st.pyplot(fig)

         #timeline analysis

        st.title("Monthly Timeline")
        timeline = helper.monthly_timeline(selected_user,df)
        fig,ax = plt.subplots()
        ax.plot(timeline['time'], timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)