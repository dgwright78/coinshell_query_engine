import csv

def silver_calc(coins, fineness):
    result = sum(
        1 for coin in coins
        if float(coin["fineness"]) == fineness
    )
    return result

total_coins = 0
monarch_count = {}
metal_count = {}
sterling_count = 0

silver_coins = {
    "florin": 11.31,
    "shilling": 5.66
}

key_dates = {
    ("penny", "1869"),
    ("florin", "1911")
}

total_silver = 0

with open("./coins.csv") as file:
    reader = csv.DictReader(file)

    coins = list(reader)

    sterling_coins = silver_calc(coins, 92.5)
    half_silver = silver_calc(coins, 50)

    for coin in coins:
        total_coins += 1
        monarch = coin["monarch"]
        metal = coin["metal"]
        fineness = float(coin["fineness"])

        monarch_count[monarch] = monarch_count.get(monarch, 0) + 1
        metal_count[metal] = metal_count.get(metal, 0) + 1

        if coin["metal"] == "silver":
            denom = coin["denomination"]
            total_silver += (silver_coins.get(denom, 0) * (fineness / 100))
        
        output_str = coin["year"] + " " + coin["denomination"]
        if (coin["denomination"], coin["year"]) in key_dates:
            output_str += ": Key Date"
        print(output_str)

print(f"Total coins: {total_coins}")
print("\nCoins by monarch:")
for monarch, count in monarch_count.items():
    print(monarch, count)
print("\nCoins by metal:")
for metal, count in metal_count.items():
    print(metal, count)
print(f"\nSterling silver coins: {sterling_coins}")
print(f"\n50% silver coins: {half_silver}")
print(f"Total silver weight in collection: {round(total_silver, 2)}g")