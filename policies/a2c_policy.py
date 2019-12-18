from stable_baselines.common.policies import FeedForwardPolicy


class A2CMlpPolicy(FeedForwardPolicy):
    def __init__(self, sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse=False, **_kwargs):
        super(A2CMlpPolicy, self).__init__(sess, ob_space, ac_space, n_env, n_steps, n_batch, reuse,
                                           net_arch=[dict(pi=[16, 32, 16],
                                                          vf=[16, 32, 16])],
                                           feature_extraction="mlp", **_kwargs)
