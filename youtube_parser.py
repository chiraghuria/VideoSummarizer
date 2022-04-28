from youtubesearchpython import VideosSearch
import json
from src import summarize_page
from youtube_transcript_api import YouTubeTranscriptApi
search = VideosSearch('TED Talk')
import streamlit as st
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline



def create_summary(get_summary, whole_text):
    summarized_text = get_summary(whole_text)
    summary_str = ""
    summary_str += "Key Points \n"
    global_summary = summarized_text
    for point in summarized_text:
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
    return round(float(scores["rouge3"].recall)*100,2)




file = open("summaries.txt", "w")
file.close()


file = open("summaries.txt", "a") 
for result in search.result()['result']:
    print(result)
    # vidoes_dict = json.loads(result)
    
    video_id = result["link"].split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = ""
    for i in transcript:
        text += ' ' + i['text']
    final_summary = create_summary(get_summary, text)  
    similarity = str(show_similarity(final_summary, text))    
    
    with open(result["link"], 'w') as f:
        f.write(final_summary)
    
    file.write(result["title"]+":::"+result["link"]+":::"+result["accessibility"]["title"]+ ":::"+similarity + "\n")
file.close()



submitted = st.form_submit_button(label="Summarize")
if submitted:
    video_id = link.split("=")[1]
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    text = ""
    for i in transcript:
        text += ' ' + i['text']
    final_summary = summarize_page.create_summary(summarize_page.get_summary, text)  
    summarize_page.show_similarity(final_summary, text)
    
                
                
                
                
                

# ''' Getting result from 2nd page. '''
# search.next()
# print(search.result()['result'])

# ''' Getting result from 3rd page. '''
# search.next()
# print(search.result()['result'])

# ''' Getting result from 4th page. '''
# search.next()
# print(search.result()['result'])