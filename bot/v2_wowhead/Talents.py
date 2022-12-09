from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests

byClassKor = {'전사': ['무기', '분노', '방어'],
              '성기사': ['신성', '보호', '징벌'],
              '사냥꾼': ['야수', '사격', '생존'],
              '도적': ['암살', '무법', '잠행'],
              '사제': ['수양', '신성', '암흑', ],
              '죽음의기사': ['혈기', '냉기', '부정'],
              '주술사': ['정기', '고양', '복원'],
              '마법사': ['비전', '화염', '냉기'],
              '흑마법사': ['고통', '악마', '파괴'],
              '수도사': ['양조', '풍운', '운무'],
              '드루이드': ['조화', '야성', '수호', '회복'],
              '악마사냥꾼': ['파멸', '복수'],
              '기원사': ['황폐', '보존'],
              }

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
                    'weapon': '무기(weapon)',
                    'one-hand': '한손무기',
                    'two-hand': '양손무기',
                    'ranged': '원거리무기(ranged)',
                    'shield': '방패',
                    'shoulder': '어깨',
                    'staff': '지팡이'
                    }


def getBIS(word):
    print('[ fn ] Talent.getBIS started')
    className = ''
    roleEng = ''
    speciality = ''
    newList = []
    finalList = []
    keyKorList = []
    valIdList = []
    valKorList = []

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
            beforeList = i.replace('bonus=', ']').split(']')
    print(beforeList)
    
    keyList = itemTypeEngToKor.keys()

    for i in beforeList:
        if 'td' in i or 'item' in i and len(i) < 40:
            tempList = [i.replace('/', '').replace('\\', '').replace('[', '').replace('td', '').replace(' ', '')]
            print(f'>>>>>>>tempList: {tempList}')
            for j in tempList:
                if j != '' and '-' not in j and 'background' not in j:
                    newList.append(j)
    print(f'[ newList ]: {newList}')

    for i in newList:
        if i.lower() in keyList:
            finalList.append(itemTypeEngToKor[i.lower()])
        elif 'item' in i:
            finalList.append(i)

    print(f'[ finalList ]: {finalList}')

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
