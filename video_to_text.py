import wave, math, contextlib
import speech_recognition as sr
from moviepy.editor import AudioFileClip
import nltk
import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
# Tokenizing Words
from nltk.tokenize import word_tokenize
from deepsegment import DeepSegment






def clean(text):
    sample = text.split('**')
    sample.pop(0)
    clean_text = ""
    i = 0
    for t in sample:
        if i % 2 != 0:
            clean_text += str(t)
        i += 1
        # print ("Clean Text: ", clean_text)
    return clean_text


# Stopwords
stop_words = set(stopwords.words("english"))

# Tokenize
def Wtokenize(text):
    words = word_tokenize(text)
    return words


# Frequency of each word
def gen_freq_table(text):
    freqTable = dict()
    words = Wtokenize(text)

    for word in words:
        word = word.lower()
        if word in stop_words:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1
    return freqTable

# Sentence Tokenize
def Stokenize(text):
    sentences = sent_tokenize(text)
    return sentences

# Storing Sentence Scores
def gen_rank_sentences_table(text):

    sentenceValue = dict()

    freqTable = gen_freq_table(text)

    sentences = Stokenize(text)

    for sentence in sentences:
        for word, freq in freqTable.items():
            if word in sentence.lower():
                if sentence in sentenceValue:
                    sentenceValue[sentence] += freq
                else:
                    sentenceValue[sentence] = freq
    return sentenceValue


def summary(text):
    sum = 0
    sentenceValue = gen_rank_sentences_table(text)
    for sentence in sentenceValue:
        sum += sentenceValue[sentence]
    avg = int(sum / len(sentenceValue))
    summary = ""
    sentences = Stokenize(text)
    for sentence in sentences:
        if (sentence in sentenceValue) and (sentenceValue[sentence] > (1.2 * avg)):
            summary += " " + sentence
    return summary




def main():
    
    # transcribed_audio_file_name = "transcribed_speech.wav"
    # zoom_video_file_name = "resources/sample_interview.m4a"
    # audioclip = AudioFileClip(zoom_video_file_name)
    # audioclip.write_audiofile(transcribed_audio_file_name)
    # with contextlib.closing(wave.open(transcribed_audio_file_name,'r')) as f:
    #     frames = f.getnframes()
    #     rate = f.getframerate()
    #     duration = frames / float(rate)
    # total_duration = math.ceil(duration / 60)
    # r = sr.Recognizer()
    # for i in range(0, total_duration):
    #     with sr.AudioFile(transcribed_audio_file_name) as source:
    #         audio = r.record(source, offset=i*60, duration=60)
    #     f = open("transcription.txt", "a")
    #     f.write(r.recognize_google(audio))
    #     f.write(" ")
    # f.close()

    with open('transcription.txt') as f:
        lines = f.readlines()
    print("LINES", lines)
    segmenter = DeepSegment('en')
    punctuated_lines = segmenter.segment(lines)
    print("punctuated_lines", punctuated_lines)
    summary_text = summary(lines)
    print("\nModel Summary: ")
    summary_list = summary_text.split(". ")
    for sentence in summary_list:
        print(sentence)
    text_file = open("summary.txt", "w")
    n = text_file.write(summary_text)
    text_file.close()

if __name__ == "__main__":
    main() 