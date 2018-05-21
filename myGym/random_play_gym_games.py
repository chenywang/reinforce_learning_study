import gym
import time


def random_play(game_name):
    env = gym.make(game_name)
    observation = env.reset()
    print "init observation", observation
    print env.action_space
    print "space", env.observation_space
    # print "high", env.observation_space.high
    # print "low", env.observation_space.low
    for _ in range(1000):
        env.render()
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)  # take a random action
        if done:
            env.reset()
            print "game over", _
        print "action", action, type(action)
        print "observation", observation, type(observation)
        print "reward", reward, type(reward)
        print "done", done, type(done)
        print "info", info, type(info)
        print "====================="


if __name__ == "__main__":
    # random_play('CartPole-v0')
    # random_play('MountainCar-v0')
    # random_play('MsPacman-v0')
    random_play('FrozenLake-v0')
