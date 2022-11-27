# 10 Steps to master Object oriented programming in Python #

## Step 1
```
class MLbox:
    pass
ml_obj = MLbox      # Both are class names
ml_obj2 = MLbox()   # ml_obj2 is instantiated object from class MLbox 


```

## Step 2
```
class MLbox:
    def training(self):
        print("ML training is in progress....")

# ml_obj = MLbox    # both are the classes
# ml_obj.training() # training() method need actual class instantiated object
# ml_obj.training(ml_obj2) # will work 

ml_obj2 = MLbox()
ml_obj2.training()
```


## Step 3
```
class MLbox:
    def __init__(self):
        self.name = "class name"
        self.properties = "class properties"
        self.algorithm = "gbm"
        self.apply_automl = False

    def training(self):
        print("ML training is in progress with {} algorithm....".format(self.algorithm))


ml_obj1 = MLbox()
ml_obj1.training()

ml_obj2 = MLbox()
ml_obj2.training()
```

## Step 4
```
class MLbox:
    def __init__(self, algorithm, apply_automl):
        self.name = "class name"
        self.properties = "class properties"
        self.algorithm = algorithm
        self.apply_automl = apply_automl

    def training(self):
        with_auto_ml = "without automl "
        if self.apply_automl:
            with_auto_ml = "with automl "
        print("ML training is in progress with {} "
              "algorithm {}....".format(self.algorithm, with_auto_ml))


ml_obj1 = MLbox("gbm", False)
ml_obj1.training()

ml_obj2 = MLbox("random_forest", True)
ml_obj2.training()

```

## Step 5
```
class MLbox:
    def __init__(self, algorithm, apply_automl):
        self.name = "class name"
        self.properties = "class properties"
        self.algorithm = algorithm
        self.apply_automl = apply_automl
        self.automl_size = 3
        self.applied_algorithms = []
        self.supported_algorithms = ["gbm", "glm", "random_forest", "naive_bayes",
                                     "xgboost", "lightgbm"]

    def configure(self):
        if self.algorithm in self.supported_algorithms:
            self.applied_algorithms.append(self.algorithm)
        if self.apply_automl:
            for each_algo in self.supported_algorithms:
                if len(self.applied_algorithms) >= self.automl_size:
                    break
                if each_algo not in self.applied_algorithms:
                    self.applied_algorithms.append(each_algo)

    def training(self):
        if len(self.applied_algorithms) == 0:
            print("No algo to apply for training..")
            return None

        with_auto_ml = "without automl "
        if self.apply_automl:
            with_auto_ml = "with automl "
        print("ML training is in progress with {} "
              "algorithms {}....".format(", ".join(self.applied_algorithms), with_auto_ml))


ml_obj1 = MLbox("gbm", False)
ml_obj1.configure()
ml_obj1.training()

ml_obj2 = MLbox("random_forest", True)
ml_obj2.configure()
ml_obj2.training()

```


## Step 6
```
class ControlBox:
    def __new__(cls, choice, *args, **kwargs):
        if choice == 'data':
            return Databox(*args, **kwargs)
        elif choice == 'ml':
            return MLbox(*args, **kwargs)
        else:
            return None

class Databox:
    def __init__(self, action):
        self.name = "data class"
        self.properties = "data class properties"
        self.supported_actions = ["skew", "anomaly", "drift"]
        self.action = action
        self.active_action = []

    def configure(self):
        if self.action in self.supported_actions:
            self.active_action = self.action


class MLbox:
    def __init__(self, algorithm, apply_automl):
        self.name = "class name"
        self.properties = "class properties"
        self.algorithm = algorithm
        self.apply_automl = apply_automl
        self.automl_size = 3
        self.applied_algorithms = []
        self.supported_algorithms = ["gbm", "glm", "random_forest", "naive_bayes",
                                     "xgboost", "lightgbm"]

    def configure(self):
        if self.algorithm in self.supported_algorithms:
            self.applied_algorithms.append(self.algorithm)
        if self.apply_automl:
            for each_algo in self.supported_algorithms:
                if len(self.applied_algorithms) >= self.automl_size:
                    break
                if each_algo not in self.applied_algorithms:
                    self.applied_algorithms.append(each_algo)

    def training(self):
        if len(self.applied_algorithms) == 0:
            print("No algo to apply for training..")
            return None

        with_auto_ml = "without automl "
        if self.apply_automl:
            with_auto_ml = "with automl "
        print("ML training is in progress with {} "
              "algorithms {}....".format(", ".join(self.applied_algorithms), with_auto_ml))


ml_obj = ControlBox("ml", "gbm", False)
ml_obj.configure()
ml_obj.training()

data_obj = ControlBox("data", "skew")
data_obj.configure()

```

## Step 7
```
class MLbox:
    def __init__(self, algorithm, apply_automl):
        self.name = "class name"
        self.properties = "class properties"
        self.algorithm = algorithm
        self.apply_automl = apply_automl
        self.automl_size = 3
        self.applied_algorithms = []
        self.supported_algorithms = ["gbm", "glm", "random_forest", "naive_bayes",
                                     "xgboost", "lightgbm"]

    def configure(self):
        if self.algorithm in self.supported_algorithms:
            self.applied_algorithms.append(self.algorithm)
        if self.apply_automl:
            for each_algo in self.supported_algorithms:
                if len(self.applied_algorithms) >= self.automl_size:
                    break
                if each_algo not in self.applied_algorithms:
                    self.applied_algorithms.append(each_algo)

    def training(self):
        if len(self.applied_algorithms) == 0:
            print("No algo to apply for training..")
            return None

        with_auto_ml = "without automl "
        if self.apply_automl:
            with_auto_ml = "with automl "
        print("ML training is in progress with {} "
              "algorithms {}....".format(", ".join(self.applied_algorithms), with_auto_ml))


class GbmInAction(MLbox):
    pass


class GlmInAction(MLbox):
    def __init__(self, apply_automl):
        super().__init__("glm", apply_automl)


class RandomForestInAction(MLbox):
    def __init__(self):
        super().__init__("random_forest", False)


gbm_obj = GbmInAction("gbm", False)
glm_obj = GlmInAction(True)
rf_obj = RandomForestInAction()


if __name__ == "__main__":
    gbm_obj.configure()
    gbm_obj.training()

    glm_obj.configure()
    glm_obj.training()

    rf_obj.configure()
    rf_obj.training()
```

## Step 8
```
class MLbox:
    def __init__(self, algorithm, apply_automl):
        self.name = "class name"
        self.properties = "class properties"
        self.algorithm = algorithm
        self.apply_automl = apply_automl
        self.automl_size = 3
        self.applied_algorithms = []
        self.supported_algorithms = ["gbm", "glm", "random_forest", "naive_bayes",
                                     "xgboost", "lightgbm"]

    def configure(self):
        if self.algorithm in self.supported_algorithms:
            self.applied_algorithms.append(self.algorithm)
        if self.apply_automl:
            for each_algo in self.supported_algorithms:
                if len(self.applied_algorithms) >= self.automl_size:
                    break
                if each_algo not in self.applied_algorithms:
                    self.applied_algorithms.append(each_algo)

    def training(self):
        if len(self.applied_algorithms) == 0:
            print("No algo to apply for training..")
            return None

        with_auto_ml = "without automl "
        if self.apply_automl:
            with_auto_ml = "with automl "
        print("ML training is in progress with {} "
              "algorithms {}....".format(", ".join(self.applied_algorithms), with_auto_ml))


class GbmInAction(MLbox):
    def __init__(self, apply_automl):
        super().__init__("gbm", apply_automl)


class RandomForestInAction(MLbox):
    def __init__(self):
        super().__init__("random_forest", False)


class BoostingMachine:
    def __new__(cls, choice, *args, **kwargs):
        if choice == 'gbm':
            return GbmInAction(*args, **kwargs)
        elif choice == 'rf':
            return RandomForestInAction()
        else:
            return None


bm_gbm_obj = BoostingMachine("gbm", True)
bm_rf_obj = BoostingMachine("rf")


if __name__ == "__main__":
    bm_gbm_obj.configure()
    bm_gbm_obj.training()

    bm_rf_obj.configure()
    bm_rf_obj.training()


```


## Step 9
```
class MlOps:
    def monitoring(self):
        print("MLOps >>> Monitoring...")


class MLbox(MlOps):
    def __init__(self, algorithm, apply_automl):
        self.name = "class name"
        self.properties = "class properties"
        self.algorithm = algorithm
        self.apply_automl = apply_automl
        self.automl_size = 3
        self.applied_algorithms = []
        self.supported_algorithms = ["gbm", "glm", "random_forest", "naive_bayes",
                                     "xgboost", "lightgbm"]

    def configure(self):
        if self.algorithm in self.supported_algorithms:
            self.applied_algorithms.append(self.algorithm)
        if self.apply_automl:
            for each_algo in self.supported_algorithms:
                if len(self.applied_algorithms) >= self.automl_size:
                    break
                if each_algo not in self.applied_algorithms:
                    self.applied_algorithms.append(each_algo)

    def training(self):
        if len(self.applied_algorithms) == 0:
            print("No algo to apply for training..")
            return None

        with_auto_ml = "without automl "
        if self.apply_automl:
            with_auto_ml = "with automl "
        print("ML training is in progress with {} "
              "algorithms {}....".format(", ".join(self.applied_algorithms), with_auto_ml))


def init(self, algorithm, apply_automl):
    self.algorithm = algorithm
    self.apply_automl = apply_automl
    self.applied_algorithms = ['algorithm']


# class = type(classname, base(s), dict)
MLboxNew = type("MLboxNew", (MLbox, ), {"__init__": init})

ml_obj = MLboxNew("gmb", True)
ml_obj.monitoring()
ml_obj.configure()
ml_obj.training()

```


## Step 10
```
from dataclasses import dataclass

@dataclass
class MLBox:
    algorithm: str
    apply_automl: bool
    supported_algorithms = ['gbm', 'glm', 'rf']

    def training(self):
        with_auto_ml = "without automl "
        if self.apply_automl:
            with_auto_ml = "with automl "
        print("ML training is in progress with {} "
              "algorithm {}....".format(self.algorithm, with_auto_ml))


ml_obj = MLBox("gbm", False)
ml_obj.training()

```









