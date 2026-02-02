def batch_items(items, batch_size=2):
    total = len(items)
    for i in range(0, total, batch_size):
        yield items[i:i + batch_size], (i // batch_size + 1), ((total + batch_size - 1) // batch_size)
