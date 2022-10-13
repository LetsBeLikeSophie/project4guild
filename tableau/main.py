import urllib
from time import gmtime
from time import time
from urllib import parse
import numpy
import requests

# token 설정
tokenID = 
tokenPW = 

# URL 관련 설정
guildSlug = 
dataURL = 'https://kr.api.blizzard.com/data/wow'
profileURL = 'https://kr.api.blizzard.com/profile/wow'
tokenPlusLocale = ""

# 단위 기간: 최근 접속 기준이 될 단위 기간
# 2629800  1개월
# 31557600 12개월
month = 2629800
lastLogin = month / 2

# 최대 조회 인원: 한 번에 몇 명까지 조회 할지
endIndex = 10
# Kdaccow or %EC%8B%9C%EC%B2%B
memberNamesEncoded = []

# 딕셔너리 설정
affixDic = {}
dungeonDic = {}
levelDic = {}

print('\n')
print("[ gmtime ]", end=' ')
print(gmtime(time()))

# token 요청
r = requests.post("https://" + tokenID + ":" + tokenPW + "@us.battle.net/oauth/token?grant_type=client_credentials")
token = r.json()
access_token = token['access_token']
print("[ token info ]", end=' ')
print(token)
print("[ access_token ]", end=' ')
print(access_token)

# 쿼리스트링 이 후 토큰이랑 로캘
tokenPlus = "&access_token=" + access_token + "&region=kr"
tokenPlusLocale = "&access_token=" + access_token + "&locale=ko_KR&region=kr"
print("[ access_token ]", end=' ')
print(tokenPlusLocale)


# 총 길드원 체크 함수
def checkMemberNum():
    r = requests.get(
        dataURL + "/guild/azshara/" + guildSlug + "/roster?"
        + "namespace=profile-kr"
        + tokenPlusLocale)
    memberInfo = r.json()
    print("총 길드원 수: " + str(len(memberInfo['members'])))
    return len(memberInfo['members'])


# 최종 접속 기준으로 길드원 출력
# 총 조회할 길드원 수 입력 필요
def saveMemberListAll():
    r = requests.get(
        dataURL + "/guild/azshara/" + guildSlug + "/roster?"
        + "namespace=profile-kr"
        + tokenPlusLocale)
    memberInfo = r.json()
    print(memberInfo.keys())
    print(len(memberInfo['members']))
    file = open('전체 길드원 목록.txt', 'w')

    for i in range(len(memberInfo["members"])):
        print(memberInfo['members'][i]['character']['name'])
        text = memberInfo['members'][i]['character']['name'] + '\n'
        file.writelines(text)
    file.close()


# 최근 6개월 멤버 정보 출력 > 텍스트 파일 저장 후
# url 멤버 이름 인코딩 하여 반환
def getMemberListEncoded():
    print("\n>>> 길드원 목록 출력 함수 시작")

    r = requests.get(
        dataURL + "/guild/azshara/" + guildSlug + "/roster?"
        + "namespace=profile-kr"
        + tokenPlusLocale)
    print("[ 대상 URL ] " +
          dataURL + "/guild/azshara/" + guildSlug + "/roster?"
          + "namespace=profile-kr"
          + tokenPlusLocale)

    memberInfo = r.json()

    fileName = '길드원 기본 정보.txt'
    file = open(fileName, 'w')
    firstLine = "아이디, 접속일자, 시간, 전문화, 직업, 성별, 종족, 아이템레벨" + '\n'
    file.writelines(firstLine)

    for i in range(0, endIndex):
        characterInfo = memberInfo['members'][i]['character']

        r = requests.get(
            characterInfo['key']['href'] + "&id=" + str(characterInfo['id'])
            + tokenPlusLocale)
        singleCharacterInfo = r.json()

        if 'last_login_timestamp' in singleCharacterInfo:
            ti = singleCharacterInfo['last_login_timestamp'] / 1000
            tigm = gmtime(singleCharacterInfo['last_login_timestamp'] / 1000)
            if time() - ti < lastLogin:
                tempName = urllib.parse.quote(singleCharacterInfo['name'])
                print(singleCharacterInfo['name'])
                if '%' in tempName:
                    memberNamesEncoded.append(tempName)
                else:
                    memberNamesEncoded.append(tempName.lower())

                if 'active_spec' in singleCharacterInfo:
                    activeSpec = singleCharacterInfo['active_spec']['name']
                else:
                    activeSpec = ''

                text = [singleCharacterInfo['name'] + ",",
                        (str(tigm.tm_year) + "-" + str(tigm.tm_mon) + "-" + str(tigm.tm_mday) + "," + str(
                            tigm.tm_hour) + "시") + ",",
                        activeSpec + ",",
                        singleCharacterInfo['character_class']['name'] + ",",
                        singleCharacterInfo['gender']['name'] + ",",
                        singleCharacterInfo['race']['name'] + ",",
                        str(singleCharacterInfo['equipped_item_level']) + '\n']
                file.writelines(text)
    print("[ 저장 완료 ] " + fileName)
    print(">>> 길드원 목록 출력 함수 끝\n")
    file.close()


#  확장팩 및 던전 정보 출력 함수 - 미사용
def getDungeoninfo(memberlist):
    print(">>> getDungeoninfo STARTS here")
    for i in range(len(memberlist)):
        r = requests.get(
            profileURL + "/character/azshara/"
            + memberlist[i] + "/encounters/dungeons?namespace=profile-kr"
            + tokenPlusLocale)
        print(
            profileURL + "/character/azshara/"
            + memberlist[i] + "/encounters/dungeons?namespace=profile-kr"
            + tokenPlusLocale)
        memDungeoninfo = r.json()
        memDungeonNum = len(memDungeoninfo['expansions'])
        print("[ Expansion List ]", end=" ")
        print(len(memDungeoninfo['expansions']), end=" ")
        print("from " + memberlist[i] + ", ")
        for j in range(memDungeonNum):
            print((memDungeoninfo['expansions'][j]['expansion']['name']))


# 쐐기 던전 정보 출력 및 텍스트 파일 저장 함수 - 미사용
def saveBestDungeonInfo(memberlistEncoded):
    file = open('길드원별 베스트런 정보.txt', 'w')

    text = ""
    for ii in range(len(memberlistEncoded)):
        r = requests.get(profileURL + "/character/azshara/"
                         + memberlistEncoded[ii]
                         + "/mythic-keystone-profile/season/8?namespace=profile-kr"
                         + tokenPlusLocale)
        a = r.json()

        if 'best_runs' in a:

            print("\n[ Best runs per character ]")
            print(a['best_runs'][0])
            print(a['best_runs'][0].keys())
            print("\n[ Starts from here ]")

            for i in range(len(a['best_runs'])):

                print("[" + str(i + 1) + "]")
                print("[아이디]", end=" ")
                print(parse.unquote(memberlistEncoded[ii]))
                print("[단수]", end=" ")
                print(a['best_runs'][i]['dungeon']['name'], end=", ")
                print(str(a['best_runs'][i]['keystone_level']) + "단")

                print("[시클여부]", end=" ")
                print(a['best_runs'][i]['is_completed_within_time'])
                print("[시간]", end=" ")
                print(a['best_runs'][i]['duration'])
                print("[Rating]", end=" ")
                print(a['best_runs'][i]['mythic_rating']['rating'])
                print("[어픽스]", end=" ")

                info = parse.unquote(memberlistEncoded[ii]) + ", " \
                       + str(a['best_runs'][i]['dungeon']['name']) + ", " \
                       + str(a['best_runs'][i]['keystone_level']) + ", " \
                       + str(a['best_runs'][i]['is_completed_within_time']) + ", " \
                       + str(a['best_runs'][i]['duration']) + ", " \
                       + str(a['best_runs'][i]['mythic_rating"]["rating']) + ", "

                # 어픽스 출력
                # eg. 폭군, 고취, 전율, 장막,
                affix = ""
                for j in range(len(a['best_runs'][i]['keystone_affixes'])):
                    print(a['best_runs'][i]['keystone_affixes'][j]['name'], end="* ")
                    affix = affix + a['best_runs'][i]['keystone_affixes'][j]['name'] + ';'
                    print(affix)

                print("\n[멤버]", end=" ")

                # 멤버 출력
                # eg. 막내도련, 파멸
                partyinfo = ""
                for j in range(len(a['best_runs'][i]['members'])):
                    partyinfo = partyinfo + a['best_runs'][i]['members'][j]['specialization']['name'] + " " + \
                                a['best_runs'][i]['members'][j]['character']['name'] + ';'
                print(partyinfo)

                print("\n")
                text = info + affix + ", " + partyinfo + "\n"
                file.writelines(text)
                print(text)

    file.close()


# 어픽스 딕셔너리 키(영문명) : 밸류(한글명)
def affixDic():
    print(">>> 어픽스 딕셔너리 함수 시작")

    r = requests.get(dataURL + "/keystone-affix/index?namespace=static-kr" + tokenPlus)
    a = r.json()
    fromENtoKR = {}

    for i in range(len(a['affixes'])):
        fromENtoKR[str(a['affixes'][i]['name']['en_US'])] = a['affixes'][i]['name']['ko_KR']
    print("[ affixDic ]", end=" ")
    print(fromENtoKR)
    print(">>> 어픽스 딕셔너리 함수 끝")
    return fromENtoKR


# 던전 딕셔너리 키(영문명) : 밸류(한글명)
def dungeonDic():
    print(">>> 던전 딕셔너리 함수 시작")

    r = requests.get(dataURL + "/mythic-keystone/dungeon/index?namespace=dynamic-kr" + tokenPlus)
    a = r.json()
    fromENtoKR = {}
    for i in range(len(a['dungeons'])):
        fromENtoKR[str(a['dungeons'][i]['name']['en_US'])] = a['dungeons'][i]['name']['ko_KR']
    # 매칭 안되는 키 값 하드 코딩
    fromENtoKR['Mechagon Junkyard'] = '작전명: 메카곤 - 고철장'
    fromENtoKR['Mechagon Workshop'] = '작전명: 메카곤 - 작업장'

    print("[ dungeonDic ]", end=" ")
    print(fromENtoKR)
    print(">>> 던전 딕셔너리 함수 끝")
    return fromENtoKR


# 쐐기 정보 (레이더) 불러와서 텍스트 파일로 저장하는 함수
def saveDungeonInfos():
    file = open('길드원별 쐐기 정보 (레이더).txt', 'w')
    firstLine = "아이디, 던전명, 단수, 완료시간, 소요시간, 쐐기돌업글, 점수, 어픽스, 단수(중앙값)" + '\n'
    file.writelines(firstLine)

    for i in range(len(memberNamesEncoded)):
        r = requests.get("https://raider.io/api/v1/characters/profile?region=kr&realm=azshara&name="
                         + memberNamesEncoded[i]
                         + "&fields=mythic_plus_best_runs")
        a = r.json()

        dungeonInfo = ""

        if 'mythic_plus_best_runs' in a:
            for j in range(len(a['mythic_plus_best_runs'])):
                affix = ''
                for k in range(len(a['mythic_plus_best_runs'][j]['affixes'])):
                    affix = affix + affixDic[str(a['mythic_plus_best_runs'][j]['affixes'][k]['name'])] + ';'

                name = (parse.unquote(memberNamesEncoded[i])).capitalize()

                dungeonInfo = name + ', ' \
                              + str(dungeonDic[str(a['mythic_plus_best_runs'][j]['dungeon'])]) + ', ' \
                              + str(a['mythic_plus_best_runs'][j]['mythic_level']) + ', ' \
                              + str(a['mythic_plus_best_runs'][j]['completed_at']) + ', ' \
                              + str(a['mythic_plus_best_runs'][j]['clear_time_ms']) + ', ' \
                              + str(a['mythic_plus_best_runs'][j]['num_keystone_upgrades']) + ', ' \
                              + str(a['mythic_plus_best_runs'][j]['score']) + ', ' \
                              + affix + ', ' \
                              + str(levelDic[name]) \
                              + '\n'
                file.writelines(dungeonInfo)
                print(dungeonInfo)
    file.close()


def getNameAndMedi():
    print(">>> { 길드원 : 중앙값 } 함수 시작")
    for i in range(len(memberNamesEncoded)):
        r = requests.get('https://raider.io/api/v1/characters/profile?region=kr&realm=azshara&name='
                         + memberNamesEncoded[i]
                         + '&fields=mythic_plus_best_runs')
        a = r.json()
        levelList = []
        levelListAfter = []
        medi = None

        if 'mythic_plus_best_runs' in a:
            for j in range(len(a['mythic_plus_best_runs'])):
                # 시클한 경우만 단수 저장
                if a['mythic_plus_best_runs'][j]['num_keystone_upgrades'] > 0:
                    levelList.append(a['mythic_plus_best_runs'][j]['mythic_level'])
                print('leveList>>> ', end='')
                print(levelList)

        # 하위 단수들 자르기
        if len(levelList) > 0:
            minNum = int(round(max(levelList) * 0.3))
            print('min(삭제기준단수)>>> ' + str(minNum))

            for ii in range(len(levelList)):
                if levelList[ii] > minNum:
                    levelListAfter.append(levelList[ii])

        print('leveListAfter(삭제후)>>> ', end='')
        print(levelListAfter)

        if len(levelListAfter) > 0:
            medi = int(round(numpy.median(levelListAfter)))
            print('medi(중앙값)>>> ' + str(medi))

        # 키(아이디 인코딩) : 밸류(메디안)
        name = (parse.unquote(memberNamesEncoded[i])).capitalize()
        print(name)
        levelDic[name] = medi

    print(levelDic)


# 파일에서 아이디 읽어와 레이더 API 받아오기
def readFile():
    print('>>> readFile 함수 시작')
    f = open("길드원 기본 정보.txt", 'r')
    lines = f.readlines()
    tempName = []
    for line in lines:
        tempList = line.split(',', maxsplit=1)
        tempName.append(tempList[0])
    f.close()

    print('[ 파일로 불러들인 길드원 수 ] ' + str(len(tempName)) + ' (-1)')
    print(tempName)
    print('\n>>> 인코딩 시작')

    for i in range(len(tempName)):
        # 첫번째 컬럼명 삭제 ('아이디')
        if i != 0:
            encodedName = urllib.parse.quote(tempName[i])
            if '%' in tempName[i]:
                memberNamesEncoded.append(encodedName)
            else:
                memberNamesEncoded.append(encodedName.lower())
    print('[ 저장 완료 (memberNamesEncoded) ]')
    print(memberNamesEncoded)
    print('>>> readFile 함수 끝')


# -----------------------------------------------------------------------------------------------
# 본문
# -----------------------------------------------------------------------------------------------

# print(checkMemberNum())

endIndex = checkMemberNum()
print("\n>>> 메인 시작")
print("[ 총 길드원 수 ] " + str(endIndex))

getMemberListEncoded()
print(">>> 전역 변수 확인")
print("[ memberNamesEncoded ]", end=" ")
print(memberNamesEncoded)
print('\n>>> 딕셔너리 설정')
affixDic = affixDic()
dungeonDic = dungeonDic()
print("\n")
getNameAndMedi()
saveDungeonInfos()

# readFile()

# 포옹 횟수 38회
# https://kr.api.blizzard.com/profile/wow/character/azshara/%EB%A7%89%EB%82%B4%EB%8F%84%EB%A0%A8/achievements/statistics?namespace=profile-kr&access_token=US8RzJuG4i5yRM1dkhCgDn6XifaaTiJlTt&locale=ko_KR&region=kr
# 사진경로
# https://kr.api.blizzard.com/profile/wow/character/azshara/%EB%A7%89%EB%82%B4%EB%8F%84%EB%A0%A8/character-media?namespace=profile-kr&access_token=US8RzJuG4i5yRM1dkhCgDn6XifaaTiJlTt&locale=ko_KR&region=kr
