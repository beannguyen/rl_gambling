from keras.engine.saving import load_model
from stable_baselines import A2C
from training.policies.a2c_policy import A2CMlpPolicy


class A2CAgent:
    def __init__(self, saved_model):
        self.saved_model_path = saved_model
        self.model = self._build_model()

    def _build_model(self):
        return A2C.load(self.saved_model_path)

    def predict(self, state):
        act_values, _ = self.model.predict(state)
        return act_values

    def load(self):
        return load_model(self.saved_model_path)
