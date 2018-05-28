import csv

id_to_pred = {}
write_list = []

TOP_K = 5

with open('submission.csv', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    # skip header
    next(csv_reader)

    for row in csv_reader:
        assert len(row) == 2
        id_to_pred[row[0]] = row[1].strip()


with open('test.csv', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    # skip header
    next(csv_reader)

    for row in csv_reader:
        assert len(row) == 2
        img_id = row[0]
        pred = id_to_pred[img_id] if img_id in id_to_pred else ""
        if pred:
            tokens = pred.split(" ")
            top1_class = tokens[1]
            top1_score = tokens[2]
            topK_index = 3
            topK_scores = [float(s) for s in tokens[topK_index:topK_index+TOP_K]]

            pred = " ".join([top1_class, top1_score])


with open('submission_mapped.csv', 'w', newline='') as f:
    write_list.insert(0, ["id", "landmarks"])

    writer = csv.writer(f)
    writer.writerows(write_list)
