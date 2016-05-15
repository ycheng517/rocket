import sys
import numpy as np
from pymongo import MongoClient
from sklearn import linear_model, preprocessing

assert str(sys.argv[1]) is not None
client = MongoClient(str(sys.argv[1]))
db = client.nba_py

variables = ['0', '1', '2', '3', '4', 
             '5', '6', '7', '8', '9', 
             '10', '11', '12', '13', '14', 
             '15', '16', '17', '18', '19', ]

ITERATIONS = 5
MINUTE_RESTRICTION = 10
ALPHA_VALS = [0, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 1]

best_error = 999
best_k = 0

for k in ALPHA_VALS: 
    total_train_error = 0
    total_train_variance = 0
    total_test_error = 0
    total_test_variance = 0
    dumb_total_train_error = 0
    dumb_total_train_variance = 0
    dumb_total_test_error = 0
    dumb_total_test_variance = 0
    baseline_error = 0
    total_count = 0
    for j in range(ITERATIONS):
        for i in range(len(variables)):
        
            allData = []
            allDumbData = []
            
            cursor = db.playtime_model.find({"PLAYER_GROUP": i, "AVG_MIN": {"$gt": MINUTE_RESTRICTION}})
            
            count = 0
            for document in cursor:
                dataRow = []
                for variable in variables:
                    dataRow.append(document[variable])
                dataRow.append(document['AVG_MIN'])
                dataRow.append((document['WIN_CHANCE'])**2)
                dataRow.append(document['MIN'])
                allData.append(dataRow)
                allDumbData.append([document['AVG_MIN'], document['MIN']])
                count = count + 1
        
            print("player group: %d, game count: %d" % (i, count))
            if (count > 600):
                total_count += count
            
                Xy = np.array(allData)
                np.random.shuffle(Xy)
                X = Xy[ :, range(0, Xy.shape[1]-1) ]
                y = Xy[ :, Xy.shape[1]-1 ]
                
                X_normalized = preprocessing.scale(X)
                
                # Separate into Train and Test datasets
                train_test_split = int(round(len(y) * 0.7))
                X_normalized_train = X_normalized[:train_test_split]
                X_normalized_test = X_normalized[train_test_split:]
                y_train = y[:train_test_split]
                y_test = y[train_test_split:]
                
                # train model
                if k == 0: 
                    regr = linear_model.LinearRegression(fit_intercept=True)
                else: 
                    regr = linear_model.Lasso(alpha=k, fit_intercept=True)
                regr.fit(X_normalized_train, y_train)
                
                # Coefficients
                # print('Intercept: ', regr.intercept_) ------------------------------------
                # for i in range(regr.coef_.size): -----------------------------------------
                    # print (variables[i], regr.coef_[i]) ----------------------------------
                # print("================") ------------------------------------------------
                # Error Analysis
                train_error = np.mean((regr.predict(X_normalized_train) - y_train) ** 2)
                train_variance = regr.score(X_normalized_train, y_train)
                test_error = np.mean((regr.predict(X_normalized_test) - y_test) ** 2)
                test_variance = regr.score(X_normalized_test, y_test)
                # print("Residual sum of squares for training set: %.2f" % train_error) ----
                # print('Variance score: %.2f' % train_variance) ---------------------------
                # print("Residual sum of squares for test set: %.2f" % test_error) -
                # print('Variance score: %.2f' % test_variance) --------------------
                total_train_error += train_error * count
                total_train_variance += train_variance * count
                total_test_error += test_error * count
                total_test_variance += test_variance * count
                
                #~~~~calculate against baseline~~~~~~~~~~~
                
                # Xy = np.array(allDumbData) -----------------------------------
                # np.random.shuffle(Xy) ----------------------------------------
                # X = Xy[ :, range(0, Xy.shape[1]-1) ] -------------------------
                # y = Xy[ :, Xy.shape[1]-1 ] -----------------------------------
#  -----------------------------------------------------------------------------
                # X_normalized = (X) -------------------------------------------
#  -----------------------------------------------------------------------------
                # # Separate into Train and Test datasets ----------------------
                # train_test_split = int(round(len(y) * 0.7)) ------------------
                # X_normalized_train = X_normalized[:train_test_split] ---------
                # X_normalized_test = X_normalized[train_test_split:] ----------
                # y_train = y[:train_test_split] -------------------------------
                # y_test = y[train_test_split:] --------------------------------
#  -----------------------------------------------------------------------------
                # regr = linear_model.LinearRegression(fit_intercept=True) -----
                # regr.fit(X_normalized_train, y_train) ------------------------
#  -----------------------------------------------------------------------------
                # # Error Analysis ---------------------------------------------
                # train_error = np.mean((regr.predict(X_normalized_train) - y_train) ** 2) 
                # train_variance = regr.score(X_normalized_train, y_train) -----
                # test_error = np.mean((regr.predict(X_normalized_test) - y_test) ** 2) 
                # test_variance = regr.score(X_normalized_test, y_test) --------
                # # print("Residual sum of squares for training set: %.2f" % train_error) ---- 
                # # print('Variance score: %.2f' % train_variance) --------------------------- 
                # # print("Residual sum of squares for dumb test set: %.2f" % test_error) 
                # # print('Variance score for dumb test set: %.2f' % test_variance) -- 
                # dumb_total_train_error += train_error * count ----------------
                # dumb_total_train_variance += train_variance * count ----------
                # dumb_total_test_error += test_error * count ------------------
                # dumb_total_test_variance += test_variance * count ------------
    
    total_train_error = total_train_error / total_count
    total_train_variance = total_train_variance / total_count
    total_test_error = total_test_error / total_count
    total_test_variance = total_test_variance / total_count
    # dumb_total_train_error = dumb_total_train_error / total_count ------------
    # dumb_total_train_variance = dumb_total_train_variance / total_count ------
    # dumb_total_test_error = dumb_total_test_error / total_count --------------
    # dumb_total_test_variance = dumb_total_test_variance / total_count --------
    print("alpha-value: %.2f" % k)
    print("total_train_error: %.2f" % total_train_error)
    print("total_train_variance: %.2f" % total_train_variance)
    print("total_test_error: %.2f" % total_test_error)
    print("total_test_variance: %.2f" % total_test_variance)
    # print("dumb_total_train_error: %.2f" % dumb_total_train_error) -----------
    # print("dumb_total_train_variance: %.2f" % dumb_total_train_variance) -----
    # print("dumb_total_test_error: %.2f" % dumb_total_test_error) -------------
    # print("dumb_total_test_variance: %.2f" % dumb_total_test_variance) -------
    # print("total_count: %d" % (total_count / ITERATIONS)) --------------------
    
    if (total_test_error < best_error):
        best_error = total_test_error
        best_k = k
    
# Calculate against baseline ---------------------------------------------------
cursor = db.playtime_model.find({"AVG_MIN": {"$gt": MINUTE_RESTRICTION}})
baseline_error = 0.0
count = 0
for document in cursor:
    baseline_error += (document['AVG_MIN'] - document['MIN'])**2
    count += 1
baseline_error = baseline_error / count
print("baseline error: %.2f" % baseline_error)
print("best error: %.2f, best alpha: %.2f" % (best_error, best_k))