import numpy as np
import random


# Global controls
ACTION_NAMES = ["left", "up", "right", "down"]
ACTION_LEFT = 0
ACTION_UP = 1
ACTION_RIGHT = 2
ACTION_DOWN = 3


def state2tensor(state):
    t = np.zeros((16, 16), dtype=np.float32)
    for i, c in enumerate(state.flatten()):
        t[c, i] = 1  # 2.0**c
    t.resize(1, 16, 4, 4)
    return t


class Game:
    def __init__(self, state=None, initial_score=0):
        """Init the Game object.
        Args:
        state: Shape (4, 4) numpy array to initialize the state with. If None,
        the state will be initialized with two random tiles (as done
        in the original game).
        initial_score: Score to initialize the Game with.
        """
        self._score = initial_score

        if state is None:
            # Initialize all states to 0(empty)
            self._state = np.zeros((4, 4), dtype=int)

            # Initialize 2 random tiles
            self.add_random_tile()
            self.add_random_tile()
        else:
            self._state = state.copy()

    def copy(self):
        """Return a copy of self."""
        return Game(np.copy(self._state), self._score)

    def game_over(self):
        """Whether the game is over. Check if any of the
           actions are still available"""
        for action in range(4):
            if self.is_action_available(action):
                return False
        return True

    def available_actions(self):
        """Computes the set of actions that are available."""
        return [action for action in range(4) if
                self.is_action_available(action)]

    def is_action_available(self, action):
        """Determines whether action is available.
        That is, executing it would change the state.
        """
        # Rotate the state by 90 anti clockwise times the action
        # This reduces the number of cases to be checked
        temp_state = np.rot90(self._state, action)
        return self._is_action_available_left(temp_state)

    def _is_action_available_left(self, state):
        """Determines whether action 'Left' is available."""

    # True if any field is 0 (empty) on the left of a tile or two tiles can
    # be merged.
        for row in range(4):
            has_empty = False
            for col in range(4):
                has_empty |= state[row, col] == 0
                if state[row, col] != 0 and has_empty:
                    return True
                if (state[row, col] != 0 and col > 0 and
                   state[row, col] == state[row, col - 1]):
                    return True

        return False

    def do_action(self, action):
        """Execute action, add a new tile, update the
           score & return the reward."""

        if action in self.available_actions():

            temp_state = np.rot90(self._state, action)
            reward = self._do_action_left(temp_state)
            self._state = np.rot90(temp_state, -action)
            self._score += reward

            self.add_random_tile()

            return self._state.copy(), reward, self.game_over(), ''

        else:
            return self._state.copy(), -8, self.game_over(), ''

    def _do_action_left(self, state):
        """Exectures action 'Left'."""

        reward = 0

        for row in range(4):
            # Always the rightmost tile in the current
            # row that was already moved
            merge_candidate = -1
            merged = np.zeros((4,), dtype=bool)

            for col in range(4):
                if state[row, col] == 0:
                    continue

                if (merge_candidate != -1 and
                    not merged[merge_candidate] and
                   state[row, merge_candidate] == state[row, col]):
                    # Merge tile with merge_candidate
                    state[row, col] = 0
                    merged[merge_candidate] = True
                    state[row, merge_candidate] += 1
                    reward += 2 ** state[row, merge_candidate]

                else:
                    # Move tile to the left
                    merge_candidate += 1
                    if col != merge_candidate:
                        state[row, merge_candidate] = state[row, col]
                        state[row, col] = 0

        return reward

    def add_random_tile(self):
        """Adds a random tile to the grid. Assumes that it has empty fields."""

        x_pos, y_pos = np.where(self._state == 0)
        assert len(x_pos) != 0
        empty_index = np.random.choice(len(x_pos))
        value = np.random.choice([1, 2], p=[0.9, 0.1])

        self._state[x_pos[empty_index], y_pos[empty_index]] = value

    def print_state(self):
        """Prints the current state."""

        def tile_string(value):
            """Concert value to string."""
            if value > 0:
                return '% 5d' % (2 ** value,)
            return "     "

        print("-" * 25)
        for row in range(4):
            print("|" + "|".join([tile_string(v)
                  for v in self._state[row, :]]) + "|")
            print("-" * 25)

    def state(self):
        """Return current state."""
        return self._state.copy()

    def score(self):
        """Return current score."""
        return self._score.copy()

    def to_tensor(self):
        return state2tensor(self._state)


class RandomPlayer():
    """
    A player which will take random move
    on 100 simulations: average score 1093, max score 2736
    """

    def __init__(self, name='Random Player'):
        self.name_ = name

    def select_action(self, state):
        return np.random.randint(4)


class OneStepPlayer():
    """
    A player which will search one step forward.
    on 100 simulations: average score 1811, max score 6192
    """

    def __init__(self, name='One Step Player'):
        self.name_ = name

    def select_action(self, state):
        rewards = [Game(state=state).do_action(i)[1] for i in range(4)]
        if np.max(rewards) > 0:
            return np.argmax(rewards)
        else:
            return np.random.randint(4)


class MultiStepPlayer():
    """
    A player which will search steps depth.
    on 100 simulations:
        2 steps depth: average score 7648, max score 16132
        3 steps depth: average score 8609, max score 16248
    """

    def __init__(self, name='Mutil Step Player', steps=2):
        self.name_ = name
        self.n_steps_ = steps

    def select_action(self, state):
        rewards = np.zeros(4, dtype=np.int32)
        for i in range(4):
            env = Game(state=state)
            new_state, rewards[i], _, _ = env.do_action(i)
            for _ in range(self.n_steps_ - 1):
                new_state, reward, _, _ = env.do_action(
                    OneStepPlayer().select_action(new_state))
                rewards[i] += reward
        if np.max(rewards) > 0:
            return np.argmax(rewards)
        else:
            return np.random.randint(4)


def play_once(env, player):
    "Play one episode using the player"
    epoch = 1
    while 1:
        a = player.select_action(env.state())
        _, r, t, _ = env.do_action(a)
        if t:
            break
        epoch += 1
    ret = env.score()
    return ret


def test_player(player, n_episodes):
    "Test player plays for given number of episodes"
    sum_ret = 0
    max_ret = 0
    for episode in range(n_episodes):
        env = Game()
        ret = play_once(env, player)
        sum_ret += ret
        if ret > max_ret:
            max_ret = ret
    print('%s average score %d, max score %d' %
          (player.name_, sum_ret / n_episodes, max_ret))


def __test__():
    "Test function to test the code"
    s = np.array(
        [[0, 0, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 0]],
        dtype=np.int8)
    env = Game(state=s)
    print(env)
    env.step(1)
    print(env)