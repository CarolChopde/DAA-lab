import csv
class Item:
    def __init__(self, name, wt, val, shelflife):
        self.name = name
        self.wt = wt
        self.val = val
        self.shelflife = shelflife
        self.valPerwt = self.val/self.wt

def FractionalKnapsack(W, items):
    if (W <= 0):
        raise ValueError("Capacity of the knapsack cannot be zero")
    if not items :
        raise ValueError("List of items cannot be empty")
    
    #sorting the items in decreasing order of valPerwt and shelfLife
    items.sort(key=lambda x: (x.valPerwt, x.shelflife), reverse="True") 

    v = 0
    for item in items:
        if W <= 0: #knapsack is full
            break
        else:
            if item.wt < W: #knapsack is not full
                v += item.val
                W -= item.wt
            else:
                frac = W/item.wt
                v += item.val * frac
                W = 0
    return v
                
def load_from_csv(filename):
    items = []
    try:
        with open (filename, mode ='r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)

            if header is None:
                raise ValueError ("File empty")
            req_columns = ["name","weight","value","shelflife"]
            if header != req_columns:
                raise ValueError("csv file missing req attributes")
            
            for row in csv_reader:
                try:
                    name = row[0]
                    wt = float(row[1])
                    val = float(row[2])
                    shelflife = int(row[3])

                    if wt <= 0 or val <= 0 or shelflife <= 0:
                        raise ValueError(f"Invalid data in row {row}")
                    
                    item = Item(name, wt, val, shelflife)
                    items.append(item)
                except ValueError as e:
                    print(f"Error: Invalid data in row {row} - {e}")
                    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except ValueError as e:
        print(f"Error in CSV file format: {e}")

    return items

def main():
    try:
        # Load items from a CSV file
        items = load_from_csv('items.csv')
        
        # Transport vehicle capacity
        W = 200
        total_value = FractionalKnapsack(W, items)
        print(f"Total value possible to be shipped: {total_value:.2f}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

        
