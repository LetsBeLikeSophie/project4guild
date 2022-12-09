from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

byClassKor = {'전사' : ['무기', '분노', '방어'],
           '성기사': ['신성', '보호', '징벌'],
           '사냥꾼': ['야수', '사격', '생존'],
           '도적': ['암살', '무법', '잠행'],
           '사제': ['수양', '신성', '암흑',],
           '죽음의기사': ['혈기', '냉기', '부정'],
           '주술사': ['정기', '고양', '복원'],
           '마법사': ['비전', '화염', '냉기'],
           '흑마법사': ['고통', '악마', '파괴'],
           '수도사': ['양조', '풍운', '운무'],
           '드루이드': ['조화', '야성', '수호', '회복'],
           '악마사냥꾼': ['파멸', '복수'],
           '기원사': ['황폐', '보존'],
           }
# byRole = {'tank': ['전탱', '보기', '혈죽', '양조', '수드', '악탱'],
#           'healer': ['신기', '수사', '신사', '복술', '운무', '회드', '보존'],
#           'dps': ['무전', '분전', '신기', '징기', '야냥', '격냥', '생냥', '암살', '무법', '잠행', '암사', \
#                   '냉죽', '부죽', '정술', '고술', '비법', '냉법', '화법', '고흑', '악흑', '파흑', '풍운', '조드', \
#                   '야드', '악딜', '황폐']}


byRole = {'tank': ['방어', '보호', '혈기', '양조', '수호', '복수'],
          'healer': ['신기', '수양', '신사', '복원', '운무', '회복', '보존'],
          'dps': ['무기', '분노', '징벌', '야수', '사격', '생존', '암살', '무법', '잠행', \
                  '암흑', '냉죽', '부정', '정기', '고양', '비전', '화염', '냉법', '고통', '악마', '파괴', \
                  '풍운', '조화', '야성', '파멸', '황폐']}

byClass = {'warrior': {'무기': 'Arms', '분노': 'Fury', '방어': 'Protection'},
           'paladin': {'신기': 'Holy', '보호': 'Protection', '징벌': 'Retribution'},
           'hunter': {'야수': 'Beast Mastery', '사격': 'Marksmanship', '생존': 'Survival'},
           'rogue': {'암살': 'Assassination', '무법': 'Outlaw', '잠행': 'Subtlety'},
           'priest': {'수양': 'Discipline', '신사': 'Holy', '암흑': 'Shadow'},
           'death-knight': {'혈기': 'Blood', '냉죽': 'Frost', '부정': 'Unholy'},
           'shaman': {'정기': 'Elemental', '고양': 'Enhancement', '복원': 'Restoration'},
           'mage': {'비전': 'Arcane', '화염': 'Fire', '냉법': 'Frost'},
           'warlock': {'고통': 'Affliction', '악마': 'Demonology', '파괴': 'Destruction'},
           'monk': {'양조': 'Brewmaster', '풍운': 'Windwalker', '운무': 'Mistweaver'},
           'druid': {'조화': 'Balance', '야성': 'Feral', '수호': 'Guardian', '회복': 'Restoration'},
           'demon-hunter': {'파멸': 'Havoc', '복수': 'Vengeance'},
           'evoker': {'황폐': 'Devastation', '보존': 'Preservation'}}

itemTypeEngToKor = {'helm': '머리',
                    'head': '머리',
                    'neck': '목',
                    'shoulders': '어깨',
                    'cloak': '망토',
                    'chest': '가슴',
                    'bracers': '손목',
                    'wrist': '손목',
                    'gloves': '손',
                    'belt': '허리',
                    'waist': '허리',
                    'legs': '다리',
                    'boots': '발',
                    'ring': '반지',
                    'trinket': '장신구',
                    'hands': '무기(hands)',
                    'mainhand': '주무기',
                    'offhand': '보조무기(offhand)',
                    'held in off-hand': '보조무기(Held In Off-hand)',
                    'weapon':'무기(weapon)',
                    'one-hand': '한손무기',
                    'two-hand': '양손무기',
                    'ranged':'원거리무기(ranged)',
                    'shield':'방패',
                    'shoulder':'어깨',
                    'staff': '지팡이'
                    }

def getBIS(word):
    print('[ fn ] Talent.getBIS started')
    className = ''
    roleEng = ''
    speciality = ''
    print('getTalents started')

    for key, value in byClass.items():
        if word in value:
            className = key
            print(className)
    for key, value in byRole.items():
        if word in value:
            roleEng = key
            print(roleEng)
    speciality = byClass[className][word]

    findString = '[db=live]'
    res = requests.get(f'https://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/bis-gear')
    html = res.text
    result = BeautifulSoup(html, 'html.parser')
    result = result.prettify()
    result_list = result.split('\n')
    # result_list2 = result_list.split('bonus=')

    for i in result_list:
        if findString in i:
            beforeList = i.replace('bonus=',']').split(']')
    # print(beforeList)
    newList = []


    keyList = itemTypeEngToKor.keys()

    print(beforeList)
    for i in beforeList:
        if 'td' in i or 'item' in i and len(i) < 40:
            tempList = [i.replace('/', '').replace('\\', '').replace('[', '').replace('td', '').replace(' ', '')]
            print(f'>>>>>>>tempList: {tempList}')
            for j in tempList:
                if j != '' and '-' not in j and 'background' not in j:
                    newList.append(j)
    print(f'[ newList ]: {newList}')
    finalList = []
    for i in newList:
        if i.lower() in keyList:
            finalList.append(itemTypeEngToKor[i.lower()])
        elif 'item' in i:
            finalList.append(i)

    print(f'[ finalList ]: {finalList}')

    keyKorList = []
    valIdList = []
    valKorList = []

    for i in finalList:
        if 'item' not in i:
            keyKorList.append(i)
        elif 'item' in i:
            if i.startswith('item'):
                valIdList.append(i)
    print(f'[ keyKorList ]: {keyKorList}')
    print(f'[ valIdList ]: {valIdList}')

    for i in range(len(valIdList)):
        html = urlopen(f"https://www.wowhead.com/ko/{valIdList[i]}/")
        bsObject = BeautifulSoup(html, "html.parser")
        translated = bsObject.head.find("meta", {"property": "twitter:title"}).get('content')
        valKorList.append(translated)
        print(f'[ translated ]: {translated}')
    # print(f'[ valKorList ]: {valKorList}')

    bisCtx = ''

    for i in range(len(keyKorList)):
        bisCtx += f'{keyKorList[i]}: {valKorList[i]}\n'
    bisCtx += f'\nhttps://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/bis-gear'
    print(f'[ bisCtx ]: {bisCtx}')
    return bisCtx
    # keyKorList = []
    # valKorList = []
    #
    # for i in finalList:
    #     if 'item' not in i:
    #         keyKorList.append(i)
    #     elif 'item' in i:
    #         valKorList.append(i)
    # bisDic = {}
    # bisCtx = ''
    # for i in range(len(keyKorList)):
    #     bisDic[keyKorList[i]] = valKorList[i]
    # print(bisDic)
    #
    # for i in range(len(keyKorList)):
    #     bisCtx += ('%s\t %s'%(item,bisDic[item]))



    bisCtx += f'\nhttps://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/bis-gear'
    return bisCtx

    # className = ''
    # roleEng = ''
    # speciality = ''
    # result = ''
    # for key, value in byClass.items():
    #     if word in value:
    #         className = key
    #         print(className)
    # speciality = byClass[className][word]
    # html = urlopen(f"https://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/bis-gear")
    # bsObject = BeautifulSoup(html, "html.parser")
    #
    # f = open('data.txt', 'w', encoding='utf-8')
    # contents = []
    # for link in bsObject.find_all('a'):
    #     data = link.get('href')
    #     # print(data)
    #     if data is not None:
    #         contents.append(data)
    # # print(contents)
    # contentsAfter = []
    # for i in range(len(contents)):
    #     if '/item' in contents[i]:
    #         contentsAfter.append(contents[i])
    # # print(contentsAfter)
    #
    # # 하드코딩
    # itemtype = ['머리', '목', '어깨', '망토', '가슴', '손목', '장갑', '허리', '다리', '발', '반지', '반지', '장신구', '무기']
    # # temp2 는 영문명
    # num = 1
    # for i in range(len(contentsAfter)):
    #     temp = contentsAfter[i].split('/')
    #     html = urlopen(f"https://www.wowhead.com/ko/{temp[1]}/")
    #     bsObject = BeautifulSoup(html, "html.parser")
    #
    #     if i > len(itemtype) or i == len(itemtype):
    #
    #         temp1 = (f'추가{num}: ' + bsObject.head.find("meta", {"property": "twitter:title"}).get('content') + ' (' + temp[
    #             2] + ')\n')
    #         # print('추가 - ' + bsObject.head.find("meta", {"property": "twitter:title"}).get('content') + ' (' + temp[
    #         #     2] + ')')
    #         if '워크래프트' not in temp1:
    #             result += temp1
    #             num = num + 1
    #     else:
    #         temp2 = (itemtype[i] + ': ' + bsObject.head.find("meta", {"property": "twitter:title"}).get('content') + ' (' + temp[2] + ')\n')
    #         result += temp2
    #
    #         # print(itemtype[i] + ' - ' + bsObject.head.find("meta", {"property": "twitter:title"}).get('content') + ' (' +
    #         #     temp[2] + ')')
    #
    # print('[ fn ] Talent.getBIS ended')
    # return result


def getKorName(itemID):
    html = urlopen(f"https://www.wowhead.com/ko/{itemID}/")
    bsObject = BeautifulSoup(html, "html.parser")
    return bsObject.head.find("meta", {"property": "twitter:title"}).get('content')


def getTalent(word):
    className = ''
    roleEng = ''
    speciality = ''
    print('getTalents started')
    for key, value in byClass.items():
        if word in value:
            className = key
            print(className)
    for key, value in byRole.items():
        if word in value:
            roleEng = key
            print(roleEng)
    speciality = byClass[className][word]
    findString = 'copy='
    res = requests.get(
        f'https://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/talent-builds-pve-{roleEng}')
    print(f'https://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/talent-builds-pve-{roleEng}')
    html = res.text
    result = BeautifulSoup(html, 'html.parser')
    result = result.prettify()
    result_list = result.split('\n')
    beforeList = []

    for i in result_list:
        if findString in i:
            beforeList = i.split(']')
    # print(beforeList)

    afterDic = {}

    for i in range(len(beforeList)):
        if findString in beforeList[i]:
            # print(beforeList[i], beforeList[i + 1])
            pveName = beforeList[i].split('\\')
            talentCode = beforeList[i + 1].split('[')
            afterDic[pveName[1].replace('"', '') + ', ' + str(i)] = talentCode[0]
    # print(afterList)
    talentCxt = ''
    keyList = afterDic.keys()

    for item in keyList:
        talentCxt += f'목적: {item}\n{afterDic[item]}\n\n'

    print('[ fn ] Talent.getTalent ended')

    return talentCxt
