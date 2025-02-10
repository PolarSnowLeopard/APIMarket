from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
import json
from openai import OpenAI
from dotenv import load_dotenv
from mock_data import MOCK_USER_INFO, MOCK_USER_ID, MOCK_PJ1_REPORT

load_dotenv()

app = Flask(__name__)
api = Api(app, version='1.0', title='My API',
          description='A simple demonstration of a Flask API with OpenAPI documentation')

ns = api.namespace('api', description='API operations')

user_nickname = api.model('UserNickname', {
    'nickname': fields.String(required=True, description='The user nickname')
})

user_id = api.model('UserID', {
    'user_id': fields.String(required=True, description='The user ID')
})

education_info = api.model('EducationInfo', {
    'college': fields.String(required=True, description='The college name'),
    'major': fields.String(required=True, description='The major name')
})

post_history = api.model('PostHistory', {
    'post_history': fields.String(required=True, description='The user post history')
})

email_content = api.model('EmailContent', {
    'email': fields.String(required=True, description='The email address'),
    'education_description': fields.String(required=True, description='The education description'),
    'recent_life_status': fields.String(required=True, description='The recent life status')
})

weather_request = api.model('WeatherRequest', {
    'location': fields.String(required=True, description='The location'),
    'time': fields.String(default='now', description='The time')
})

calculation_request = api.model('CalculationRequest', {
    'formula': fields.String(required=True, description='The formula to calculate')
})

report_request = api.model('ReportRequest', {
    'message': fields.String(required=False, description='The report message, the prediction result of the model')
})

@ns.route('/get_user_id')
class GetUserID(Resource):
    @ns.expect(user_nickname)
    @ns.doc(description='获取给定昵称的用户ID。返回与该昵称关联的用户ID，如果昵称不存在则返回空对象。')
    def post(self):
        data = request.json
        nickname = data.get('nickname')
        return jsonify(MOCK_USER_ID.get(nickname, {}))

@ns.route('/get_user_info')
class GetUserInfo(Resource):
    @ns.expect(user_id)
    @ns.doc(description='获取给定用户ID的用户信息。返回与该ID关联的用户信息，如果ID不存在则返回空对象。')
    def post(self):
        data = request.json
        user_id = data.get('user_id')
        return jsonify(MOCK_USER_INFO.get(user_id, {}))

@ns.route('/generate_education_description')
class GenerateEducationDescription(Resource):
    @ns.expect(education_info)
    @ns.doc(description='生成院校与专业的介绍。使用 OpenAI 模型生成给定院校和专业的中文描述。')
    def post(self):
        data = request.json
        college = data.get('college')
        major = data.get('major')
        prompt = f"根据给定的学校名称与专业名称生成对该院校与专业的介绍：\n{college} {major}\n"
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的院校与专业介绍分析师。"
                 "请撰写一段邮件内容，介绍给定的院校与专业。你的回答只需要包含一段话，"
                 "不要包含称谓、落款、日期等任何信息，不要进行任何解释。你必须用中文进行交互"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].message.content

@ns.route('/summarize_recent_life_status')
class SummarizeRecentLifeStatus(Resource):
    @ns.expect(post_history)
    @ns.doc(description='根据用户的帖子历史总结用户的近期生活状态。使用 OpenAI 模型生成中文描述。')
    def post(self):
        data = request.json
        post_history = data.get('post_history')
        prompt = f"根据以下用户帖子历史，总结用户的近期生活状态：\n{post_history}\n"
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "你是一个专业的用户分析师，擅长根据用户发帖记录总结用户近期生活状态，"
                 "并撰写一段邮件内容。你的回答只需要包含一段话，"
                 "不要包含称谓、落款、日期等任何信息，不要进行任何解释。用“你”作为开头。你必须用中文进行交互"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=512,
            n=1,
            stop=None,
            temperature=0.7
        )
        return response.choices[0].message.content

@ns.route('/send_email')
class SendEmail(Resource):
    @ns.expect(email_content)
    @ns.doc(description='发送包含用户教育描述和近期生活状态的邮件。模拟发送邮件并返回确认消息。')
    def post(self):
        data = request.json
        email = data.get('email')
        education_description = data.get('education_description')
        recent_life_status = data.get('recent_life_status')
        print(f"Sending email to {email}...")
        print(f"Education description: {education_description}")
        print(f"Recent life status: {recent_life_status}")
        return "Sent!"

@ns.route('/get_weather')
class GetWeather(Resource):
    @ns.expect(weather_request)
    @ns.doc(description='获取给定地点和时间的当前天气信息。返回模拟的天气数据。')
    def post(self):
        data = request.json
        location = data.get('location')
        time = data.get('time', 'now')
        return jsonify({"location": location, "temperature": "25", "time": time})

@ns.route('/calculate')
class Calculate(Resource):
    @ns.expect(calculation_request)
    @ns.doc(description='计算给定数学公式的结果。模拟计算并返回固定结果。')
    def post(self):
        data = request.json
        formula = data.get('formula')
        print("Calculating...")
        print(f"Formula: {formula}")
        print(f"Result: {1}")
        return jsonify({"result": 1})

@ns.route('/pj1_report')
class PJ1Report(Resource):
    @ns.expect(report_request)
    @ns.doc(description='生成课题一算法模型在给定数据集的推理结果的报告。')
    def post(self):
        data = request.json
        message = data.get('message')
        if not message:
            return jsonify({"result": MOCK_PJ1_REPORT})
        prompt = f"你是一个专业的报告生成器，下面是跨境贸易支付监测课题一算法模型（基于图神经网络）在数据集上的推理结果，请根据给定的输入生成专业的模型效果报告。你的报告应尽可能详细，不要包含任何称谓、落款、日期等任何信息，不要进行任何解释。你必须用中文进行交互：\n{message}\n"
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4",  # 选择合适的引擎
            messages=[
                {"role": "system", "content": "你是一个专业的报告生成器。"
                "请撰写报告，总结给定模型的推理结果。你的回答应尽可能详尽，且确保专业"
                "不要包含称谓、落款、日期等任何信息，不要进行任何解释。你必须用中文进行交互"},
                {"role": "user", "content": prompt}
            ],
            max_tokens=5120,  # 设置生成文本的最大长度
            n=1,
            stop=None,
            temperature=0.7  # 控制生成文本的随机性
        )
        return jsonify({"result": response.choices[0].message.content})

@ns.route('/exit_script')
class ExitScript(Resource):
    @ns.doc(description='结束脚本并终止交互。模拟退出操作。')
    def post(self):
        print("Exiting script...")
        return "Exited"

if __name__ == '__main__':
    app.run(debug=True)