import requests
from urllib import parse



def getCharacterInfo(characterName, access_token):

    print(f'[ characterName ]: {characterName}')

    r = requests.get(f'https://kr.api.blizzard.com/profile/wow/character/{serverName}/{characterName}'
                     f'?namespace=profile-kr'
                     f'&access_token={access_token}'
                     f'&locale=ko_KR&region=kr')
    characterContent = r.json()

    characterInfo = characterContent['race']['name'] + ','

    if 'active_spec' in characterContent:
        characterInfo += characterContent['active_spec']['name'] + ','
    else:
        characterInfo = ''

    characterInfo += characterContent['character_class']['name'] + ',' \
                     + str(characterContent['equipped_item_level'])
    print(f'[ characterInfo ]: {characterInfo}')

    return characterInfo

def getMythicInfo(characterName):

    print(f'[ characterName ]: {characterName}')

    r = requests.get(f'https://raider.io/api/v1/characters/profile?region=kr'
                     f'&realm={serverName}'
                     f'&name={characterName}'
                     f'&fields=mythic_plus_weekly_highest_level_runs')

    contents = r.json()

    result = []


    if len(contents['mythic_plus_weekly_highest_level_runs']) != 0:
        for i in range(len(contents['mythic_plus_weekly_highest_level_runs'])):
            result.append([contents['mythic_plus_weekly_highest_level_runs'][i]['dungeon'],
                           contents['mythic_plus_weekly_highest_level_runs'][i]['mythic_level'],
                           contents['mythic_plus_weekly_highest_level_runs'][i]['num_keystone_upgrades']])
    else:
        print('[ 데이터 없음 ]')

    print(result)