import matplotlib.pyplot as plt
from utils.recorder import get_records

def generate_progress_chart():
    records = get_records()
    if not records:
        return "No data"

    days = {}
    for ts, msg in records:
        day = ts.strftime("%Y-%m-%d")
        days[day] = days.get(day, 0) + 1

    sorted_days = sorted(days.items())
    x = [k for k, _ in sorted_days]
    y = [v for _, v in sorted_days]

    plt.figure(figsize=(6, 3))
    plt.plot(x, y, marker='o')
    plt.title("學習進度記錄")
    plt.xlabel("日期")
    plt.ylabel("次數")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("progress_chart.png")
    return "progress_chart.png"
