import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.datasets import make_regression 


class LinearReg:
    def __init__(self, alpha=0.03, num_iterations=300):
        self.alpha = alpha 
        self.num_iterations = num_iterations
        self.w = np.random.randn() 
        self.b = np.random.randn()
    
    def mse(self, y_pred, y):
        return np.mean((y_pred - y)**2)
    
    def fit(self, X, y):
        m = len(X)
        
        for i in range(self.num_iterations):
            y_pred = X * self.w + self.b
            print(f"Cost at iteration i was {self.mse(y_pred, y)}")
            dw = (2/m) * np.sum((y_pred - y) * X)
            db = (2/m) * np.sum(y_pred - y)

            self.w -= (self.alpha * dw)
            self.b -= (self.alpha * db)

    def predict(self, X_case):
        return X_case * self.w + self.b

    def plot(self, X, y, X_new=None, y_pred_new=None):
        plt.scatter(X, y, color="blue", label="Data points")
        plt.plot(X, self.predict(X), color="red", label="Line")
        if X_new is not None and y_pred_new is not None:
            plt.scatter(X_new, y_pred_new, color="orange", label="Predictions", marker="o", s=100, edgecolors="black")

        plt.xlabel("X")
        plt.ylabel("y")
        plt.legend()
        plt.show()

X, y = make_regression(n_samples=100, n_features=1, noise=10, random_state=42) # Always 42

X = X.flatten()
model = LinearReg(0.01, 500)

X_new = np.linspace(X.min(), X.max(), 9)

model.fit(X, y)

y_pred_new = model.predict(X_new)

model.plot(X, y, X_new, y_pred_new)
