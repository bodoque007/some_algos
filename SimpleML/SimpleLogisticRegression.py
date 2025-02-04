import numpy as np 
import matplotlib.pyplot as plt 
from sklearn.datasets import make_classification 

class LogisticReg:
    def __init__(self, alpha=0.03, num_iterations=300):
        self.alpha = alpha 
        self.num_iterations = num_iterations
        self.b = 0
        self.w = None
    
    def cross_entropy(self, y_pred, y):
        return -1 * np.mean(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred))
    
    def fit(self, X, y):
        m = len(X)
        n = X.shape[1] 
        self.w = np.zeros(n)
        print(self.w)
        for i in range(self.num_iterations):
            y_pred = self.sigmoid(X @ self.w + self.b)
            if i % 100 == 0:
                print(f"Iteration {i} has loss {self.cross_entropy(y_pred, y)}")
            dw = (1/m) * X.T @ (y_pred - y)
            db = (1/m) * np.sum(y_pred - y)
            self.w -= self.alpha * dw
            self.b -= self.alpha * db
    
    def predict(self, X):
        y_pred = self.sigmoid(X @ self.w + self.b)
        return np.where(y_pred >= 0.5, 1, 0)

    def sigmoid(self, z):
        return 1/(1 + np.exp(-z))
    
    def plot(self, X, y, X_new=None, y_pred_new=None):
        if X.shape[1] != 1:
            raise ValueError("Can only plot in one dimension, aka jsut one feature")
        plt.scatter(X[:, 0], y, color="blue", label="Data points")
        plt.plot(X[:, 0], self.predict(X), color="red", label="Line")
        if X_new is not None and y_pred_new is not None:
            plt.scatter(X_new, y_pred_new, color="orange", label="Predictions", marker="o", s=100, edgecolors="black")
        plt.xlabel("X")
        plt.ylabel("y")
        plt.legend()
        plt.show()


model = LogisticReg(0.01, 500)

X, y = make_classification()
## Standarizes X input. Remember that in numpy, axis=0 are the columns
X = (X - np.mean(X, axis=0))/np.std(X, axis=0)
model.fit(X, y)
print(f"Final w learned is {model.w}. b learned is {model.b}")
