from transformers import pipeline

# Русскоязычные модели для саммари
summarizer = pipeline("summarization", model="IlyaGusev/rut5_base_sum_gazeta")

def summarize(config, text):
    summary = summarizer(text, max_length=150, min_length=30, do_sample=False)
    
    return summary[0]["summary_text"]
