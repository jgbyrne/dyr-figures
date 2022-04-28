import matplotlib.pyplot as plt
import math

def main(data):
    X = []
    Y = []
    with open(data) as inf:
        for line in inf:
            parts = line.split()
            s, ml, l = int(parts[0]), float(parts[1].strip()), float(parts[2].strip())
            if s < 5000000:
                X.append(s / 1000000)
                Y.append(-l)

    plt.scatter(X, Y, marker='x', s=3, linewidth=1, c=[[0.2,0.2,0.2]])
    plt.yscale = 'log'
    plt.ylabel("− Log Likelihood (log scale)")
    plt.xlabel("Steps (millions)")
    plt.savefig('convergence.png', bbox_inches='tight', dpi=500)

if __name__ == "__main__":
    main("nar-logl.csv")
