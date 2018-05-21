from time import sleep

import gym
def maual_play(game_name):
    env = gym.make(game_name)
    print type(env)
    observation = env.reset()
    print "init observation", observation
    print "action_space", env.action_space
    print "observation_space", env.observation_space
    print "high", env.observation_space.high
    print "low", env.observation_space.low
    for _ in range(1000):
        env.render()
        sleep(5)
        action = env.action_space.sample()
        observation, reward, done, info = env.step(1) # take a random action
        # if done:
        #     print "game over", _
        #     env.reset()
            # break
        print "action", action, type(action)
        print "observation", observation, type(observation)
        print "reward", reward, type(reward)
        print "done", done, type(done)
        print "info", info, type(info)
        print "====================="

if __name__ == "__main__":
    # maual_play("CartPole-v0")
    maual_play('MountainCar-v0')