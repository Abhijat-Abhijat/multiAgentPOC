from sklearn.feature_extraction.text import TfidfVectorizer
from util.tools import current_timestamp, make_msg

def agent10_task(message):
    text = message["content"]
    try:
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform([text])
        keywords = sorted(zip(vectorizer.get_feature_names_out(), X.toarray()[0]), key=lambda x: -x[1])[:5]
        keyword_list = [k[0] for k in keywords]
    except Exception as e:
        keyword_list = [str(e)]
    return make_msg(
        sender="agent10_keyword_extractor",
        receiver="orchestrator",
        task="return_keywords",
        content={"keywords": keyword_list, "timestamp": current_timestamp()},
        step=2
    )
