from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# 角色配置数据
CHARACTERS = {
    "ningjing": {
        "id": "ningjing",
        "name": "宁静",
        "title": "清醒的局外人",
        "keywords": ["独立自我", "拒绝内耗", "霸气直爽"],
        "description": "你是天生的'破局者'，讨厌弯弯绕绕的潜规则，信奉实力说话。你看似冷漠，实则活得最通透，拒绝任何形式的道德绑架。",
        "quote": "还要我怎样？",
        "color": "#8B0000"
    },
    "xuqing": {
        "id": "xuqing",
        "name": "许晴",
        "title": "浪漫的破碎公主",
        "keywords": ["理想主义", "情绪敏感", "追求浪漫"],
        "description": "你是团队里的'情感温度计'，拥有最纯粹的童心和对世界美好的向往，但同时也极易受伤。你渴望被理解、被宠爱。",
        "quote": "我觉得我快碎了",
        "color": "#FF69B4"
    },
    "zhengshuang": {
        "id": "zhengshuang",
        "name": "郑爽",
        "title": "高敏感的讨好者",
        "keywords": ["内心戏丰富", "容易委屈", "害怕冲突"],
        "description": "你是团队里的'受气包'兼'粘合剂'，心思细腻，总能第一时间察觉到他人的情绪变化，却往往忽略了自己。",
        "quote": "我不知道该说什么...",
        "color": "#DDA0DD"
    },
    "maoamin": {
        "id": "maoamin",
        "name": "毛阿敏",
        "title": "智慧的定海神针",
        "keywords": ["包容大气", "高情商", "从容淡定"],
        "description": "你是团队的'精神支柱'，无论局面多混乱，你总能云淡风轻地化解尴尬。你看破不说破，用温柔的方式包容所有人。",
        "quote": "没事，我来弄",
        "color": "#4682B4"
    },
    "jingboran": {
        "id": "jingboran",
        "name": "井柏然",
        "title": "暖心的全能管家",
        "keywords": ["责任感强", "细腻体贴", "默默承受"],
        "description": "你是团队里的'贴心小棉袄'，明明年纪不大，却操着最多的心。从记账到做饭，你总是冲在最前面照顾大家。",
        "quote": "姐，我来搬",
        "color": "#20B2AA"
    },
    "yangyang": {
        "id": "yangyang",
        "name": "杨洋",
        "title": "沉默的行动派",
        "keywords": ["高冷寡言", "默默做事", "执行力强"],
        "description": "你是团队里的'沉默守护者'，话不多但事都做了。不善于表达情感，但会用行动证明自己的担当。",
        "quote": "（默默干活）",
        "color": "#708090"
    },
    "chenyihan": {
        "id": "chenyihan",
        "name": "陈意涵",
        "title": "元气的冒险背包客",
        "keywords": ["精力旺盛", "随遇而安", "大大咧咧"],
        "description": "你是团队的'能量电池'，只要有你在，就不会冷场。你对世界充满好奇，不怕苦不怕累，享受混乱带来的刺激。",
        "quote": "走！我们去爬山！",
        "color": "#FFD700"
    }
}

# 测试题目数据 - 聚焦名场面和行为题
QUESTIONS = [
    {
        "id": 1,
        "scene": "机场初遇·第一次见面",
        "question": "大家第一次在机场集合，互相还不熟悉，你会怎么做？",
        "options": [
            {"text": "主动上前打招呼，热情拥抱每个人", "char": "chenyihan"},
            {"text": "站在一旁观察，等别人来跟自己说话", "char": "yangyang"},
            {"text": "简单寒暄后保持距离，不主动热络", "char": "ningjing"},
            {"text": "努力找话题，怕冷场让大家尴尬", "char": "jingboran"},
            {"text": "期待别人主动接近自己，有点小紧张", "char": "xuqing"},
            {"text": "缩在角落，担心自己说错话", "char": "zhengshuang"},
            {"text": "微笑着跟大家聊天，照顾每个人的情绪", "char": "maoamin"}
        ]
    },
    {
        "id": 2,
        "scene": "房车座位·资源争夺",
        "question": "房车上座位不够，还有人没地方坐，你会？",
        "options": [
            {"text": "直接坐到最好的位置，谁爱咋咋地", "char": "ningjing"},
            {"text": "站着不说话，心里委屈为什么没人让座给自己", "char": "xuqing"},
            {"text": "立刻站起来把自己的座位让给姐姐", "char": "jingboran"},
            {"text": "无所谓，坐地上也行，反正我能折腾", "char": "chenyihan"},
            {"text": "默默站到一边，不敢争取座位", "char": "zhengshuang"},
            {"text": "协调大家轮流坐，或者想办法加座位", "char": "maoamin"},
            {"text": "不说话，默默去后备箱整理行李腾空间", "char": "yangyang"}
        ]
    },
    {
        "id": 3,
        "scene": "尴尬九分钟·餐桌冷场",
        "question": "吃饭时突然冷场，空气凝固了整整九分钟，你会？",
        "options": [
            {"text": "低头猛吃，假装什么都没发生", "char": "yangyang"},
            {"text": "心里七上八下：是不是我说错话了？", "char": "zhengshuang"},
            {"text": "直接问：'大家为什么不说话？'", "char": "xuqing"},
            {"text": "讲个笑话或者提议玩游戏打破沉默", "char": "chenyihan"},
            {"text": "该吃吃该喝喝，完全不觉得尴尬", "char": "ningjing"},
            {"text": "给大家夹菜倒水，用行动缓解气氛", "char": "jingboran"},
            {"text": "微笑着等待，相信总会有人开口", "char": "maoamin"}
        ]
    },
    {
        "id": 4,
        "scene": "经费危机·预算不够",
        "question": "发现旅行经费严重超支，大家开始讨论省钱方案，你会？",
        "options": [
            {"text": "拿出小本本开始详细记账，计算每一笔开销", "char": "jingboran"},
            {"text": "无所谓，钱不够就去赚/借，车到山前必有路", "char": "chenyihan"},
            {"text": "直接表态：'我那份我自己解决'", "char": "ningjing"},
            {"text": "担心是因为自己花钱太多才导致超支", "char": "zhengshuang"},
            {"text": "提出':要不我们吃点好的吧，开心最重要'", "char": "xuqing"},
            {"text": "说':没事，大家商量着来，总能解决的'", "char": "maoamin"},
            {"text": "默默查攻略找最便宜的住宿和交通", "char": "yangyang"}
        ]
    },
    {
        "id": 5,
        "scene": "任务分工·谁来做",
        "question": "需要有人去做饭/打扫/跑腿，但没人主动请缨，你会？",
        "options": [
            {"text": "直接指派：'你去做这个，他去做那个'", "char": "ningjing"},
            {"text": "期待有人能安排好一切，自己跟着做就行", "char": "xuqing"},
            {"text": "二话不说起身就开始干活", "char": "yangyang"},
            {"text": "主动站出来：'我来吧，我擅长这个'", "char": "jingboran"},
            {"text": "跟着一起干，边干边聊天很开心的样子", "char": "chenyihan"},
            {"text": "想帮忙又怕做不好，犹豫不决", "char": "zhengshuang"},
            {"text": "协调分配，确保每个人都有合适的任务", "char": "maoamin"}
        ]
    },
    {
        "id": 6,
        "scene": "意见不合·发生争执",
        "question": "团队里因为某件事意见不合，吵了起来，你会？",
        "options": [
            {"text": "'吵什么吵，按我说的做，不行就散伙'", "char": "ningjing"},
            {"text": "'为什么不能开开心心地说话呢？'", "char": "xuqing"},
            {"text": "默默退出争论，自己去把事做了", "char": "yangyang"},
            {"text": "试图调解：'大家都有道理，咱们折中一下'", "char": "maoamin"},
            {"text": "躲在一边难过，觉得自己没用", "char": "zhengshuang"},
            {"text": "赶紧记下来谁说了什么，回头再算账", "char": "jingboran"},
            {"text": "打圆场：'哎呀别吵了，我们去玩吧！'", "char": "chenyihan"}
        ]
    },
    {
        "id": 7,
        "scene": "突发状况·计划改变",
        "question": "原定计划突然被取消，所有人都懵了，你会？",
        "options": [
            {"text": "马上查备选方案，迅速调整行程", "char": "yangyang"},
            {"text": "'没关系啦，正好可以去别的地方探险！'", "char": "chenyihan"},
            {"text": "'怎么会这样？那我们怎么办？'", "char": "xuqing"},
            {"text": "冷静分析现状，提出新的建议", "char": "ningjing"},
            {"text": "先安抚大家情绪：'别急，总会有办法的'", "char": "maoamin"},
            {"text": "自责是不是自己没提前确认好", "char": "zhengshuang"},
            {"text": "赶紧联系各方协调补救措施", "char": "jingboran"}
        ]
    },
    {
        "id": 8,
        "scene": "身体疲惫·极限挑战",
        "question": "连续几天睡眠不足，大家都很累，你会？",
        "options": [
            {"text": "咬牙坚持，不抱怨也不表现出来", "char": "yangyang"},
            {"text": "'我好累啊，能不能休息一下...'", "char": "xuqing"},
            {"text": "'没事没事，我还能行！大家加油！'", "char": "chenyihan"},
            {"text": "直接说':我累了，今天到此为止'", "char": "ningjing"},
            {"text": "默默给大家准备热水、找休息的地方", "char": "jingboran"},
            {"text": "担心自己拖后腿，强撑着不表现出来", "char": "zhengshuang"},
            {"text": "安排大家轮流休息，照顾好每个人", "char": "maoamin"}
        ]
    },
    {
        "id": 9,
        "scene": "被误解·遭到质疑",
        "question": "你做的事情被别人误解甚至批评，你会？",
        "options": [
            {"text": "'我不喜欢解释，懂的人自然懂'", "char": "ningjing"},
            {"text": "当场表达感受':你这样说让我很伤心'", "char": "xuqing"},
            {"text": "不说话，下次默默把事情做得更好", "char": "yangyang"},
            {"text": "心里很难过但不辩解，怕冲突升级", "char": "zhengshuang"},
            {"text": "耐心解释自己的初衷，寻求理解", "char": "jingboran"},
            {"text": "'没事啦，误会解开了就好！'", "char": "chenyihan"},
            {"text": "帮忙打圆场，化解双方的尴尬", "char": "maoamin"}
        ]
    },
    {
        "id": 10,
        "scene": "旅程结束·离别时刻",
        "question": "旅行结束了，大家即将分别，你最想说？",
        "options": [
            {"text": "'这次旅行挺有意思的，有缘再见'", "char": "ningjing"},
            {"text": "'虽然很累很痛，但这真是一段难忘的回忆'", "char": "xuqing"},
            {"text": "默默收拾行李，最后跟大家挥挥手", "char": "yangyang"},
            {"text": "'大家都好好的，我们以后还要一起玩哦！'", "char": "chenyihan"},
            {"text": "'只要你们安好，我就放心了'", "char": "maoamin"},
            {"text": "'我是不是哪里做得不够好？'", "char": "zhengshuang"},
            {"text": "'大家的联系方式都留好了，有事随时找我'", "char": "jingboran"}
        ]
    }
]

@app.route('/')
def index():
    """首页 - 展示测试介绍"""
    return render_template('index.html')

@app.route('/quiz')
def quiz():
    """测试页面"""
    return render_template('quiz.html', questions=QUESTIONS)

@app.route('/api/questions')
def get_questions():
    """API - 获取所有题目"""
    return jsonify(QUESTIONS)

@app.route('/api/calculate', methods=['POST'])
def calculate_result():
    """API - 计算测试结果"""
    data = request.json
    answers = data.get('answers', [])
    
    # 统计每个角色的得分
    scores = {char_id: 0 for char_id in CHARACTERS.keys()}
    
    for answer in answers:
        question_id = answer.get('question_id')
        selected_char = answer.get('character')
        if selected_char and selected_char in scores:
            scores[selected_char] += 1
    
    # 找出得分最高的角色
    max_score = max(scores.values())
    top_characters = [char_id for char_id, score in scores.items() if score == max_score]
    
    # 如果有多个最高分，取第一个（或者可以随机选）
    result_char_id = top_characters[0]
    result = CHARACTERS[result_char_id]
    
    # 添加详细得分信息
    result['scores'] = scores
    result['total_questions'] = len(QUESTIONS)
    
    return jsonify(result)

@app.route('/result/<char_id>')
def result(char_id):
    """结果页面"""
    if char_id not in CHARACTERS:
        return "角色不存在", 404
    
    character = CHARACTERS[char_id]
    return render_template('result.html', character=character)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
