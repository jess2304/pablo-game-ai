"""
In this file we define a function that trains an agent with DQN
"""





import numpy as np
import random
from collections import deque
import json





def train_dqn(env, model, n_episodes=100, save_path="models/model_pablo.h5", metrics_path="metrics/metrics.json"):
    """
    Make the training of the DQN model

    Parameters
    ----------

    env : PabloGameAI
      environment of the game : instance of class
    model: tf.keras.Sequential
      model to train
    n_episodes : int
      number of episodes (games)
    save_path : str
      the path to save the model
    metrics_path : str
      path to save the metrics

   
    """

    # Initialize replay memory with a max length of 2000
    replay_memory = deque(maxlen=2000)

    # Parameters
    batch_size = 32
    gamma = 0.95
    epsilon = 1.0
    epsilon_decay = 0.995
    epsilon_min = 0.01

    # List to store total rewards for each episode
    total_rewards = []


    # Begin the episodes
    for episode in range(n_episodes):
        print(f"------------    Begin  Game number: {episode}  --------------------")
        # Reset the environment and reshape the state
        state = env.reset()
        state = np.array(state).astype('float32').reshape((1, 5))
        done = False
        total_reward = 0

        # Loop of a whole episode (game)
        while not done:
            # Take a step in the environment
            action,next_state, reward, done = env.step(model,epsilon)

            # Log the details of the action taken
            print(f"Episode {episode}: Action {action} |  State {state} | Next State {next_state} | Reward {reward}")

            if not done :

              if not (np.isnan(state).any() or np.isnan(next_state).any()):
                state = np.array(state).astype('float32').reshape((1, 5)) 
                next_state = np.array(next_state).astype('float32').reshape((1, 5))
                
                # Add the experience to the replay memory
                replay_memory.append((state, action, reward, next_state, done))
                
                # Update the model if replay memory has enough samples
                if len(replay_memory) > batch_size:
                    # Sample minibatch from replay memory
                    minibatch = random.sample(replay_memory, batch_size)
                    
                    # Loop every experience in the minibatch
                    for s, a, r, next_s, d in minibatch:
                          target = r + (gamma * np.amax(model.predict(next_s)[0]) * (not d))
                          target_f = model.predict(s)
                          target_f[0][a-1] = target
                          model.fit(s, target_f, epochs=1, verbose=0)

              # Update the state and the total reward
              state = next_state
              total_reward += reward

              # Decay epsilon
              epsilon = max(epsilon_min, epsilon * epsilon_decay)
            
        # Append the total reward
        total_rewards.append(total_reward)

        # Progress every 5 episodes
        if episode % 5 == 0:
            print(f"---------------------------------------------------      Episode: {episode}, Total Reward: {total_reward}            ---------------------------------------------------------------")

    # Save the model
    model.save(save_path)

    # Save metrics
    with open(metrics_path, "w") as f:
        json.dump(total_rewards, f)

