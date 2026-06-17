import streamlit as st
import pandas as pd 
import PyPDF2
from textblob import TextBlob
import plotly.express as px
import plotly.graph_objects as go
from collections import Counter
import re

st.set_page_config(page_title="Product Review Sentiment Analysis", layout="wide")

st.title("📊 Product Review Sentiment Analysis")
uploaded_file = st.file_uploader("Upload a PDF file containing product reviews", type=["pdf"])

def extract_text_from_pdf(pdf_file):
    """Extract text from an uploaded PDF file (works with PyPDF2 v2+ and older)."""
    # PyPDF2 v2+ uses PdfReader with .pages
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        pages = reader.pages
    except Exception:
        # Fallback for older PyPDF2 versions
        reader = PyPDF2.PdfFileReader(pdf_file)
        pages = [reader.getPage(i) for i in range(reader.numPages)]

    text = ""
    for page in pages:
        # page may come from different PyPDF2 versions
        if hasattr(page, "extract_text"):
            pg_text = page.extract_text()
        elif hasattr(page, "extractText"):
            pg_text = page.extractText()
        else:
            pg_text = None
        if pg_text:
            text += pg_text + "\n"
    return text

def get_sentiment(text):
    analysis = TextBlob(text)
    polarity = analysis.polarity
    if polarity > 0.1:
        return "Positive" , polarity
    elif polarity < -0.1:
        return "Negative" , polarity
    else:
        return "Neutral" , polarity

def split_reviews(text):

    reviews = re.split(r'\d+\.\s+', text)
    reviews = [r.strip() for r in reviews if r.strip() and len(r.strip()) > 20]

    return reviews

if uploaded_file is not None:
    text_content = extract_text_from_pdf(uploaded_file)
    reviews = split_reviews(text_content)
    st.success(f"Extracted {len(reviews)} reviews from the PDF.")
    results = []
    for i,review in enumerate(reviews):
        sentiment, polarity = get_sentiment(review)
        results.append({
            'Review_ID': i+1,
            'Review': review[:200] + "..." if len(review) > 200 else review,
            'Full_Review': review,
            'Sentiment': sentiment,
            'Polarity_Score': round(polarity, 3)
        })
    df = pd.DataFrame(results)
    col1 , col2 , col3 = st.columns(3)

    positive_count = len(df[df['Sentiment'] == 'Positive'])
    negative_count = len(df[df['Sentiment'] == 'Negative'])
    neutral_count = len(df[df['Sentiment'] == 'Neutral'])
    with col1:
        st.metric("Positive Reviews", positive_count,
                  f"{(positive_count/len(df)*100):.1f}%")
    with col2:
        st.metric("Negative Reviews", negative_count,
                  f"{(negative_count/len(df)*100):.1f}%")
    with col3:
        st.metric("Neutral Reviews", neutral_count,
                  f"{(neutral_count/len(df)*100):.1f}%")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        sentiment_counts = df['Sentiment'].value_counts()
        sentiment_df = sentiment_counts.reset_index()
        sentiment_df.columns = ['Sentiment', 'Count']
        fig_pie = px.pie(sentiment_df,
                        values='Count',
                        names='Sentiment',
                        title="Sentiment Distribution",
                        color='Sentiment',
                        color_discrete_map={'Positive': 'green',
                                            'Negative': 'red',
                                            'Neutral': 'blue'})
        st.plotly_chart(fig_pie, use_container_width=True)
    with col2:
        fig_bar = px.bar(sentiment_df,
                x='Sentiment',
                y='Count',
                title="Sentiment Counts",
                labels={'Sentiment': 'Sentiment', 'Count': 'Count'},
                color='Sentiment',
                color_discrete_map={'Positive': 'green',
                            'Negative': 'red',
                            'Neutral': 'blue'})
        st.plotly_chart(fig_bar, use_container_width=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        avg_polarity = df['Polarity_Score'].mean()
        st.metric("Average Polarity Score", f"{avg_polarity:.3f}")
    with col2:
        most_common = df['Sentiment'].mode()[0]
        st.metric("Most Common Sentiment", most_common)
    st.divider()

    fig_hist = px.histogram(df, x='Polarity_Score',
                         title="Polarity Score Distribution",
                         nbins=20,
                         labels={'Polarity_Score': 'Polarity Score'},
                         color_discrete_sequence=['green'])
    st.plotly_chart(fig_hist, use_container_width=True)

    st.divider()
    st.subheader("Review Details")

    filter_sentiment = st.multiselect(
        "Filter by Sentiment",
        options=['Positive', 'Negative', 'Neutral'],
        default=['Positive', 'Negative', 'Neutral']
    )

    filtered_df = df[df['Sentiment'].isin(filter_sentiment)]

    st.dataframe(filtered_df[['Review_ID', 'Review', 'Sentiment', 'Polarity_Score']],
                use_container_width=True,height=400)
    st.divider()

    st.subheader("Individual Review Analysis")
    review_id = st.selectbox("Select Review ID", 
                             options=df['Review_ID'].tolist())
    selected_review = df[df['Review_ID'] == review_id].iloc[0]

    st.write(f"**Sentiment:** {selected_review['Sentiment']}")
    st.write(f"**Polarity Score:** {selected_review['Polarity_Score']}")
    st.write("**Full Review Text:**")
    st.info(selected_review['Full_Review'])

    st.divider()

    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Analysis Results as CSV",
        data=csv,
        file_name='sentiment_analysis_results.csv',
        mime='text/csv'
    )
else:
    st.info("Please upload a PDF file to analyze product reviews.")

    st.markdown("""
    ### How to Use:
    1. Click the "Browse files" button to upload a PDF file containing product reviews.
    2. The app will extract the reviews, analyze their sentiment, and display the results.
    3. You can view summary metrics, visualizations, and filter reviews by sentiment.   
    4. Click on individual reviews to see their full text and sentiment details.
    5. Finally, you can download the analysis results as a CSV file for further use.
    """)