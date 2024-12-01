from flask import Flask,render_template,request
import pickle
import numpy as np

popular_df=pickle.load(open('files/popular.pkl','rb'))
new_book=pickle.load(open('files/new_book.pkl','rb'))
similarity_score=pickle.load(open('files/similarity_score.pkl','rb'))
final_df=pickle.load(open('files/final_df.pkl','rb'))


app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           book_name = list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['num_ratings'].values),
                           rating=list(popular_df['avg_rating'].values),
                           year_of_publication=list(popular_df['Year-Of-Publication'].values),
                           amazon_url=list(popular_df['amazon_url'].values)
                           )

@app.route('/recommender')
def recommender():
    return render_template('recommender.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    book_index = np.where(final_df.index == user_input)[0][0]
    similar_books = sorted(list(enumerate(similarity_score[book_index])), key=lambda x: x[1], reverse=True)[1:5]

    data = []
    for i in similar_books:
        item = []
        temp_df = new_book[new_book['Book-Title'] == final_df.index[i[0]]]
        temp_df.drop_duplicates('Book-Title')
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['amazon_url'].values))
        data.append(item)

    return render_template('recommender.html',data=data)

@app.route('/contact')
def contact():
    return  render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)
