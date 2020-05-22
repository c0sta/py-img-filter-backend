from flask import Flask
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def login():
    # shows form
    return '''  
        <form> 
            <input type="text" name="username" />
            <input type="password" name="password" />
            <button type="submit">Submit</button>
        </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)
