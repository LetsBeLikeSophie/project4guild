import urllib
from time import gmtime

import discord
import requests
from discord.ext import commands

# (1) token 설정
tokenID = 
tokenPW = 

# (2) token 설정
TOKEN = 
CHANNEL_ID = 

# 단위 기간: 최근 접속 기준이 될 단위 기간
# 2629800  1개월
# 31557600 12개월
month = 2629800
lastLogin = month / 2

# URL 관련 설정
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


bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

# bot = commands.Bot(command_prefix='!', intents=discord.Intents.default())
# client = discord.Client(intents=discord.Intents.default())

# @client.event
# async def on_ready():
#
#     # send_msg.start()
#
#     print("Hi, logged in as")
#     print(client.user.name)
#     print()


def searchItems(word):
    words = word.split()
    print(f'words = {words}')
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
        print(f'https://kr.api.blizzard.com/data/wow/search/item?namespace=static-kr'
                         f'&name.en_US={firstWord}'
                         f'&orderby=id'
                         f'&_page={pageNum}'
                         f'&access_token={access_token}')
        a = r.json()

        pageSize = a['pageSize']
        print(f'총 {totalPageNum-1} 중 {pageNum} 번째 페이지')
        print(f'페이지 수 : {pageSize}')

        print(prettyWord)
        print(len(prettyWord))
        print(f'{pageNum}페이지 에 ', end='')
        for j in range(len(a['results'])):

            if a['results'][j]['data']['name']['en_US'] == word:
                foundItemList.append(a['results'][j]['data']['media']['id'])
                foundItemList.append(a['results'][j]['data']['name']['ko_KR'])
                foundItemList.append(a['results'][j]['data']['item_class']['name']['ko_KR'])
                foundItemList.append(a['results'][j]['data']['item_subclass']['name']['ko_KR'])
                foundItemList.append(a['results'][j]['data']['inventory_type']['name']['ko_KR'])
                foundItemList.append(a['results'][j]['data']['quality']['name']['ko_KR'])

                foundItemDic[a['results'][j]['data']['name']['en_US']] = foundItemList
                print(f'{word} 추가완료 : {foundItemDic}')

        if not foundItemDic:
            print('검색 결과가 없습니다.')
    return foundItemDic





@bot.event
async def on_ready():
    # send_msg.start()
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
# 입력값 듀플, 출력값 스트링
# (Edge, of, Night) 를 'Edge Of Night' 로 바꾼 후
# of 만 소문자화, 'Edge of Night' 를 반환
def wordPrettier(inputWord):

    if inputWord is not None:
        list_searchWords = inputWord.split()
        for i in range(len(list_searchWords)):
            if list_searchWords[i] == 'Of' or list_searchWords == 'OF':
                list_searchWords[i] = 'of'
                print(f'Word \'of\' is replaced to lowercase')
            elif list_searchWords[i] != 'of':
                list_searchWords[i] = list_searchWords[i].capitalize()
                print(f'\'{list_searchWords[i]}\' is capitalized')
        parameter = ' '.join(list_searchWords)
        print(f'[ parameter ] : {parameter}')
        prettyWord = parameter
        print(prettyWord)
        return parameter
    else:
        print('입력값이 없습니다.')


def qualityColour(colour):
    colours = {'하급': ':black_large_square:',
              '일반': ':white_large_square:',
              '고급': ':green_square:' ,
              '희귀': ':blue_square:',
              '영웅': ':purple_square:',
              '전설': ':orange_square:',
              '계승': ':blue_square:'
              }
    return colours[colour]

def typeIcon():
    icon = {}

def findImage(itemId):
    r = requests.get(f'https://kr.api.blizzard.com/data/wow/media/item/{itemId}?namespace=static-kr&locale=ko_KR&access_token={access_token}')
    a = r.json()
    return a['assets'][0]['value']


@bot.command()
async def 아이템검색(ctx, *searchWords):
    # await ctx.reply('{} talks to {}.'.format(arg1, arg2))
    # await ctx.reply('검색아이템: ' + searchWords)
    # list_searchWords = list(searchWords)
    inputWord = ' '.join(searchWords)
    # await ctx.send(f':small_orange_diamond:{inputWord} 를 입력 했어요.')

    # firstWord = list_searchWords[0].capitalize()
    # print(f'[ firstWord ] : {firstWord}')
    # print(f'[ list_searchWord ] : {list_searchWords}')

    # When searchWord is Eng
    if inputWord.upper() != inputWord.lower():

        prettyWord = wordPrettier(inputWord)
        # time.sleep(1)

        if inputWord != prettyWord:
            await ctx.send(f':small_orange_diamond:{prettyWord} 를 검색할게요! :wink:')
        print(f'함수 전 parameter {prettyWord}')
        found = searchItems(prettyWord)

        if found:
            # await ctx.send(found)

            embed = discord.Embed(title=f'제가 뭘 찾았는지 보세요!',
                                  description=f'{found[prettyWord][1]}!! 이걸 찾아왔어요.', color=0xF2F5A9)

            colour = qualityColour(found[prettyWord][-1])
            embed.add_field(name=f'\n> 한글명: {found[prettyWord][1]}　　　　　　　　　　{colour}{found[prettyWord][-1]}\n'
                                 f'> 영문명: {prettyWord}\n',
                            value=f'> {found[prettyWord][2]} \> {found[prettyWord][3]} \> {found[prettyWord][4]}\n'
                                  f'> ID: {found[prettyWord][0]}\n'
                                  f'> 와우헤드: https://ko.wowhead.com/item={found[prettyWord][0]}', inline=True)

            imageURL = findImage(found[prettyWord][0])

            embed.set_thumbnail(url=imageURL)

        elif not found:
            embed = discord.Embed(title=f'으앗!',
                                  description=f'딱 맞는 아이템을 찾지 못했어요.:sob:', color=0xF2F5A9)
            embed.set_thumbnail(url='https://cdn.icon-icons.com/icons2/81/PNG/256/help_question_15583.png')
            embed.add_field(name='키워드는', value='전체 단어를 입력해보세요.\n대소문자는 제가 바꿀 수 있어요.', inline=False)


    # When searchWord is Kor
    elif inputWord.upper() == inputWord.lower():

        embed = discord.Embed(title=f'와우 헤드 링크를 찾아왔어요!',
                              description=' ', color=0xF2F5A9)

        inputWord = inputWord.replace(' ', '+')
        embed.add_field(name='여기를 가보시겠어요?', value=f'https://ko.wowhead.com/items/name:{inputWord}', inline=False)
        # embed.set_image(url='https://render.worldofwarcraft.com/kr/character/azshara/225/121395169-main-raw.png')

    embed.set_footer(text='ⓒ아직누우면안돼요')
    await ctx.channel.send(embed=embed)

# 'https://kr.api.blizzard.com/profile/wow/character/azshara/%EB%A7%89%EB%82%B4%EB%8F%84%EB%A0%A8/character-media?namespace=profile-kr'
#                             '&access_token=USHX8VnPZBAOnHyW4g3DNE76GY1Sok2M1s&locale=ko_KR&region=kr'



def findImage(id):

    parsedId =''
    imageURL = {}
    # When Kor
    if id.upper() == id.lower():
        parsedId = urllib.parse.quote(id)
    # When Eng
    elif id.upper() != id.lower():
        parsedId = id.lower

    print(f'{id} is parsed to {parsedId}')

    r = requests.get(f'{profileURL}/character/azshara/{id}/character-media?namespace=profile-kr&access_token={access_token}&locale=ko_KR&region=kr')
    a = r.json()
    imageURL['small'] = a['assets'][0]['value']
    imageURL['large'] = a['assets'][3]['value']

    print(imageURL)
    return imageURL



@bot.command()
async def 형상(ctx, searchId):
    imageURLs = findImage(searchId)
    embed = discord.Embed(title=f'{searchId}님의 멋진 모습이네요!',
                          description=f'음...사실대로 말하는 게 나았으려나요?', color=0xF2F5A9)
    embed.set_thumbnail(url=imageURLs['small'])
    embed.set_image(url=imageURLs['large'])
    embed.set_footer(text='ⓒ아직누우면안돼요')
    await ctx.channel.send(embed=embed)





@bot.command()
async def 토큰(ctx):
    price, time = getPrice().split(',')
    embed = discord.Embed(title=f'토큰 가격은 {price}원 이네요.',
                          description=f'{time}에 업데이트 됐어요!', color=0xF2F5A9)
    # embed.set_thumbnail(url='https://wowtokenprices.com/assets/wowtoken-compressed.png')
    embed.set_footer(text='ⓒ아직누우면안돼요')
    await ctx.channel.send(embed=embed)



def getPrice():
    r = requests.get(
        f'https://kr.api.blizzard.com/data/wow/token/index?namespace=dynamic-kr&locale=ko_KR&access_token=KReJ663wQTrCwyponOJ6aIyjezRd2GNVFt')
    a = r.json()

    updatedTime = a['last_updated_timestamp']
    price = int(a['price'] / 10000)
    digit = str(price / 10000)
    a, b = digit.split('.')
    # print(f'{price} to {a}만 {b}원')
    tigm = gmtime(updatedTime / 1000)
    # print(f'{tigm.tm_year}년 {tigm.tm_mon}월 {tigm.tm_mday}일 {tigm.tm_hour}시 {tigm.tm_min}분 {tigm.tm_sec}초')

    return f'{a}만 {b}원,{tigm.tm_year}년 {tigm.tm_mon}월 {tigm.tm_mday}일 {tigm.tm_hour}시 {tigm.tm_min}분'


bot.run(TOKEN)



