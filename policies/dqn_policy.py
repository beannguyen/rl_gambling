from stable_baselines.deepq.policies import FeedForwardPolicy


class CustomMlpPolicy(FeedForwardPolicy):
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch,
                 reuse=False, obs_phs=None, dueling=True, **_kwargs):
        super(CustomMlpPolicy, self).__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse,
                                              feature_extraction="mlp", obs_phs=obs_phs, dueling=dueling, layers=[24, 24],
                                              layer_norm=False, **_kwargs)
