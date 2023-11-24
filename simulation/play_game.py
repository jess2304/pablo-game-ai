"""
Play a game against AI model imported
"""


from env.game_env import PabloGameAI
import numpy as np


def play_game(loaded_model):
    """
    Play the game against the loaded AI model

    Parameters
    ----------
    loaded_model : keras.Sequential()
        loaded trained model 
    """

    # Initialiser le jeu
    env = PabloGameAI(human_player=True)
    done = False

    while not done:

        print("\n\n--------------------------------------------------------------------\n\n")
        # Give the actual hands
        print(f"Hand of human : {env.human_hand}    |    Hand of AI : {env.ai_hand}")
        print("\n")
        # The turn of the human to take a card and decide
        drawn_card = env.draw_card()
        action = int(input("Choose your action (1-5): "))
        print("\n")
        # Apply the action on the current state of the game
        if action in [1, 2, 3, 4]:
            # Exchange the card with one in your hand
            card_index = action-1
            env.human_hand[card_index] = drawn_card

        elif action == 5:
            # Call "Pablo"
            env.pablo_called = True
        elif action == 6:
            # Do nothing
            pass

        done = env.pablo_called

        # The turn of the AI
        if not done:
            # AI takes a card
            print(f"Hand of human : {env.human_hand}    |    Hand of AI : {env.ai_hand}")
            env.drawn_card = env.draw_card()

            # Make the current state
            current_state = env.state_representation()
            current_state = np.array(current_state).astype('float32')
            current_state = np.reshape(current_state, [1, 5])

            # The AI model will predict the action with q values
            q_values = loaded_model.predict(current_state)

            # Choose the best action with q_value
            best_action = np.argmax(q_values[0])+1

            # Apply the action
            if best_action in [1, 2, 3, 4]:
                # Exchange the card with one in your hand
                card_index = best_action-1
                env.ai_hand[card_index] = env.drawn_card

            elif best_action == 5:
                # Call "Pablo"
                env.pablo_called = True
            elif best_action == 6:
                # Do nothing
                pass

            done = env.pablo_called

            # PRint action of AI
            print(f"AI has chosen {best_action}")

        # Check if the game is finished
        if done:
            print("Game finished !\n")
            print(f"Human hand : {env.human_hand} and AI hand : {env.ai_hand}")
