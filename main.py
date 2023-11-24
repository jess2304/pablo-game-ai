"""
We will run our code in this main that is the only file needed to be executed.
We will choose either we play the game of train the model and save it. 
"""






import argparse
from env.game_env import PabloGameAI
from ai.model import make_model, load_model
from ai.training import train_dqn
from plots.plots import represent_from_json, represent_from_list
from ai.evaluation import evaluate_model
from simulation.play_game import play_game


def main():
    """
    main function to run when executing the program.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=["train", "evaluate", "play"], help="Mode to run the script in.")
    parser.add_argument("-m", "--model", help="Path to the AI model file (for evaluate and play modes).", default="models/model_pablo.h5")

    args = parser.parse_args()

    if args.mode == "train":
        # Create environment
        env = PabloGameAI()
        model = make_model(size=5, optimizer = 'adam', loss = 'mse')
        # Train the model
        train_dqn(env, model, n_episodes=100, save_path="models/model_pablo.h5", metrics_path="metrics/metrics.json")

        represent_from_json("metrics/metrics.json","Total rewards per episode","episode","total rewards")



    elif args.mode in ["evaluate", "play"]:
        # Load the model
        model = load_model(args.model)
        

        if model is not None:

            if args.mode == "evaluate":
                env = PabloGameAI()
                average_reward, list_rewards = evaluate_model(model,env,50)
                represent_from_list(list_rewards)
                print(f"The average reward is {average_reward}.")
                pass

            elif args.mode == "play":
                play_game(model)
        else:
            print("The game wasn't played or evaluated because there was no model.")



# Running the main.


if __name__ == "__main__":
    main()