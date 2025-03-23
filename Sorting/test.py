import matplotlib.pyplot as plt
import random

def generate_bar_chart():
    numbers = [random.randint(1, 50) for _ in range(10)]  # Generate 10 random numbers
    indices = list(range(1, len(numbers) + 1))  # X-axis indices
    
    plt.figure(figsize=(8, 5))
    plt.bar(indices, numbers, color='blue')
    
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.title("Random Number Bar Chart")
    plt.xticks(indices)
    
    for i, value in enumerate(numbers):
        plt.text(i + 1, value + 1, str(value), ha='center')
    
    plt.show()

# Run the function to display the chart
generate_bar_chart()
