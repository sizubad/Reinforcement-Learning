import numpy as np
import random


class Agent():
    "All of the Agent expect Q-learning has been given to you."
    """Inspired: https://github.com/brianspiering/rl-course/blob/master/labs/\
                 lab_4_tic_tac_toe/lab_4_tic_tac_toe.ipynb"""
    def __init__(self, game_class, epsilon=0.2, alpha=.5):
        "Initialize the agent"
        self.V = dict()  # Values of different states as we encounter them
        self.NewGame = game_class
        self.epsilon = epsilon
        self.alpha = alpha

    def state_value(self, game_state, action):
        "Look up state value. If never seen state, then assume neutral."
        return self.V.get((str(game_state), action), 0.0)

    def learn_game(self, n_episodes=1_000):
        "Let's learn through complete experience to get that reward."
        for episode in range(n_episodes):
            self.learn_from_episode()

    def learn_from_episode(self):
        "Update Values based on reward."
        game = self.NewGame()
        while not game.game_over():
            action, reward = self.learn_from_move(game)
        self.V[(str(game._state), action)] = reward

    def learn_from_move(self, game):
        "The heart of Q-learning."

        current_state = game._state
        selected_next_move = self.learn_select_move(game)
        r = game.do_action(selected_next_move)  # Get reward for choosen action
        current_state_value = self.state_value(current_state,
                                               selected_next_move)

        try:
            best_next_move = self.select_best_move(game)
            best_move_value = self.state_value(game._state, best_next_move)
            td_target = r + best_move_value
            self.V[(str(current_state),
                    selected_next_move)] = r + self.alpha*best_move_value
        except:
            pass
        return selected_next_move, r

    def learn_select_move(self, game):
        "Exploration and exploitation"
        best_state_action = self.select_best_move(game)  # Exploitation
        selected_state_action = best_state_action
        if random.random() < self.epsilon:
            allowed_state_action_values = self.state_values(game._state,
                                                            game.available_actions())
            selected_state_action = self.random_V(allowed_state_action_values)[1]
        return selected_state_action

    def select_best_move(self, game):
        "Selects best move for given state(Greedy)"
        allowed_state_action_values = self.state_values(game._state,
                                                        game.available_actions())
        best_state_action = self.argmax_V(allowed_state_action_values)
        return best_state_action[1]

    def round_V(self):
        "After training, this makes action selection random from equally-good choices"
        for k in self.V.keys():
            self.V[k] = round(self.V[k], 1)

    def state_values(self, game_state, actions):
        "Return Q value for given state-action pair"
        return dict(((str(game_state), action),
                    self.state_value(game_state, action))
                    for action in actions)

    def argmax_V(self, state_values):
        "For the best possible states, chose randomly amongst them."
        try:
            max_V = max(state_values.values())
        except:
            max_V = 0
        chosen_state_action = random.choice([state_action for state_action, v in state_values.items() if v == max_V])
        return chosen_state_action

    def random_V(self, state_values):
        "Any state will do."
        return random.choice(list(state_values.keys()))

    def random_play(self):
        "Agent plays with random policy"
        game = self.NewGame()
        while not game.game_over():
            self.random_move(game)
        return game.score()

    def random_move(self, game):
        "Agent chooses avialble actions randomly"
        available = game.available_actions()
        game.do_action(np.random.choice(available))

    def q_learning_play(self):
        "Agent plays with q_learning"
        game = self.NewGame()
        while not game.game_over():
            best = self.select_best_move(game)
            if best in game.available_actions():
                game.do_action(best)
            else:
                game.do_action(np.random.choice(game.available_actions()))
        return game.score()