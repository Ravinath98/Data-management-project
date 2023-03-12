from flask.app import Flask
from flask import request, render_template, redirect
from forms.dynamic_form import wrapper_func
import psycopg2  # pip install psycopg2
import psycopg2.extras
import nltk.data
# nltk.download('punkt')
import os

PRODUCT_IMAGES_FOLDER = os.path.join('static', 'product_images')

app = Flask('form_app')
app.config['PRODUCTS_FOLDER'] = PRODUCT_IMAGES_FOLDER #put all the product images to this folder

app.secret_key = "supersecretkey"

DB_HOST = "localhost"
DB_NAME = "datamanagment"
DB_USER = "ravi"
DB_PASS = "ravi"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)

@app.route('/', methods=['GET', 'POST'])
def main():
    asin='B01AUI4VVA' #asin of the product
    title='Testing product' #title of the product

    cursor = conn.cursor()
    querySelect = "select * from reviewsoriginaltest"
    cursor.execute(querySelect)

    #print("*******************************************************")
    res = cursor.fetchone()
    # print(res)

    # print(res[2])
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    output_text=tokenizer.tokenize(res[2])
    cursor.close()


    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # input_list = ['one', 'two', 'three','test','d']  # generate it as needed
    input_list=output_text
    prefs = wrapper_func(input_list)
    form = prefs(request.form)
    if request.method == 'POST' and form.validate():
        # print(request.form)
        temp_list=list(request.form.items())
        notIdea=''
        notTip=''
        tipIdea = ''
        temp_list_ideas=[]
        if len(temp_list)!=0:
            for i in temp_list:
                tipIdea=tipIdea+i[0]
                temp_list_ideas.append(i[0])
            tip = 'Yes'
            # print('output text: ')
            # print(output_text)
            # print('temp list: ')
            # print(temp_list)
            notIdea_list=[item for item in output_text if item not in temp_list_ideas]

            for i in notIdea_list:
                notIdea=notIdea+i

            # print('not idea: ')
            # print(notIdea)
            notTip='No'



        else:
            tipIdea=res[2]
            tip = 'No'

        cur.execute("INSERT INTO reviewstransformedtemp (tip,tipIdea) VALUES (%s,%s)", [tip, tipIdea])
        if len(notIdea)!=0:
            cur.execute("INSERT INTO reviewstransformedtemp (tip,tipIdea) VALUES (%s,%s)", [notTip, notIdea])
        cur.execute("DELETE FROM reviewsoriginaltest WHERE id = (SELECT id FROM reviewsoriginaltest ORDER BY id LIMIT 1)")
        conn.commit()
        cur.close()
        # do your logic with the submitted form data here
        return redirect('/')

    image_name=asin+'.jpg'
    full_filename = os.path.join(app.config['PRODUCTS_FOLDER'], image_name)
    return render_template("index.html", form=form,full_filename=full_filename,title=title)

if __name__ == '__main__':
    app.run(debug=True)