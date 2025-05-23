import os
import csv
from itertools import combinations
from collections import defaultdict


def read_transactions_from_csv(filename):
    transactions = []
    with open(filename, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            transaction = [item.strip() for item in row if item.strip()]
            if transaction:
                transactions.append(transaction)
    return transactions


def apriori_tid(transactions, min_support):
    num_transactions = len(transactions)
    min_count = min_support * num_transactions


    tid_table = []
    item_counts = defaultdict(int)

    for tid, transaction in enumerate(transactions):
        for item in transaction:
            itemset = frozenset([item])
            item_counts[itemset] += 1
        tid_table.append((tid, [frozenset([item]) for item in transaction]))


    frequent_itemsets = dict()
    Lk = {itemset: count for itemset, count in item_counts.items() if count >= min_count}
    frequent_itemsets.update(Lk)
    k = 2

    while Lk:

        candidates = generate_candidates(Lk.keys(), k)

        new_tid_table = []
        candidate_counts = defaultdict(int)

        for tid, itemsets in tid_table:

            itemsets_set = set(itemsets)
            transaction_items = set().union(*itemsets_set)

            matched_candidates = []
            for candidate in candidates:
                if candidate.issubset(transaction_items):
                    candidate_counts[candidate] += 1
                    matched_candidates.append(candidate)
            if matched_candidates:
                new_tid_table.append((tid, matched_candidates))

        Lk = {itemset: count for itemset, count in candidate_counts.items() if count >= min_count}
        frequent_itemsets.update(Lk)
        tid_table = new_tid_table
        k += 1

    return frequent_itemsets, num_transactions


def generate_candidates(prev_frequent_itemsets, k):

    candidates = set()
    itemsets_list = list(prev_frequent_itemsets)
    for i in range(len(itemsets_list)):
        for j in range(i + 1, len(itemsets_list)):
            union_set = itemsets_list[i] | itemsets_list[j]
            if len(union_set) == k:
                candidates.add(union_set)
    return candidates



if __name__ == "__main__":
    file_path = os.path.join(os.path.dirname(__file__), 'wine_transactions 5000 Record.csv')
    transactions = read_transactions_from_csv(file_path)

    min_support = 0.2

    frequent_itemsets, total_transactions = apriori_tid(transactions, min_support)

    print("📦 Frequent Itemsets (AprioriTID):")
    for itemset, count in frequent_itemsets.items():
        support = count / total_transactions
        print(f"{set(itemset)}: support = {support:.2f}")
