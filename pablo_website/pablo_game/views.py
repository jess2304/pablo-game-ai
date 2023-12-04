from django.shortcuts import render, redirect
from .pablo_game_ai.environment.game_env import PabloGameAI
import json


# Create your views here.



def start_game(request):
    """
    Starting the game with a representation in the html.
    """
    game = PabloGameAI(human_player = True)

    human_cards = game.human_hand
    human_cards_json = json.dumps(human_cards)  

    return(render(request, "game.html", {"human_cards_json":human_cards_json}))





def game_view(request):
    """
    Make a game view according to the request of the user.
    """
    if request.method == "POST" :
        # Actions sent by the user
        # I'll do it later ;)
        pass
    else:
        return(start_game(request))





