import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline



def create_summary(get_summary, whole_text):
    st.write("Preparing your summary...")
    summarized_text = get_summary(whole_text)
    st.write("Key Points")
    summary_str = ""
    summary_str += "Key Points \n"
    global_summary = summarized_text
    for point in summarized_text:
        st.write(str(point))
        summary_str += point
    return summary_str


def get_summary(text):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    num_iters = int(len(text)/1000)
    summarized_text = []
    for i in range(0, num_iters + 1):
        start = 0
        start = i * 1000
        end = (i + 1) * 1000
        out = summarizer(text[start:end])[0]['summary_text']
        summarized_text.append(out)
    return summarized_text

def show_similarity(final_summary, whole_text):
    scorer = rouge_scorer.RougeScorer(['rouge3'], use_stemmer=True)
    scores = scorer.score(final_summary,whole_text)
    st.success("The summary is " + str(round(float(scores["rouge3"].recall)*100,2)) + "\% similar to the video.")
    return round(float(scores["rouge3"].recall)*100,2)


def app():
    st.title("Explore")
    lst = []
    with open('summaries.txt') as file:
        for line in file:
            title, link, desc = line.split(":::")
            lst.append([title, link, desc])
            with st.expander(title):                
                video_id = link.split("=")[1]
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                text = ""
                for i in transcript:
                    text += ' ' + i['text']
                final_summary = create_summary(get_summary, text)  
                show_similarity(final_summary, text)
    
    
    print(lst[0][0], lst[0][0])
    with st.expander(lst[0][0]):                
                video_id = lst[0][1].split("=")[1]
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                text = ""
                for i in transcript:
                    text += ' ' + i['text']
                final_summary = create_summary(get_summary, text)  
                show_similarity(final_summary, text)





    