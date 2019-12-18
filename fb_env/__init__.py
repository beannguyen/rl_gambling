from gym.envs.registration import register

register(
    id='fb-v0',
    entry_point='fb_env.envs:BookmakerEnv',
)

# register(
#     id='fb-v1',
#     entry_point='fb_env.envs:ContinuousBookmakerEnv',
# )
