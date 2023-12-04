from django.shortcuts import render, redirect
from .pablo_game_ai.environment.game_env import PabloGameAI

# Create your views here.



def start_game(request):
    game = PabloGameAI(human_player = True)

    request.session["game_state"] = game.state_representation()

    return(render(request, "game.html", {"game_state":game.state_representation()}))






