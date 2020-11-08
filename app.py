from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.seoul_matjip


# HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('index.html')


# API 역할을 하는 부분
@app.route('/api/restaurant_list', methods=['GET'])
def show_matjips():
    # 1. db에서 mystar 목록 전체를 검색합니다. ID는 제외하고 like 가 많은 순으로 정렬합니다.
    matjips = list(db.restaurants.find({}, {'_id':False}).sort('like',-1))
    print(matjips)
    # 참고) find({},{'_id':False}), sort()를 활용하면 굿!

    # 2. 성공하면 success 메시지와 함께 stars_list 목록을 클라이언트에 전달합니다.
    return jsonify({'result': 'success', 'msg': 'list 연결되었습니다!', 'list': matjips})


@app.route('/api/restaurant_like', methods=['POST'])
def like_matjips():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name = request.form["name"]

    # 2. mystar 목록에서 find_one으로 name이 name_receive와 일치하는 star를 찾습니다.
    current_like = db.restaurants.find_one({'name':name})["like"]
    # 3. star의 like 에 1을 더해준 new_like 변수를 만듭니다.
    new_like = current_like + 1
    # 4. mystar 목록에서 name이 name_receive인 문서의 like 를 new_like로 변경합니다.
    # 참고: '$set' 활용하기!

    db.restaurants.update_one({'name': name}, {'$set':{'like': new_like}})
    # 5. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': name+'좋아'})


@app.route('/api/delete', methods=['POST'])
def delete_star():
    # 1. 클라이언트가 전달한 name_give를 name_receive 변수에 넣습니다.
    name = request.form["name"]
    # 2. mystar 목록에서 delete_one으로 name이 name_receive와 일치하는 star를 제거합니다.
    db.restaurants.delete_one({'name':name})
    # 3. 성공하면 success 메시지를 반환합니다.
    return jsonify({'result': 'success', 'msg': name+'삭제~'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)