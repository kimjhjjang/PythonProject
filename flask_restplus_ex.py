from flask import Flask
app = Flask(__name__)

#일반적인 라우트 방식
@app.route('/board')
def board():
    return '게시판'

# URL에 매개변수를 받는 방식
@app.route('/user/<username>')
def show_user_profile(username):
    return 'User %s' % username

# 위에 있는것이 Endpoint 역할을 해줍니다.
@app.route('/boards',defaults={'page':'index'})
@app.route('/boards/<page>')
def boards(page):
    return '게시판 %s' % page


app.run(host="localhost", port=5002)