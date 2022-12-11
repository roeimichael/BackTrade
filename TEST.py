import pandas as pd
from sklearn.tree import DecisionTreeClassifier

date_df = pd.read_csv("./data/dates/2021-10-26.csv")
next_date_df = pd.read_csv("./data/dates/2021-10-27.csv")
target_df = pd.read_csv("./data/Targets.csv")

X_train = date_df.drop(['ticker'], axis=1)  # the current day data
X_test = next_date_df.drop(['ticker'], axis=1)  # next day data
y_train = target_df['2021-10-27']  # takes the next day target
y_validate = target_df['2021-10-28']  # day after the next target
clf = DecisionTreeClassifier(max_depth=5)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

n_nodes = clf.tree_.node_count
children_left = clf.tree_.children_left
children_right = clf.tree_.children_right
feature = clf.tree_.feature
threshold = clf.tree_.threshold

node_indicator = clf.decision_path(X_test)
print(node_indicator)
leave_id = clf.apply(X_test)

sample_id = 0
node_index = node_indicator.indices[node_indicator.indptr[sample_id]:
                                    node_indicator.indptr[sample_id + 1]]
print('Rules used to predict sample %s: ' % sample_id)
for node_id in node_index:

    if leave_id[sample_id] == node_id:  # <-- changed != to ==
        # continue # <-- comment out
        print("leaf node {} reached, no decision here".format(leave_id[sample_id]))  # <--

    else:  # < -- added else to iterate through decision nodes
        if X_test[sample_id, feature[node_id]] <= threshold[node_id]:
            threshold_sign = "<="
        else:
            threshold_sign = ">"

        print("decision id node %s : (X[%s, %s] (= %s) %s %s)"
              % (node_id,
                 sample_id,
                 feature[node_id],
                 X_test[sample_id, feature[node_id]],  # <-- changed i to sample_id
                 threshold_sign,
                 threshold[node_id]))
