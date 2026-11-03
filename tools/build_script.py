import re,sys,os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','canon'))
def paras(p):
    s=open(p).read()
    s=s.split('\n---\n',1)[1] if '\n---\n' in s else s
    s=re.sub(r' ?<!-- speak-tw-ok[^>]*-->','',s)
    return [x.strip() for x in s.strip().split('\n\n') if x.strip()]
def pages(t,limit=110):
    if len(t)<=limit or t.startswith('#') or t.startswith('【'): return [t]
    out=[];cur=''
    for sent in re.findall(r'[^。？！]*[。？！」]+」?|.+$',t):
        if cur and len(cur)+len(sent)>limit: out.append(cur);cur=''
        cur+=sent
    if cur: out.append(cur)
    return out
MAP={
'共同段落.md':[('C01','程真：'),('C02','多打的'),('C03','他跑八百公尺'),('C04','妳爸爸以為我們的開始是'),('C05','誤吃蝦仁'),('C07','他的心跳好像特別慢'),('C08','早上常常一起晨跑'),('C09','碰上寒流'),('C10','搭火車回學校'),('C12','有一年奧運'),('C13','在廚房跟我求婚'),('C14','那陣子我早上吐得厲害'),('C15','熱豆漿'),('C16','腳腫起來'),('C17','第一次聽到妳的心跳'),('C18','照超音波那天'),('C19','後來妳會踢了'),('C20','妳出生那天'),('C21','第一次抱妳的時候'),('C22','握住我的手指'),('C23','第一個詞是'),('C24','在別人面前不太笑'),('C25','發燒的那幾個晚上'),('C26','跑來我們房間'),('C27','還有妳的名字'),('C28','寫到這裡，我停下筆')],
'客廳線.md':[('N01','你們倆窩在沙發上'),('N02','如果跌倒了'),('N03','避風港'),('N04','接力賽裡，交棒的人'),('N05','好了，妳爸爸在叫我了')],
'照片線.md':[('T01','床頭櫃上那張照片'),('T02','去跑一場馬拉松'),('T03','他的跑鞋到現在'),('T04','還是習慣睡在中間'),('T05','一個人站在沙發上'),('T06','畫了一張全家福'),('T07','空蕩蕩的跑道'),('T08','要乖乖聽外婆的話')],
'照片線-後續.md':[('TS00','上一封信寫完的那天晚上'),('TS01','畢業典禮那天'),('TS02','我在醫院住了一個多月'),('TS03','先學會走'),('TS04','每個週末，妳都會問'),('TS05','先一個人回家'),('TS06','明天，媽媽就要回家了')],
'鏡子線.md':[('F01','鏡子裡的我'),('F02','升國中那年'),('F03','全世界只有外婆'),('F04','高二那年站上'),('F05','大一那年暑假'),('F06','身分證換新'),('F07','四百公尺跨欄'),('F08','每天早上的藥'),('F09','話已經到了嘴邊'),('F10','結婚第三年'),('F11','如果妳真的來了，媽媽想把'),('F12','電視裡的裁判喊')],
'鏡子線-後續.md':[('FS00','一封一封放在他面前'),('FS01','我哭得說不出話'),('FS02','筆電還開在餐桌上'),('FS03','第一次抱妳的時候，妳已經不小了'),('FS04','媽媽，晚安'),('FS05','外婆來看妳的那天'),('FS06','爸爸也寫一句')],
}
SFX={'電視裡的裁判喊':'【音效】電視轉播：起跑口令「各就位」','「預備——」':'【音效】「預備」之後兩秒的靜默','槍聲響了':'【音效】發令槍聲，接著觀眾歡呼'}
used=set()
def render(fname,ps,out,mapping=None,extra=None):
    mapping=mapping if mapping is not None else MAP.get(fname,[])
    for p in ps:
        for cid,kw in mapping:
            if kw in p and cid not in used:
                out.append(f'\n【CG {cid}】'); used.add(cid)
        for k,v in SFX.items():
            if p.startswith(k) or (k=='槍聲響了' and p.startswith(k)): out.append(v)
        for pg in pages(p):
            out.append(pg)
o=['# 交棒總在終點後：視覺小說劇本草稿','','自動由 canon/ 的定稿文字組成（tools/build_script.py）。一段一頁，超過約 110 字的段落在句號處拆成兩頁。【CG】標記表示從這一頁開始換成那張圖，直到下一個標記。CG 編號對照 CG清單.md。','','音樂（暫定，待作者決定）：轉播現場的環境音混進 BGM，不做逐句音效；只有口令與槍聲是單次音效。共同段落用主題曲；三條線各用主題曲的改編版（客廳線溫暖、照片線只剩鋼琴、鏡子線空靈）；後續沿用該線的版本，轉場 CG 時淡出再淡入。','','---','','## 共同段落','','【BGM】主題曲']
render('共同段落.md',[x for x in paras('共同段落.md') if not x.startswith('【分歧')],o)
o+=['','【選項】抬頭看向：房門外的客廳／床頭櫃上的照片／化妝台上的鏡子','','---','','## 客廳線（選「房門外的客廳」）','','【BGM】主題曲・客廳線版（溫暖）']
render('客廳線.md',paras('客廳線.md'),o)
o+=['','【轉場】淡出到白，停兩秒','','## 客廳線後續','']
ns=open('客廳線-後續.md').read().split('\n---\n',1)[1]
ns=re.sub(r' ?<!-- speak-tw-ok[^>]*-->','',ns)
head,rest=ns.split('【分歧：',1); rest=rest.split('】',1)[1]
boy=rest.split('## 學長',1)[1].split('## 學姊',1)[0]; girl=rest.split('## 學姊',1)[1].split('## 共同結尾',1)[0]; end=rest.split('## 共同結尾',1)[1]
sp=lambda t:[x.strip() for x in t.strip().split('\n\n') if x.strip()]
nmap=[('NS00','我們三個人坐在沙發上'),('NS01','全中運')]
render('x',sp(head),o,nmap)
o+=['','【選項】站在妳身後的是：田徑隊的學長／田徑隊的學姊','','### 學長']
render('x',sp(boy),o,[('NS02a','田徑隊的學長'),('NS03a','吃飯的時候，他很少說話'),('NS04a','他的跑鞋和妳的跑鞋'),('NS05','送走客人以後')])
o+=['','### 學姊']
used.discard('NS05')
render('x',sp(girl),o,[('NS02b','田徑隊的學姊'),('NS03b','吃飯的時候，她很少說話'),('NS04b','她的跑鞋和妳的跑鞋'),('NS05','送走客人以後')])
o+=['','### 共同結尾']
render('x',sp(end),o,[('NS06','接力賽裡，交棒以後')])
o+=['','---','','## 照片線（選「床頭櫃上的照片」）','','【BGM】主題曲・照片線版（只剩鋼琴）']
render('照片線.md',paras('照片線.md'),o)
o+=['','【轉場】淡出到黑，停兩秒','','## 照片線後續','']
render('照片線-後續.md',paras('照片線-後續.md'),o)
o+=['','---','','## 鏡子線（選「化妝台上的鏡子」）','','【BGM】主題曲・鏡子線版（空靈）']
render('鏡子線.md',paras('鏡子線.md'),o)
o+=['','【轉場】從槍聲後的靜默淡出，停兩秒','','## 鏡子線後續','']
render('鏡子線-後續.md',paras('鏡子線-後續.md'),o)
open('劇本草稿.md','w').write('\n\n'.join(x.strip('\n') for x in o if x.strip())+'\n')
allids=set(re.findall(r'^\| ([A-Z]+\d+[ab]?(?:／b)?) ',open('CG清單.md').read(),re.M))
print('placed',len(used),'missing',sorted(set(i for i in allids)-used))
