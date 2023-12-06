"""
Game environment named PabloGameAI
"""

import random
import numpy as np




DECK = ["ace_of_clubs","ace_of_hearts","ace_of_diamonds","ace_of_spades"] +[str(i)+"_of_clubs" for i in range(2,11)] + [str(i)+"_of_spades" for i in range(2,11)] + [str(i)+"_of_diamonds" for i in range(2,11)] + [str(i)+"_of_hearts" for i in range(2,11)]


def str_to_int(card):
  """
  Transforms the string with color to a simple int

  Returns
  -------
  int 
    The number in the card
  """

  if ('ace' in card):
    result = 1
  else:
    result = int(card.replace("_of_clubs","").replace("_of_hearts","").replace("_of_diamonds","").replace("_of_spades",""))

  return result


class PabloGameAI:
  """
  PabloGameAI is a class that describes an environment 
  in which there are two players, a human and an ai
  each player has 4 cards and will take a card in his turn
  and he will replace it by one of the other cards. 
  The winner is the one who has the minimal sum of cards.
  """

  def __init__(self, human_player = False, colours_consider = False):
    """
    Init the class with the attributes
    """
    self.deck = DECK    # cards from 1 to 10 and in 4 different colors
    random.shuffle(self.deck) # Shuffle the deck
    self.ai_hand = self.deck[:4] # 4 cards for IA
    self.deck = self.deck[4:]  # Take the 4 cards from the deck

    if human_player is True:   # If there's a human player then give him a hand
      self.human_hand = self.deck[:4] # 4 cards for IA
      self.deck = self.deck[4:]  # Take the 4 cards from the deck

    self.drawn_card = None # Not a drawn card for the moment
    self.state = self.state_representation() # Updating the state of the game
    self.pablo_called = False # We have just beguun

    print("Length of the deck : ",len(self.deck))



  def reset(self):
    """
    Reset the game

    Returns
    -------
    list
      The representation of state
    """

    self.deck = DECK    # cards from 1 to 10 and in 4 different colors
    random.shuffle(self.deck)  # Shuffle the deck
    self.ai_hand = self.deck[:4]  # 4 cards for IA
    self.deck = self.deck[4:]  # Take the 4 cards from the deck
    self.drawn_card = None # Not a drawn card for the moment
    self.state = self.state_representation()  # Updating the state of the game
    self.pablo_called = False # We have just beguun

    return self.state


  def draw_card(self):
    """
    Draw a card from the deck

    Returns
    -------
    int
      The number in the card ;)
    """
    if len(self.deck) >= 1:
        drawn_card = self.deck.pop(0)   # Pop it like it's hot ;)

        print("The drawn card is : ",drawn_card)

        return(drawn_card)
    else:
      print("The drawn card is : ",-1)
      return(-1)   # No cards in the deck :'(
  



  def choose_action(self, state, model, epsilon):
    """
    Choose an action to do according to the model and epsilon

    Parameters
    ----------
    state: list
      List of the cards in the hand of the IA
    model: Keras.tf.Keras.Sequential
      model in training or testing
    epsilon:
      Error

    Returns
    -------
    int
      The number of the action.

    """
    if np.random.rand() <= epsilon:
        return random.randint(1, 6)  # Choose random action

    state = np.array(state).astype('float32')
    state = np.reshape(state, [1, 5])
    q_values = model.predict(state)
    print("Prediction in the choose action in the class",q_values)

    return np.argmax(q_values[0])+1  # Choose best action +1 (index +1)


  def step(self,model,epsilon):
    """
    Doing the step according to the action

    * Actions : 1,2,3,4 : exchange with card number (1,2,3,4)
    * Action : 5 : call pablo
    * Action


    Returns
    -------
    Tuple[list,int,bool]
      Tuple of the state, the reward and the game if it's done or not.
    """
    done = False # Is the game finished or not
    reward = 0 # Reward of the IA to its action

    old_state = self.state_representation() # Old state of the game (hands deck etc...)


    # Draw a card first

    self.drawn_card = self.draw_card()

    if self.drawn_card == -1:
      self.pablo_called = True
      done = True
      return (-1,self.state, reward, done)
    print("change the old state")
    old_state[4] = self.drawn_card
    print("old state : ",old_state)

    print("make action")
    action = self.choose_action(old_state, model, epsilon) # Make the action according to the model
    print("action made")


    # Now we see what happens when the model chooses the action
    if action in [1, 2, 3, 4]:
      # Exchange the card with one in your hand
      card_index = action-1
      self.ai_hand[card_index] = self.drawn_card

    elif action == 5:
      # Call "Pablo"
      self.pablo_called = True
    elif action == 6:
      # Do nothing
      pass


    # Update the state of the game
    new_state = self.state_representation()
    # Reward
    reward = self.reward(old_state,new_state)
    done = self.pablo_called
    self.state = new_state

    print("Step is Done")

    return(action,new_state, reward, done)




  def state_representation(self):
    """
    Represent the current state (ai hand and drawn card)

    Returns
    -------
    list
      The state is the ai hand and the drawn card
    """

    # Represent current state


    ai_hand_int = [str_to_int(card) for card in self.ai_hand]
    if self.drawn_card is not None :
      drawn_card = [str_to_int(self.drawn_card)]
    else:
      drawn_card = [self.drawn_card]


    return(ai_hand_int + drawn_card)

  def reward(self, old_state, new_state):
    """
    Compute the reward depending on the old and new state

    Parameters
    ----------
    old_state : list
      Old state of the hand and the drawn card
    new_state : list
      New state of the hand and the drawn card

    Returns
    -------
    int
      The reward is the difference.
    """
    old_sum = sum(old_state[:4])
    new_sum = sum(new_state[:4])
    return old_sum - new_sum