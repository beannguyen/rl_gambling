from keras.engine.saving import load_model
from stable_baselines import DQN
from training.policies.dqn_policy import CustomMlpPolicy


class DQNAgent:
    def __init__(self, saved_model):
        self.saved_model_path = saved_model
        self.model = self._build_model()

    def _build_model(self):
        model = DQN.load(self.saved_model_path, policy=CustomMlpPolicy)
        return model

    def predict(self, state):
        act_values, _ = self.model.predict(state)
        return act_values

    def load(self):
        return load_model(self.saved_model_path)
