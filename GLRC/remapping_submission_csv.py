import csv

id_to_landmarks = {}
write_list = []
score_min = 0.0

with open('submission.csv', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    # skip header
    next(csv_reader)

    for row in csv_reader:
        assert len(row) == 2
        id_to_landmarks[row[0]] = row[1].strip()


with open('test.csv', newline='') as csv_file:
    csv_reader = csv.reader(csv_file)
    # skip header
    next(csv_reader)

    for row in csv_reader:
        assert len(row) == 2
        id = row[0]
        landmark = id_to_landmarks[id] if id in id_to_landmarks else ""
        if landmark:
            tokens = landmark.split(" ")
            infer_category = tokens[1]
            score_str = tokens[2]
            score = float(score_str)
            if score < score_min:
                landmark = ""
            else:
                landmark = " ".join([infer_category, score_str])
        write_list.append([id, landmark])

with open('submission_mapped_filter_by_score.csv', 'w', newline='') as f:
    write_list.insert(0, ["id", "landmarks"])

    writer = csv.writer(f)
    writer.writerows(write_list)