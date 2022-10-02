import joblib
import nltk
import pandas as pd

from fastapi import FastAPI, HTTPException
from nltk.tokenize import regexp_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem.porter import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# creating a FastAPI server
server = FastAPI(title='User API')

nltk.download('punkt')
nltk.download('stopwords')


users = {
    'christophe': 'laurence',
    'mounir': 'mazouari'
}

def authenticate_user(username, password):
    authenticated_user = False
    if username in users.keys():
        if users[username] == password:
            authenticated_user = True
    return authenticated_user


@server.get('/status')
async def return_status():
    '''
    returns 1 if the server.is up
    '''
    return 1

@server.get('/permissions')
async def return_permission(username: str = 'username', password: str = 'password'):
    if authenticate_user(username=username, password=password):
        return {'username': username, ' is allowed to use this api': 'yes' }
    else:
        raise HTTPException(status_code=403, detail='Authentication failed')



#################### Préparation des phrases pour la prediction: BEGIN ####################
def lower_and_tokenize(review):

    "la fonction prend en argument une colonne de textes"
    "renvoie, pour chauue ligne de la colonne, la liste des mots qui composent le texte"

    review = review.apply(lambda x : x.lower())

    return(review.apply(word_tokenize))


def filter_and_stem(review):

    "la fonction prend en argument une colonne de textes tokenizés"
    "renvoie la liste des mots sans les stop_words de la langue anglais"
    "et applique un stemmer pour n'en garder que la racine"

    stop_words = set(stopwords.words('english'))
    stop_words.update([",", "."])
    review = review.apply(lambda x : [mot for mot in x if mot not in stop_words])

    porter_stemmer = PorterStemmer()

    return(review.apply(lambda x : [porter_stemmer.stem(w) for w in x]))



### processer les phrases ###
def phrase_preprocessing(dataset):

    data = dataset.copy()

    data["Review_Text"] = lower_and_tokenize(data["Review_Text"])
    data["Review_Text"] = filter_and_stem(data["Review_Text"])
    data["Review_Text"] = data["Review_Text"].apply(lambda x : ' '.join(x))

    return(data.reset_index(drop=True))

########### Vectorizer la phrase ################
def apply_tfidf_test(vect_tfidf_on_train,test_dataset):

    "on prend le vectorizer dejà fité sur le jeu d'entrainement et on transforme le jeu de TEST en un array "
    "représentant la fréquence des mots de chaque ligne de données à l'aide de la méthode tf-idf "

    reviews_test_tfidf = vect_tfidf_on_train.transform(test_dataset["Review_Text"])

    df_reviews_test_tfidf = pd.DataFrame(reviews_test_tfidf.toarray(), columns=vect_tfidf_on_train.get_feature_names())

    return(df_reviews_test_tfidf)
#################### Préparation des phrases pour la prediction: END ####################


#################### Prediction du ressenti: BEGIN ####################

@server.get('/sentiment')
async def return_sentiment(username: str = 'username', password: str = 'password', sentence: str = 'hello world'):
    if not authenticate_user(username=username, password=password):
        raise HTTPException(status_code=403, detail='Authentication failed')

    vectorizer_loaded = joblib.load("tfidf_vectorizer.joblib")

    sentence_df = pd.DataFrame(data = {"Review_Text" : [sentence] } )
    sentence_preprocessed = phrase_preprocessing(sentence_df)
    sentence_vectorized = apply_tfidf_test(vectorizer_loaded, sentence_preprocessed)

    try:
       model_loaded = joblib.load("model_final_test.joblib")
    except:
        raise HTTPException(status_code=403, detail='cannot download model')

    sentiment = model_loaded.predict(sentence_vectorized)

    return {
        'username': username,
        'sentence': sentence,
        'score': sentiment[0]
    }

#################### Prediction du ressenti: BEGIN ####################

if __name__=="__main__":
    sentence = "However I have had bad experience camera has been handled in an unprofessional manner, the staff seems not really care our personal belongings"
    print(return_sentiment(username='christophe', password='laurence', sentence=sentence))
    sentence = "The Eiffel Tower is absolutely beautiful I love seeing the Eiffel Tower it has amazing views from the top it is truly a remarkable site"
    print(return_sentiment(username='christophe', password='laurence', sentence=sentence))
