"""
Evaluation of the model
"""


import numpy as np



def evaluate_model(model, env, num_episodes=1):
    """
    Evaluate the model to get some scores in ordrer to find out if it's worth it or it's worth putting it in the trash ;)

    Parameters
    ----------
    model : tf.keras.Sequential
      Model to evaluate
    env : PabloGameAI
      environment of the game
    num_episodes:
      Number of games

    Returns
    -------
    tuple[flmoat,list]
      average reward score and list of rewards per episode
    """
    total_rewards = 0
    list_episode_rewards = []
    for episode in range(num_episodes):

        state = env.reset()
        state = np.array(state).astype('float32')
        state = np.reshape(state, [1, 5])
        done = False
        episode_rewards = 0

        while not done:
            env.drawn_card = env.draw_card()
            if env.drawn_card == -1:
              env.pablo_called = True
              done = True
            else:
              # Make the current state
              current_state = env.state_representation()
              current_state = np.array(current_state).astype('float32')
              current_state = np.reshape(current_state, [1, 5])



              if not np.isnan(current_state).any():
                  # The AI model will predict the action with q values
                  q_values = model.predict(current_state)[0]
                  
                  # Choose the best action with q_value
                  best_action = np.argmax(q_values)+1

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


                  reward = env.reward(current_state[0],env.state_representation())


                  print(f"Action : {best_action}, Reward : {reward}")

                  episode_rewards += reward

              done = env.pablo_called



        print(f"--------------------------------------------------Total rewards for episode {episode + 1} : {episode_rewards}------------------------------------------------------------------")
        list_episode_rewards.append(episode_rewards)
        total_rewards += episode_rewards

    average_reward = total_rewards / num_episodes
    print(f"Average reward of {num_episodes} episodes : {average_reward}")

    return(average_reward,list_episode_rewards)

