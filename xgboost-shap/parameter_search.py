import xgboost as xgb
import shap
import numpy as np
import matplotlib.pyplot as plt
import scipy
from sklearn.model_selection import train_test_split
import argparse

def main(n):
	parser = argparse.ArgumentParser()

	# parameter combination index
	parser.add_argument('-i', action="store", dest="i", type=int)
	args = parser.parse_args()

	# upload data matrix into X, y
	dtrain = xgb.DMatrix('workdir/dmatrix_bin')
	X = scipy.sparse.csr_matrix.toarray(dtrain.get_data())
	y = dtrain.get_label()

	# split into training and testing
	x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

	### conduct a grid search over max_depth and min_child_weight
	from itertools import product
	# max_depth_values = list(range(3, 10, 2))
	# max_depth_values = list(range(9, 16, 2))
	max_depth_values = list(range(15, 22))
	# min_child_weight_values = list(range(1, 6, 2))
	# min_child_weight_values = list(range(2, 5))
	min_child_weight_values = [2]
	comb = list(product(max_depth_values, min_child_weight_values))
	md, mcw = comb[args.i]
	
    ### search over sampling parameters
	# sample_values = [0.7, 0.8, 0.9]
	st, sl, ss = 0.8, 0.8, 0.8
	# if args.i // 3 == 0:
	# 	st = sample_values[args.i % 3]
	# elif args.i // 3 == 1:
	# 	sl = sample_values[args.i % 3]
	# else:
	# 	ss = sample_values[args.i % 3]

    # define parameters
	num_round = 50
	params = {
		"eta" : 0.10,
		"gamma" : 0,
		"colsample_bytree" : st,
		"colsample_bylevel" : sl,
		"subsample" : ss, 
		"tree_method" : "hist", 
		"grow_policy" : "lossguide",
		"max_depth": 17,
		"min_child_weight" : 2,
		"n_estimators" : num_round,
		"early_stopping_rounds" : num_round//10 
	}

    # initialize XGBoost Regressor and train
	model = xgb.XGBRegressor(**params)
	model.fit(x_train, y_train, eval_set=[(x_test, y_test)])


if __name__ == '__main__':
    main()