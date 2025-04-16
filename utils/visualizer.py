import matplotlib.pyplot as plt

def generate_dummy_chart():
    plt.figure(figsize=(4,2))
    plt.plot([1, 2, 3], [1, 4, 2])
    plt.title("學習趨勢")
    plt.savefig("/mnt/data/devtrackbot/learning_chart.png")
