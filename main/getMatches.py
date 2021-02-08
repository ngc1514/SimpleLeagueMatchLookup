import requests 
import time

riot_token = ""

if(not riot_token):
	riot_token = input("Please enter your Riot API token here, or replace variable riot_token with your token and rerun the program: \n")


summonerName = input ("Enter summoner's name: ")
url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + summonerName
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
   			"Accept-Language": "en-US,en;q=0.9",
   			"Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
   			"Origin": "https://developer.riotgames.com",
   			"X-Riot-Token": riot_token} 
r = requests.get(url = url, headers = headers) 
playerData = r.json()



def printAllUserData():
	print()
	for k,v in playerData.items():
		print("\t" + str(k) + ": " + str(v))



def printEssentialData():
	print("\nBasic info: ")
	msg = "\tname: {name} \n\taccountId: {account}"
	print(msg.format(name=playerData['name'], account=playerData['accountId']))



def getMatchListByAccoundId(endIndex):
	print("\nRecentMatch: ")
	matchApiUrl = "https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/" + playerData['accountId'] + "?endIndex=" + str(endIndex)
	matchApiHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
   			"Accept-Language": "en-US,en;q=0.9",
   			"Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
   			"Origin": "https://developer.riotgames.com",
   			"X-Riot-Token": riot_token} 
	matchReq = requests.get(url = matchApiUrl, headers = matchApiHeaders) 
	matchData = matchReq.json()

	matchesArr = matchData['matches']
	for match in matchesArr:
		curMatchId = str(match.get("gameId"))
		print("\tmatchId: " + curMatchId)
		getMatchPlayerIdentities(curMatchId, 5)



def getMatchPlayerIdentities(matchId, limitPlayerNum):
	count = 0

	print("\t\tPlayed with: ")
	getIdenUrl = "https://na1.api.riotgames.com/lol/match/v4/matches/" + str(matchId)
	getIdenHeaders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.152 Safari/537.36",
   			"Accept-Language": "en-US,en;q=0.9",
   			"Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
   			"Origin": "https://developer.riotgames.com",
   			"X-Riot-Token": riot_token} 
	getIdenReq = requests.get(url = getIdenUrl, headers = getIdenHeaders) 
	getIdenData = getIdenReq.json()

	playerIdenList = getIdenData['participantIdentities']
	for playerIden in playerIdenList:
		if(count<limitPlayerNum):
			playerInfoArr = playerIden.get("player")
			msg = "\t\t\tparticipantId: {participantId} \n\t\t\tsummonerName: {teammateName} \n\t\t\taccountId: {teammateId}\n"
			print(msg.format(participantId=str(playerIden.get("participantId")),
				teammateName=str(playerInfoArr.get("summonerName")),
				teammateId=str(playerInfoArr.get("accountId"))
				)
			)
			count += 1
		else:
			break



def main():
	if(r.status_code == 200):
		printEssentialData()
		getMatchListByAccoundId(3)



if __name__ == "__main__":
    main()

