import asyncio
import urllib
from time import gmtime

import Talents
import discord
import requests
from discord.ext import commands

# (1) token 설정
tokenID =
tokenPW =

# (2) token 설정
TOKEN =
# CHANNEL_ID = 

# 단위 기간: 최근 접속 기준이 될 단위 기간
# 2629800  1개월
# 31557600 12개월
month = 2629800
lastLogin = month / 2

# URL 관련 설정
guildServer =
guildSlug =
dataURL = 'https://kr.api.blizzard.com/data/wow'
profileURL = 'https://kr.api.blizzard.com/profile/wow'
tokenPlusLocale = ""

# 최대 조회 인원: 한 번에 몇 명까지 조회 할지
endIndex = 10
# Kdaccow or %EC%8B%9C%EC%B2%B
memberNamesEncoded = []
memberDic = {}

# token 요청
r = requests.post("https://" + tokenID + ":" + tokenPW + "@us.battle.net/oauth/token?grant_type=client_credentials")
token = r.json()
access_token = token['access_token']
print("[ token info ]", end=' ')
print(token)
print("[ access_token ]", end=' ')
print(access_token)

# 하드코딩 직업 예외 부분

doubleNamed = {'신성': '\'성기사\' 인가요? \'사제\' 인가요?',
               '냉기': '\'마법사\' 인가요? \'죽음의기사(죽기)\' 인가요?'}
doubleNamedClass = ['성기사', '사제', '마법사', '죽음의 기사', '죽기', '법사']

# 하드코딩
classNameDic = {'hunter': '사냥꾼',
                'warlock': '흑마법사',
                'druid': '드루이드',
                'mage': '마법사',
                'death-knight': '죽음의기사',
                'demon-hunter': '악마사냥꾼',
                'evoker': '기원사',
                'monk': '수도사',
                'priest': '사제',
                'paladin': '성기사',
                'rogue': '도적',
                'shaman': '주술사',
                'warrior': '전사'}

classNameEng = {'Warrior': [{'name': '전사'}, {'Arms': '무기', 'Fury': '분노', 'Protection': '방어'}],
                'Paladin': [{'name': '성기사'}, {'Holy': '신성', 'Protection': '보호', 'Retribution': '징벌'}],
                'Hunter': [{'name': '사냥꾼'}, {'Beast Mastery': '야수', 'Marksmanship': '사격', 'Survival': '생존'}],
                'Rogue': [{'name': '도적'}, {'Assassination': '암살', 'Outlaw': '무법', 'Subtlety': '잠행'}],
                'Priest': [{'name': '사제'}, {'Discipline': '수양', 'Holy': '신성', 'Shadow': '암흑'}],
                'Death Knight': [{'name': '죽음의기사'}, {'Blood': '혈기', 'Frost': '냉기', 'Unholy': '부정'}],
                'Shaman': [{'name': '주술사'}, {'Elemental': '정기', 'Enhancement': '고양', 'Restoration': '복원'}],
                'Mage': [{'name': '마법사'}, {'Arcane': '비전', 'Fire': '화염', 'Frost': '냉기'}],
                'Warlock': [{'name': '흑마법사'}, {'Affliction': '고통', 'Demonology': '악마', 'Destruction': '파괴'}],
                'Monk': [{'name': '수도사'}, {'Brewmaster': '양조', 'Windwalker': '풍운', 'Mistweaver': '운무'}],
                'Druid': [{'name': '드루이드'}, {'Balance': '조화', 'Feral': '야성', 'Guardian': '수호', 'Restoration': '회복'}],
                'Demon Hunter': [{'name': '악마사냥꾼'}, {'Havoc': '파멸', 'Vengeance': '복수'}],
                'Evoker': [{'name': '기원사'}, {'Devastation': '황폐', 'Preservation': '보존'}]}

botStatusMSG = '뭐라도 '


def searchItems(word):
    words = word.split()
    print(f'[words]: {words}')
    firstWord = words[0]

    r = requests.get(f'https://kr.api.blizzard.com/data/wow/search/item?namespace=static-kr'
                     f'&name.en_US={firstWord}'
                     f'&orderby=id'
                     f'&access_token={access_token}')
    a = r.json()
    foundItemDic = {}
    foundItemList = []
    totalPageNum = a['pageCount'] + 1
    pageNum = a['page']

    for pageNum in range(1, totalPageNum):
        r = requests.get(f'https://kr.api.blizzard.com/data/wow/search/item?namespace=static-kr'
                         f'&name.en_US={firstWord}'
                         f'&orderby=id'
                         f'&_page={pageNum}'
                         f'&access_token={access_token}')
        # print(f'https://kr.api.blizzard.com/data/wow/search/item?namespace=static-kr'
        #       f'&name.en_US={firstWord}'
        #       f'&orderby=id'
        #       f'&_page={pageNum}'
        #       f'&access_token={access_token}')
        a = r.json()

        pageSize = a['pageSize']
        # print(f'총 {totalPageNum - 1} 중 {pageNum}번째 페이지')
        # print(f'페이지 수 : {pageSize}')
        #
        # print(prettyWord)
        # print(len(prettyWord))
        print(f'[{pageNum}페이지]: ', end='')
        for j in range(len(a['results'])):

            if a['results'][j]['data']['name']['en_US'] == word:
                foundItemList.append(a['results'][j]['data']['media']['id'])
                foundItemList.append(a['results'][j]['data']['name']['ko_KR'])
                foundItemList.append(a['results'][j]['data']['item_class']['name']['ko_KR'])
                foundItemList.append(a['results'][j]['data']['item_subclass']['name']['ko_KR'])
                foundItemList.append(a['results'][j]['data']['inventory_type']['name']['ko_KR'])
                foundItemList.append(a['results'][j]['data']['quality']['name']['ko_KR'])

                foundItemDic[a['results'][j]['data']['name']['en_US']] = foundItemList
                print(f'{word} 추가 완료 : {foundItemDic}')

        if not foundItemDic:
            print('검색 결과 없음')
    return foundItemDic


@bot.event
async def on_ready():
    # send_msg.start()
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(botStatusMSG))
    print("Hi, logged in as")
    print(bot.user.name)
    print()


@bot.command(aliases=['길드카톡'])
async def Hello(ctx):
    await ctx.send('https://open.kakao.com/o/gTle5JL')


# @tasks.loop(minutes = 5)
# async def send_msg():
#     channel = client.get_channel(CHANNEL_ID)
#     await channel.send('Hello')


prettyWord = ''


# 입력값 튜플, 출력값 스트링
# (Edge, of, Night) 를 'Edge Of Night' 로 바꾼 후
# of 만 소문자화, 'Edge of Night' 를 반환
def wordPrettier(inputWord):
    if inputWord is not None:
        list_searchWords = inputWord.split()
        for i in range(len(list_searchWords)):
            if list_searchWords[i] == 'Of' or list_searchWords == 'OF':
                list_searchWords[i] = 'of'
                # print(f'Word \'of\' is replaced to lowercase')
            elif list_searchWords[i] != 'of':
                list_searchWords[i] = list_searchWords[i].capitalize()
                # print(f'\'{list_searchWords[i]}\' is capitalized')
        parameter = ' '.join(list_searchWords)
        prettyWord = parameter
        print(f'[prettyWord] : {prettyWord}')
        return parameter
    else:
        print('입력값이 없습니다.')


def qualityColour(colour):
    colours = {'하급': ':black_large_square:',
               '일반': ':white_large_square:',
               '고급': ':green_square:',
               '희귀': ':blue_square:',
               '영웅': ':purple_square:',
               '전설': ':orange_square:',
               '계승': ':blue_square:'
               }
    return colours[colour]


def typeIcon():
    icon = {}


def findItemImage(itemId):
    r = requests.get(
        f'https://kr.api.blizzard.com/data/wow/media/item/{itemId}?namespace=static-kr&locale=ko_KR&access_token={access_token}')
    a = r.json()
    return a['assets'][0]['value']


def findImage(id):
    parsedId = ''
    imageURL = {}
    # When Kor
    if id.upper() == id.lower():
        parsedId = urllib.parse.quote(id)
    # When Eng
    elif id.upper() != id.lower():
        parsedId = id.lower

    print(f'[parsedId]: {id} >>> {parsedId}')

    r = requests.get(
        f'{profileURL}/character/{guildServer}/{id}/character-media?namespace=profile-kr&access_token={access_token}&locale=ko_KR&region=kr')
    a = r.json()
    print(
        f'{profileURL}/character/{guildServer}/{id}/character-media?namespace=profile-kr&access_token={access_token}&locale=ko_KR&region=kr')
    if 'assets' in a:
        imageURL['small'] = a['assets'][0]['value']
        imageURL['large'] = a['assets'][3]['value']
        print(f'[imageURL]: {imageURL}')
    else:
        print('[에러 ', end='')
        print(a['code'], end=']: ')
        print(a['detail'])

    return imageURL


@bot.event
async def on_message(message):
    channel = message.channel
    topic = message.channel.topic
    if topic is not None and '#수비대장봇' in topic:
        # [명령어]
        if message.content.startswith('!명령어'):
            print(f'\n[명령어]: !명령어')
            print(f'[author.nick]: {message.author.nick}(name: {message.author.name})')

            embed = discord.Embed(title=f'제가 할 수 있는 것들이에요:star:',
                                  description='\n', color=0xF2F5A9)
            embed.add_field(name='**  **', value='**  **', inline=False)
            embed.add_field(name='\n> !명령어', value='가능한 명령어를 보여줘요.\n예) !명령어', inline=False)
            embed.add_field(name='**  **', value='**  **', inline=False)
            embed.add_field(name='\n> !토큰', value='가장 최신 업데이트 된 토큰 가격을 보여줘요.\n예) !토큰', inline=False)
            embed.add_field(name='**  **', value='**  **', inline=False)
            embed.add_field(name='\n> !형상 (!형변)',
                            value='캐릭터의 모습을 보여줘요.\n예) !형상\n**       **!형상 잠꾸러긔\n**       **!형변\n**       **!형변 장난꾸러긔',
                            inline=False)
            embed.add_field(name='**  **', value='**  **', inline=False)
            embed.add_field(name='\n> !검색 (!아이템)',
                            value='영문명 아이템을 찾아줘요.\n한글명 아이템은 와우헤드 링크로 보내요.:sweat_smile: \n예) !검색 밤의 끝\n**       **!검색 edge of night\n**       **!아이템 밤의 끝\n**       **!아이템 edge of night',
                            inline=False)
            embed.add_field(name='**  **', value='**  **', inline=False)

            # embed.set_thumbnail(url='https://cdn.icon-icons.com/icons2/2959/PNG/512/coins_coin_money_cash_icon_185964.png')
            embed.set_footer(text=f'ⓒ{bot.user.name}')
            await channel.send(embed=embed)

        # [특성/비스]
        if message.content.startswith('!특성') or message.content.startswith('!비스'):
            messageByWord = message.content.split(' ')
            resultDic = {}
            resultList = []
            print(message)
            print(f'[author.nick]: {message.author.nick}(name: {message.author.name})')
            if messageByWord[1] in doubleNamed:
                timeout = 5
                send_message = await channel.send(doubleNamed[messageByWord[1]])

                def check(m):
                    return m.author == message.author and m.channel == message.channel

                try:
                    msg = await bot.wait_for('message', check=check, timeout=timeout)
                except asyncio.TimeoutError:
                    await channel.send(f'마냥 기다릴 수 없어요. 저도 바쁘다고욧!:snowman2: \n준비가 되면 다시 찾아주세요:wink:')
                else:
                    className = msg.content
                    word = ''
                    if '법' in className:
                        word = '냉법'
                    elif '죽' in className:
                        word = "냉죽"
                    elif '사제' in className:
                        word = "신사"
                    elif '기사' in className:
                        word = "신기"
                    else:
                        await channel.send('잘못 입력했어요.')

                    if messageByWord[0] == '!특성':
                        # message.author.dm_channel
                        await channel.send(f'{word}에 대한 특성이에요.\n\n{Talents.getTalent(word)}')
                    elif messageByWord[0] == '!비스':
                        # for key, value in Talents.byClass.items():
                        #     if word in value:
                        #         className = key
                        await channel.send('1분 정도 기다려 주세요. 끝나면 알려드릴께요. (추가 명령 금지:face_with_peeking_eye:)')
                        await channel.send(f'{word}에 대한 BIS에요.\n\n{Talents.getBIS(word)}')
                        await channel.send(f':ballot_box_with_check:{message.author.mention}님! 완료되었습니다!')

                    # await channel.send(f'{msg.content}메시지를 {timeout}초 안에 입력하셨습니다!')
            else:
                if messageByWord[0] == '!특성':
                    for key, value in Talents.byClass.items():
                        if messageByWord[1] in value:
                            className = key
                    await channel.send(
                        f'{messageByWord[1]} {classNameDic[className]}에 대한 특성이에요.\n\n{Talents.getTalent(messageByWord[1])}')
                #     message.author.dm_channel.send
                elif messageByWord[0] == '!비스':
                    for key, value in Talents.byClass.items():
                        if messageByWord[1] in value:
                            className = key
                    await channel.send('1분 정도 기다려 주세요. 끝나면 알려드릴께요. (추가 명령 금지:face_with_peeking_eye:)')
                    await channel.send(
                        f'{messageByWord[1]} {classNameDic[className]}에 대한 BIS에요.\n{Talents.getBIS(messageByWord[1])}')
                    await channel.send(f'{message.author.mention}님! :ballot_box_with_check:완료되었습니다!')

        # [토큰]
        if message.content.startswith('!토큰'):
            print(f'\n[명령어]: !토큰')
            print(f'[author.nick]: {message.author.nick}(name: {message.author.name})')

            price, time = getPrice().split(',')
            embed = discord.Embed(title=f'토큰 가격은 {price} 이에요.',
                                  description=f'{time}에 업데이트 됐어요!', color=0xF2F5A9)
            embed.set_thumbnail(
                url='https://cdn.icon-icons.com/icons2/2959/PNG/512/coins_coin_money_cash_icon_185964.png')
            embed.set_footer(text=f'ⓒ{bot.user.name}')
            await channel.send(embed=embed)

        # [형상/형변]
        if message.content.startswith('!형상') or message.content.startswith('!형변'):
            messageByWord = message.content.split(' ')

            # 로그
            print(f'\n[명령어]: {messageByWord[0]}')
            print(f'[author.nick]: {message.author.nick}(name: {message.author.name})', end='')

            if len(messageByWord) > 1:
                searchId = messageByWord[1]
            elif len(messageByWord) == 1:
                if message.author.nick is None:
                    await channel.send(
                        f'서버 닉네임을 :video_game:게임 닉네임으로 설정해 주세요. \n'
                        f':arrow_right: {message.author.mention} 우클릭 해 변경할 수 있어요.\n'
                        f'또는 {messageByWord[0]} \'아이디\' 형태로 검색할 수 있어요.:wink:')
                elif message.author.nick is not None:
                    searchId = message.author.nick

                # 로그
                print(f', [searchId]: {searchId}')

            imageURLs = findImage(searchId)
            if imageURLs:
                embed = discord.Embed(title=f'{searchId}님의 멋진 모습이네요!',
                                      description=f'음...사실대로 말하는 게 나았으려나요?', color=0xF2F5A9)
                embed.set_thumbnail(url=imageURLs['small'])
                embed.set_image(url=imageURLs['large'])
                embed.set_footer(text=f'ⓒ{bot.user.name}')
                await channel.send(embed=embed)

            elif not imageURLs:
                await channel.send('음..그 사람의 데이터를 찾을 수 없었어요!:rolling_eyes:\n다시 해보실래요?')

        # [검색/아이템]
        if message.content.startswith('!검색') or message.content.startswith('!아이템'):
            messageByWord = message.content.split(' ')

            # 로그
            print(f'\n[명령어]: {messageByWord[0]}')
            print(f'[author.nick]: {message.author.nick}(name: {message.author.name})')

            if len(messageByWord) > 1:
                inputWord = ' '.join(messageByWord[1:])

                # When searchWord is Eng
                if inputWord.upper() != inputWord.lower():
                    prettyWord = wordPrettier(inputWord)
                    if inputWord != prettyWord:
                        await channel.send(f'{prettyWord}를 검색할게요! :wink:')

                    found = searchItems(prettyWord)
                    if found:
                        embed = discord.Embed(title=f'제가 뭘 찾았는지 보세요!',
                                              description=f'{found[prettyWord][1]}!! 이걸 찾아왔어요.', color=0xF2F5A9)

                        colour = qualityColour(found[prettyWord][-1])
                        embed.add_field(
                            name=f'\n> 한글명: {found[prettyWord][1]}　　　　　　　　　　{colour}{found[prettyWord][-1]}\n'
                                 f'> 영문명: {prettyWord}\n',
                            value=f'> {found[prettyWord][2]} \> {found[prettyWord][3]} \> {found[prettyWord][4]}\n'
                                  f'> ID: {found[prettyWord][0]}\n'
                                  f'> 와우 헤드: https://ko.wowhead.com/item={found[prettyWord][0]}', inline=True)

                        imageURL = findItemImage(found[prettyWord][0])
                        embed.set_thumbnail(url=imageURL)
                        print(f'[결과]: {inputWord} 검색, {found[prettyWord][1]} 찾음')

                    elif not found:
                        embed = discord.Embed(title=f'으앗!',
                                              description=f'딱 맞는 아이템을 찾지 못했어요.:sob:', color=0xF2F5A9)
                        embed.set_thumbnail(url='https://cdn.icon-icons.com/icons2/81/PNG/256/help_question_15583.png')
                        embed.add_field(name='키워드는',
                                        value=':heavy_check_mark:전체 단어를 입력해보세요.\n:heavy_check_mark:대소문자는 제가 바꿀 수 있어요.',
                                        inline=False)
                        print(f'[결과]: {inputWord} 검색 found 실패')

                # When searchWord is Kor
                elif inputWord.upper() == inputWord.lower():

                    embed = discord.Embed(title=f'와우 헤드 링크를 찾아왔어요!',
                                          description=' ', color=0xF2F5A9)

                    inputWord = inputWord.replace(' ', '+')
                    embed.add_field(name='여기를 가보시겠어요?', value=f'https://ko.wowhead.com/items/name:{inputWord}',
                                    inline=False)
                    embed.set_thumbnail(url='https://cdn.icon-icons.com/icons2/212/PNG/256/Link256_25043.png')
                    print(f'[결과]: {inputWord} 검색')

                embed.set_footer(text=f'ⓒ{bot.user.name}')
                await channel.send(embed=embed)

            elif len(messageByWord) == 1:
                await channel.send('찾을 아이템을 알려주세요!')
                # time.sleep(1)
                await channel.send(
                    ':heavy_check_mark:영어면 한글로 찾아줄 수 있어요.\n:heavy_check_mark:한글은 와우 헤드 검색만 가능해요.:stuck_out_tongue:')
                print(f'[결과]: 입력값 없음')


def getPrice():
    r = requests.get(
        f'https://kr.api.blizzard.com/data/wow/token/index?namespace=dynamic-kr&locale=ko_KR&access_token={access_token}')
    a = r.json()

    updatedTime = a['last_updated_timestamp']
    price = int(a['price'] / 10000)
    digit = str(price / 10000)
    a, b = digit.split('.')
    # print(f'{price} to {a}만 {b}원')
    tigm = gmtime(updatedTime / 1000)
    # print(f'{tigm.tm_year}년 {tigm.tm_mon}월 {tigm.tm_mday}일 {tigm.tm_hour}시 {tigm.tm_min}분 {tigm.tm_sec}초')

    return f'{a}만 {b}원,{tigm.tm_year}년 {tigm.tm_mon}월 {tigm.tm_mday}일 {tigm.tm_hour}시'
    # f'{tigm.tm_min}분'


# @형상.error
# @토큰.error
# async def 에러(ctx, error):
#
#     print(f'{ctx} >>> {error}')
#
#     await ctx.send("명령어를 확인해주세요!")
#


# @bot.event
# async def on_typing(channel, user, when):
#     print(f'[{channel}] {when}, {user}')


bot.run(TOKEN)

# https://www.wowhead.com/guide/classes/death-knight/blood/cheat-sheet
