from stable_baselines import A2C
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import SubprocVecEnv

from fb_env.envs.fb_env import BookmakerEnv


def train_a2c(env_name='fb-v0', e=0):
    # multiprocess environment
    n_cpu = 4
    env = SubprocVecEnv([lambda: BookmakerEnv(data_path='csv_files/train-12122019.json', seed=i) for i in range(n_cpu)])

    model = A2C(MlpPolicy, env, verbose=2,
                tensorboard_log='tensorboard')
    model.learn(total_timesteps=100000000, seed=1)
    model.save(f"saved/{A2C.__name__}_{env_name}_{e}")


if __name__ == '__main__':
    # for i in range(3):
    train_a2c(env_name='fb-v0', e=0)
