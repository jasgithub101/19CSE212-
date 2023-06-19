class AuctionItem:
    def __init__(self, item_id, item_name, item_description, bid_start_price):
        self.item_id = item_id
        self.item_name = item_name
        self.item_description = item_description
        self.bid_start_price = bid_start_price


class HybridAuctionPlatform:
    class MaxHeap:
        def __init__(self):
            self.heap = []

        def insert(self, bid_amount, bidder_name):
            self.heap.append((bid_amount, bidder_name))
            self._bubble_up(len(self.heap) - 1)

        def get_highest_bid(self):
            if not self.heap:
                return None
            return self.heap[0]

        def _bubble_up(self, index):
            parent_index = (index - 1) // 2

            while index > 0 and self.heap[index][0] > self.heap[parent_index][0]:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
                parent_index = (index - 1) // 2

    def __init__(self, size=10):
        self.size = size
        self.items = {}
        self.table = [[] for _ in range(self.size)]

    def _hash_function(self, key):
        return sum(ord(char) for char in str(key)) % self.size

    def insert(self, item_id, item_name, item_description, bid_start_price):
        if item_id in self.items:
            print("Item with the same ID already exists.")
            return

        item = AuctionItem(item_id, item_name, item_description, bid_start_price)
        item.bid_heap = self.MaxHeap()
        index = self._hash_function(item_id)
        self.items[item_id] = item
        self.items[item_id].index = index
        self.table[index].append(item_id)
        print("Item added successfully.")

    def search(self, item_id):
        if item_id in self.items:
            return self.items[item_id]
        return None

    def delete(self, item_id):
        if item_id in self.items:
            item = self.items[item_id]
            item.bid_heap = None
            del self.items[item_id]
            index = self._hash_function(item_id)
            self.table[index].remove(item_id)

    def place_bid(self, item_id, bidder_name, bid_amount):
        item = self.search(item_id)

        if not item:
            print("Invalid item ID.")
            return

        if bid_amount < item.bid_start_price:
            print("Bid amount is lower than the starting bid price.")
            return

        if item.bid_heap.get_highest_bid() is not None and bid_amount <= item.bid_heap.get_highest_bid()[0]:
            print("Bid amount is lower than the current highest bid.")
            return

        item.bid_heap.insert(bid_amount, bidder_name)
        print("Bid placed successfully.")

    def get_items(self):
        return list(self.items.values())

    def display_items(self):
        items = self.get_items()

        if not items:
            print("No items on auction.")
            return

        for item in items:
            current_highest_bid = item.bid_heap.get_highest_bid()

            print(f"Item ID: {item.item_id}")
            print(f"Item Name: {item.item_name}")
            print(f"Item Description: {item.item_description}")
            print(f"Bid Start Price: {item.bid_start_price}")

            if current_highest_bid:
                print(f"Current Highest Bid: {current_highest_bid[0]} by {current_highest_bid[1]}")
            else:
                print("No bids placed for this item.")

            print()

    def print_bids(self, item_id):
        item = self.search(item_id)

        if not item:
            print("Invalid item ID.")
            return

        bids = item.bid_heap.heap

        if not bids:
            print("No bids placed for this item.")
            return

        print(f"Bids history for Item ID: {item.item_id}")
        sorted_bids = sorted(bids, key=lambda x: x[0], reverse=True)
        for i in range(len(sorted_bids)):
            bid = sorted_bids[i]
            print(f"{i+1}) {bid[0]} by {bid[1]}")


    def end_auction(self, item_id):
        item = self.search(item_id)

        if not item:
            print("Invalid item ID.")
            return


        highest_bid = item.bid_heap.get_highest_bid()

        if highest_bid:
            print(f"Highest bid for {item.item_name}: {highest_bid[0]} by {highest_bid[1]}")
        else:
            print("No bids placed for this item.")

        item.bid_heap = None
        self.delete(item_id)


def display_menu():
    print("==== Auction Platform Menu ====")
    print("1. Add Item to Auction")
    print("2. Place a Bid")
    print("3. End Auction for an Item")
    print("4. View Items on Auction")
    print("5. Print Bids for an Item")
    print("6. Exit")


def main():
    auction_platform = HybridAuctionPlatform()

    while True:
        display_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            item_id = input("Enter Item ID: ")
            item_name = input("Enter Item Name: ")
            item_description = input("Enter Item Description: ")
            bid_start_price = input("Enter Bid Start Price: ")

            try:
                bid_start_price = float(bid_start_price)
                auction_platform.insert(item_id, item_name, item_description, bid_start_price)
            except ValueError:
                print("Invalid bid start price. Please enter a valid number.")
        elif choice == "2":
            item_id = input("Enter Item ID: ")
            bidder_name = input("Enter Bidder Name: ")
            bid_amount = input("Enter Bid Amount: ")

            try:
                bid_amount = float(bid_amount)
                auction_platform.place_bid(item_id, bidder_name, bid_amount)
            except ValueError:
                print("Invalid bid amount. Please enter a valid number.")
        elif choice == "3":
            item_id = input("Enter Item ID: ")
            auction_platform.end_auction(item_id)
        elif choice == "4":
            auction_platform.display_items()
        elif choice == "5":
            item_id = input("Enter Item ID: ")
            auction_platform.print_bids(item_id)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
