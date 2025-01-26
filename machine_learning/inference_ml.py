import joblib

# Caminhos para os arquivos salvos
model_path = 'models/sentiment_classifier_model.pkl'
vectorizer_path = 'models/tfidf_vectorizer.pkl'
label_encoder_path = 'models/label_encoder.pkl'

# Carregar os arquivos salvos
classifier = joblib.load(model_path)
vectorizer = joblib.load(vectorizer_path)
label_encoder = joblib.load(label_encoder_path)

# Novo texto para inferência
new_text = ["O filme foi maravilhoso, cheio de emoção e uma ótima história!"]
new_text_tfidf = vectorizer.transform(new_text)
predicted_label_encoded = classifier.predict(new_text_tfidf)
predicted_label = label_encoder.inverse_transform(predicted_label_encoded)

print(f"Texto: {new_text[0]}")
print(f"Sentimento previsto: {predicted_label[0]}")