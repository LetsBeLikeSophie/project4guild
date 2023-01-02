from urllib.request import urlopen

import bot_Util
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

itemTypeEngToKor = {'helm': ':small_blue_diamond:머리',
                    'head': ':small_blue_diamond:머리',
                    'neck': ':small_blue_diamond:목',
                    'shoulders': ':small_blue_diamond:어깨',
                    'cloak': ':small_blue_diamond:망토',
                    'chest': ':small_blue_diamond:가슴',
                    'bracers': ':small_blue_diamond:손목',
                    'wrist': ':small_blue_diamond:손목',
                    'gloves': ':small_blue_diamond:손',
                    'belt': ':small_blue_diamond:허리',
                    'waist': ':small_blue_diamond:허리',
                    'legs': ':small_blue_diamond:다리',
                    'boots': ':small_blue_diamond:발',
                    'ring': ':ring:반지',
                    'ring1': ':ring:반지',
                    'ring2': ':ring:반지',
                    'trinket': ':small_orange_diamond:장신구',
                    'trinket1': ':small_orange_diamond:장신구',
                    'trinket2': ':small_orange_diamond:장신구',
                    'hands': ':axe:무기(hands)',
                    'mainhand': ':dagger:주무기',
                    'offhand': ':crutch:보조무기(offhand)',
                    'held in off-hand': ':crutch:보조무기(Held In Off-hand)',
                    'weapon': ':dagger:무기(weapon)',
                    'one-hand': ':dagger:한손무기',
                    'two-hand': ':crossed_swords:양손무기',
                    'ranged': ':bow_and_arrow:원거리무기(ranged)',
                    'shield': ':shield:방패',
                    'shoulder': ':small_blue_diamond:어깨',
                    'staff': ':magic_wand:지팡이',
                    '1hweapon': ':dagger:무기(1HWeapon)',
                    '2hweapon': ':dagger:무기(2HWeapon)'
                    }



def getLink(word):
    # word = '무기'
    print('[ fn ] Talent.getLink started')
    className = ''
    roleEng = ''
    speciality = ''

    for key, value in byClass.items():
        if word in value:
            className = key
            print(f'[ className ]: \'{className}\' grabbed from \'{word}\'')
    for key, value in byRole.items():
        if word in value:
            roleEng = key
            print(f'[ roleEng ]: {roleEng}')
    speciality = byClass[className][word]

    return f'https://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/bis-gear'



def getBIS(word):
    # word = '무기'
    print('[ fn ] Talent.getBIS started')
    className = ''
    roleEng = ''
    speciality = ''

    for key, value in byClass.items():
        if word in value:
            className = key
            print(f'[ className ]: \'{className}\' grabbed from \'{word}\'')
    for key, value in byRole.items():
        if word in value:
            roleEng = key
            print(f'[ roleEng ]: {roleEng}')
    speciality = byClass[className][word]

    findString = ']Neck['
    res = requests.get(f'https://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/bis-gear')
    html = res.text
    result = BeautifulSoup(html, 'html.parser')
    result = result.prettify()
    result_list = result.split('\n')

    title = []
    for i in result_list:
        if 'Raid' in i:
            title.append(i)
        elif 'Mythic+' in i:
            title.append(i)
    print(f'>>>>>>>>>>>>>>>>>title {title}')

    titleList = []

    for i in title:
        if '[h3 toc=' in i:
            print(i)
            titleList = i.replace('[h3 toc=', '][').replace('/h3]', '][').split('][')

    print(f'>>>>>>>>>>>>>>>>>title {titleList}')
    title = []

    for i in titleList:
        if 'Best in Slot Gear for' in i:
            title2 = i.replace(']', '[').split('[')
            print(type(title2))
            for j in range(len(title2)):
                if 'Best in Slot' in title2[j]:
                    title.append(title2[j])
    print(f'[ title ]: {title}')
    #
    beforeList = []
    newList = []
    finalList = []

    for i in result_list:
        if findString in i:
            beforeList = i.replace('bonus=', '][').replace('(', '][').split('][')

    # print(beforeList)
    #
    keyList = itemTypeEngToKor.keys()
    #
    # # print(beforeList)
    for i in beforeList:
        if 'td' in i or 'item' in i and len(i) < 40:
            tempList = [
                i.replace('/', '').replace('\\', '').replace('[', '').replace(']', '').replace('td', '').replace(' ',
                                                                                                                 '')]
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

    finalCtx = ''
    titleIndex = 0

    for i in range(len(finalList)):
        if '머리' in finalList[i] and titleIndex < len(title):
            finalCtx += '\n**[ ' + title[titleIndex] + '] **\n' + finalList[i] + ': '
            print(f'[ title[titleIndex] ]: {title[titleIndex]}')
            print(f'[ finalList[i] added ]: {finalList[i]}')
            titleIndex += 1

        else:
            valList = itemTypeEngToKor.values()
            if finalList[i] in valList:
                finalCtx += finalList[i] + ': '
                print(f'[ finalList[i] added ]: {finalList[i]}')

            elif finalList[i].startswith('item'):
                if finalList[i - 1] in valList:
                    html = urlopen(f"https://www.wowhead.com/ko/{finalList[i]}/")
                    bsObject = BeautifulSoup(html, "html.parser")
                    translated = bsObject.head.find("meta", {"property": "twitter:title"}).get('content')
                    finalCtx += translated + '\n'
                    print(f'[ translated added ]: {translated}')

    return finalCtx



def getKorName(itemID):
    html = urlopen(f"https://www.wowhead.com/ko/{itemID}/")
    bsObject = BeautifulSoup(html, "html.parser")
    return bsObject.head.find("meta", {"property": "twitter:title"}).get('content')


def getTalent(word):
    className = ''
    roleEng = ''
    speciality = ''
    print('[ fn ] Talents.getTalents started')
    for key, value in byClass.items():
        if word in value:
            className = key
            print(f'[ className ]: \'{className}\' grabbed from \'{word}\'')
    for key, value in byRole.items():
        if word in value:
            roleEng = key
            print(f'[ roleEng ]: {roleEng}')
    speciality = byClass[className][word]
    findString = 'copy='
    res = requests.get(
        f'https://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/talent-builds-pve-{roleEng}')
    print(
        f'[ url ]: https://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/talent-builds-pve-{roleEng}')
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
            # print('i')
            # print(beforeList[i-4])
            # print('i+1')
            # print(beforeList[i + 1])
            # print(f'beforeList[i-4] >>> {beforeList[i-4]}, {beforeList[i-5]} ')
            pveName = beforeList[i - 4].split('[')
            # print('pveName')
            # print(f'[ pveName ]: {pveName}')

            if 'Mythic+' in pveName[0]:
                pveName[0] += ' :small_blue_diamond:쐐기'
            elif 'Raid' in pveName[0]:
                pveName[0] += ' :small_orange_diamond:레이드'

            pveName[0]
            talentCode = beforeList[i + 1].split('[')
            # afterDic[pveName[1].replace('"', '') + ', ' + str(i)] = talentCode[0]

            afterDic[pveName[0]] = talentCode[0]
    print(f'[ afterDic ]: {afterDic}')

    # print(afterList)
    talentCxt = ''
    keyList = afterDic.keys()

    for item in keyList:
        talentCxt += f':arrow_forward:{item}\n{afterDic[item]}\n\n'

    talentCxt += f'https://www.wowhead.com/guide/classes/{className.lower()}/{speciality.lower()}/talent-builds-pve-{roleEng}'

    print('[ fn ] Talent.getTalent ended')

    return talentCxt
