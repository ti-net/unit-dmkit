import requests
import json
def evaluate(f_in,url,bot_id,user_id,f_out="evaluate_result",bernard_level=0,version="2.0",log_id="0",bot_session="",client_session="{\"client_results\":\"\", \"candidate_options\":[]}",source="KEYBOARD",type="TEXT",update="",asr_candidates=[]) :
    try :
        file_input=open(f_in,'r',encoding='utf-8')
    except :
        print('无法打开文件 %s'%f_in)
        exit()
    file_out=open(f_out,'w')
    json_header = {'Content-Type': 'application/json'}
    prase_data = {
        "bot_session": bot_session,
        "log_id": log_id,
        "request": {
            "bernard_level": bernard_level,
            "query": "",
            "query_info": {
                "asr_candidates": asr_candidates,
                "source": source,
                "type": type
            },
            "updates": update,
            "user_id": user_id,
            "client_session": client_session
        },
        "bot_id": bot_id,
        "version": version
    }
    requrl =url
    right_think=0
    right_word=0
    right_samples=0
    right_prediction=0
    number_cacul=0
    for row in file_input :
        if row :
            fail=0
            sentance=row.strip().split('\t')
            sentance.append('')
            prase_data["request"]["query"]=sentance[0]
            try :
                obj = requests.post(url, data=json.dumps(prase_data), headers=json_header)
                content = obj.json()
                print(content)
            except :
                print("a")
                if fail<3 :
                    fail+=1
                else :
                    file_out.write(sentance[0]+'\t'+'SYS_ERROR_URL'+'\n')
            if content:
                bot_resp=content
                try :
                    res=bot_resp['result']['response']['schema']
                    slot_str=''
                    for slot in res["slots"]:
                        slot_str += slot["name"] + ':' +  slot["original_word"] + '###'
                    slot_str=slot_str.rstrip('#')
                except :
                    file_out.write(sentance[0]+'\t'+'url返回错误'+sentance[1]+'\t'+sentance[2]+'\t'+'SYS_ERROR_JSON'+content+'\n')
                    continue
                number_cacul+=1
                if not (sentance[1]=='SYS_OTHER' or sentance[1]==''):
                    right_samples+=1
                    s1='正例样本'
                else :
                    s1='负例样本'
                if sentance[1]==res['intent'] :
                    s2=',意图正确'
                    right_think+=1
                else :
                    s2=',意图错误'
                word_l=sentance[2].split('###')
                word_l.sort()
                word_r=slot_str.split('###')
                word_r.sort()
                if len(word_l)==len(word_r):
                    task=0
                    for i in range(len(word_l)) :
                        if  word_l[i]!=word_r[i] :
                            task=1
                            break
                    if not task :
                        s3='词槽正确'
                        if s2==',意图正确' :
                            right_word+=1
                    else :
                        s3='词槽错误'
                if not (res['intent']=='SYS_OTHER' or res['intent']==''):
                    right_prediction+=1
                    s4='预测为正例'
                else :
                    s4='预测为负例'
                file_out.write(sentance[0]+'\t'+s1+s4+s2+s3+'\t'+sentance[1]+'\t'+sentance[2]+'\t'+res['intent']+'\t'+slot_str+'\n')
    file_input.close()
    file_out.close()
    file_out=open(f_out,'r+')
    content=file_out.read()
    file_out.seek(0,0)
    write_lines=''
    if number_cacul == 0 :
        write_lines+='对样本进行预测失败，请检查您的配置\n'
        print ('对样本进行预测失败，请检查您的配置')
        file_out.close()
        exit()
    write_lines+='已成功对%d个样本进行预测\n'%number_cacul
    print ('已成功对%d个样本进行预测'%number_cacul)
    if right_samples == 0 :
        write_lines+='error:识别为正例样本数为0，无法计算准确率\n'
        print ('error:识别为正例样本数为0，无法计算准确率')
    else :
        write_lines+='整体准确率:%.2f(%d/%d)\n'%(float(right_word)/float(right_prediction)*100,right_word,right_prediction)
        write_lines+='意图准确率:%.2f(%d/%d)\n'%(float(right_think)/float(right_prediction)*100,right_think,right_prediction)
        print ('整体准确率:%.2f(%d/%d)'%(float(right_word)/float(right_prediction)*100,right_word,right_prediction))
        print ('意图准确率:%.2f(%d/%d)'%(float(right_think)/float(right_prediction)*100,right_think,right_prediction))
    if right_samples == 0 :
        write_lines+='error:评估集合中正例样本数为0，无法计算召回率\n'
        print ('error:评估集合中正例样本数为0，无法计算召回率')
    else :
        write_lines+='整体召回率:%.2f(%d/%d)\n'%(float(right_word)/float(right_samples)*100,right_word,right_samples)
        write_lines+='意图召回率:%.2f(%d/%d)\n'%(float(right_think)/float(right_samples)*100,right_think,right_samples)
        print ('整体召回率:%.2f(%d/%d)'%(float(right_word)/float(right_samples)*100,right_word,right_samples))
        print ('意图召回率:%.2f(%d/%d)'%(float(right_think)/float(right_samples)*100,right_think,right_samples))
    file_out.write(write_lines+content)
    file_out.close()



my_access_token="24.4768757eec5992f123be23ed4e79fc60.2592000.1556071230.282335-15609885"
my_user_id="test"
my_bot_id=40475
my_f_in="test.txt"
url_address='https://aip.baidubce.com/rpc/2.0/unit/bot/chat?access_token='
my_url=url_address+my_access_token
evaluate(f_in=my_f_in,url=my_url,bot_id=my_bot_id,user_id=my_user_id)
