from ast import List
from urllib import response
from click import get_binary_stream
from requests import get

BASE_URL = "http://data.nba.net"
ALL_JSON = "/prod/v1/today.json"

# Acessa Json da página
def get_links():
    response = get(BASE_URL+ALL_JSON).json()
    return response["links"]

# Cria função para pegar placar em tempo real 
def get_currentScoreboard():
    response = get(BASE_URL+get_links()["currentScoreboard"]).json()
    games = response["games"]
    
    for game in games:
        home_team = game["hTeam"]
        away_team = game["vTeam"]
        clock = game["clock"]
        period = game["period"]
        arena = game['arena']['name']
        city = game['arena']['city']
        
        # Exibe resultados: adicionei nome do ginásio e cidade do jogo
        print("##############################################\n")
        print(f"{arena} -  {city}")
        print(f"{home_team['triCode']} vs {away_team['triCode']}")
        print(f"SCORE: {home_team['score']} vs {away_team['score']}")
        print(f"{clock} -  {period['current']}\n" )        
        
# Lista ranking de times por pontos por jogo (ppg)       
def get_teams_stats():
    stats = get_links()["leagueTeamStatsLeaders"]
    data = get(BASE_URL+stats).json()
    teams = data["league"]["standard"]["regularSeason"]["teams"]

    teams = list(filter(lambda x: x["name"] != "Team", teams))
    teams.sort(key = lambda x: int(x["ppg"]["rank"]))

    for team in teams:
        team_name = team["name"]
        nickname = team["nickname"]
        ppg_avg = team["ppg"]["avg"]
        rank = team["ppg"]["rank"]
        print(f"RANK: {rank} | {team_name} - {nickname} | PPG Médio: {ppg_avg}")

# Função lista todos os times da temporada (incluindo as equipes do ALL-STAR game)
def teams():
    response = get(BASE_URL+get_links()["teams"]).json()
    team = response['league']['standard']
    
    list = team
    
    for teams in team:
        team_name = teams['nickname']
        print(team_name)

# Lista os jogadores da Liga, posição (abreviada: 'G': guard , 'F': forward e 'C': center)
def get_leagueRosterPlayers():
  players = get_links()["leagueRosterPlayers"]
  data = get(BASE_URL+players).json()
  player = data['league']['standard']

  lista = (player)
  #print(lista)

  for players in player:
    first_name  = players['firstName']
    second_name = players['lastName']
    name_complete = (f"{first_name} {second_name}")
    jersey = players['jersey']
    position = players["pos"]

    print(f"{name_complete}  | {position} | {jersey}")
    
# Lista todos os técnicos da liga
def get_leagueRosterCoaches():
    coaches = get_links()["leagueRosterCoaches"]
    data = get(BASE_URL+coaches).json()
    coach = data['league']['standard']
    
    for coaches in coach:        
            first_name = coaches['firstName']
            second_name = coaches['lastName']
            name_complete = (f"{first_name} {second_name}")
            team = coaches['teamSitesOnly']['teamCode']
            assist_coach = coaches['isAssistant'] 
            
            if assist_coach is False:                             
                print(f"{name_complete} | {team}")    
                     
                       
     
        
while True:
    print("########################\n")
    print("SEJA BEM VINDO!!!! DADOS NBA \n")
    print("1 - Ver Jogos\n")
    print("2 - Ver Times por PPG\n")
    print("3 - Listar Jogadores da Liga\n")
    print("4 - Listar todos os times da liga\n")
    print("5 - Listar todos os técnicos da liga\n")
    user_choice = input("Opção: ")

    if user_choice == "1":
        get_currentScoreboard()
    elif user_choice == "2":
        get_teams_stats()
    elif user_choice == "3":
        get_leagueRosterPlayers()
    elif user_choice == "4":
        teams()
    elif user_choice == "5":
        get_leagueRosterCoaches()
    else:
        continue
