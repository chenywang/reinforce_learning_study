import tensorflow as tf
import numpy as np
import gym

from RL_brain.actor_critic import Actor, Critic

np.random.seed(2)
tf.set_random_seed(2)  # reproducible

OUTPUT_GRAPH = False
MAX_EPISODE = 1000
MAX_EP_STEPS = 200
DISPLAY_REWARD_THRESHOLD = -100  # renders environment if total episode reward is greater then this threshold
RENDER = False  # rendering wastes time
GAMMA = 0.9
LR_A = 0.001    # learning rate for actor
LR_C = 0.01     # learning rate for critic

env = gym.make('Pendulum-v0')
env.seed(1)  # reproducible
env = env.unwrapped

N_S = env.observation_space.shape[0]
A_BOUND = env.action_space.high

sess = tf.Session()

actor = Actor(sess, n_features=N_S, lr=LR_A, action_bound=[-A_BOUND, A_BOUND])
critic = Critic(sess, n_features=N_S, lr=LR_C)

sess.run(tf.global_variables_initializer())

if OUTPUT_GRAPH:
    tf.summary.FileWriter("logs/", sess.graph)

for i_episode in range(MAX_EPISODE):
    s = env.reset()
    t = 0
    ep_rs = []
    while True:
        # if RENDER:
        env.render()
        a = actor.choose_action(s)

        s_, r, done, info = env.step(a)
        r /= 10

        td_error = critic.learn(s, r, s_)  # gradient = grad[r + gamma * V(s_) - V(s)]
        actor.learn(s, a, td_error)  # true_gradient = grad[logPi(s,a) * td_error]

        s = s_
        t += 1
        ep_rs.append(r)
        if t > MAX_EP_STEPS:
            ep_rs_sum = sum(ep_rs)
            if 'running_reward' not in globals():
                running_reward = ep_rs_sum
            else:
                running_reward = running_reward * 0.9 + ep_rs_sum * 0.1
            if running_reward > DISPLAY_REWARD_THRESHOLD: RENDER = True  # rendering
            print("episode:", i_episode, "  reward:", int(running_reward))
            break
