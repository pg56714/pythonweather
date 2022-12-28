from flask_ngrok import run_with_ngrok
from flask import Flask, request

# 載入 LINE Message API 相關函式庫
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

# 載入 json 標準函式庫，處理回傳的資料格式
import json

app = Flask(__name__)

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)                     # 取得收到的訊息內容
    try:
        json_data = json.loads(body)                     # json 格式化訊息內容
        access_token = 'tVbcl+a9nJf8KSMDme2/lkfDLBAJdmvUSLtru+mkGNCpphXbhwUuJqYOdHluCnmDsD2bhWoRcDhifsWkn4lrwYpr5UFV7ymmjGRu91TemhcSRRKrs87UbQqjO+uGsdozfd0DUF58za0rLk0FMOcW8wdB04t89/1O/w1cDnyilFU='
        secret = 'ad55a13441bb3da9191f66fc5169958f'
        line_bot_api = LineBotApi(access_token)                # 確認 token 是否正確
        handler = WebhookHandler(secret)                   # 確認 secret 是否正確
        signature = request.headers['X-Line-Signature']            # 加入回傳的 headers
        handler.handle(body, signature)                    # 綁定訊息回傳的相關資訊
        msg = json_data['events'][0]['message']['text']            # 取得 LINE 收到的文字訊息
        tk = json_data['events'][0]['replyToken']               # 取得回傳訊息的 Token

        #抓天氣預報資料
        #x=input('請輸入縣市:')
        url="https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-9BD40C7F-D603-470B-AF70-9F88BA32B8CC&locationName=" + msg
        headers = {'Accept': 'application/json'}
        data = requests.get(url, headers=headers)
        data=data.json()
        city=str(data['records']['location'][0]['locationName'])
        start=str(data['records']['location'][0]['weatherElement'][2]['time'][2]['startTime'])
        tempmin=str(data['records']['location'][0]['weatherElement'][2]['time'][2]['parameter']['parameterName'])+"度"
        tempmax=str(data['records']['location'][0]['weatherElement'][4]['time'][2]['parameter']['parameterName'])+"度"
        rain=str(data['records']['location'][0]['weatherElement'][1]['time'][2]['parameter']['parameterName'])+"%"
        end=str(data['records']['location'][0]['weatherElement'][2]['time'][2]['endTime'])
        msg1='✨'+city+'✨\n'+start+"~\n"+end+"\n❄️最低溫是："+tempmin+"，\n🔥最高溫是："+tempmax+"；\n💧降雨機率是:"+rain+'\n\n數據取自中央氣象局'
        #print(msg)

        #判斷貼圖(降雨機率)
        if(rain > '50'):
          PID = 11537
          SID = 52002750
          #image1 = 'https://imgur.dcard.tw/CdUYfMih.jpg'
          #image2 = 'https://imgur.dcard.tw/CdUYfMih.jpg'
        if(rain == '50'):
          PID = 11537
          SID = 52002749
        if(rain < '50'):
          PID = 11537
          SID = 52002735
          #image1 = 'https://e.share.photo.xuite.net/h00889942/1ec167e/12844799/649636735_m.jpg'
          #image2 = 'https://e.share.photo.xuite.net/h00889942/1ec167e/12844799/649636735_m.jpg'


        line_bot_api.reply_message(tk,TextSendMessage(msg1,package_id=PID, sticker_id=SID))           # 回傳訊息
        #print(msg, tk)                             # 印出內容
    except:
        msg1 = '查無此縣市，請重新輸入!'
        line_bot_api.reply_message(tk,TextSendMessage(msg1))
        #print(msg1, tk)
        #print(body)                               # 如果發生錯誤，印出收到的內容
    return 'OK'                                   # 驗證 Webhook 使用，不能省略
if __name__ == "__main__":
  run_with_ngrok(app)                                 # 串連 ngrok 服務
  app.run()
  