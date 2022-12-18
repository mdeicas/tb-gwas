import xgboost as xgb
import shap
import numpy as np
import matplotlib.pyplot as plt
import scipy
from sklearn.model_selection import train_test_split

def main():

    # upload DMatrix from binary and get X, y
    dtrain = xgb.DMatrix('workdir/dmatrix_bin')
    X = scipy.sparse.csr_matrix.toarray(dtrain.get_data())
    y = dtrain.get_label()

    # split X, y into training and testing
    x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    # set parameters
    num_round = 150
    params = {
		"eta" : 0.10,
		"gamma" : 0,
		"colsample_bytree" : 0.8,
		"colsample_bylevel" : 0.9,
		"subsample" : 0.8, 
		"tree_method" : "hist", 
		"grow_policy" : "lossguide",
		"max_depth": 3,
		"min_child_weight" : 2,
		"n_estimators" : num_round,
	}

    # initialize XGBoost regressor and train the model. 
    model = xgb.XGBRegressor(**params)
    model.fit(x_train, y_train, eval_set=[(x_test, y_test)])

    # save the XGBoost model and calculate shap values
    model.save_model(f"/workdir/model.json")
    explainer = shap.TreeExplainer(model)
    shap_values_xgb = explainer.shap_values(dtrain.get_data())

    # xgb tree plot
    xgb.plot_tree(model)
    plt.savefig(f"/workdir/xgboost_tree", dpi=500)
    plt.clf()

    # shap dependence plot
    shap.dependence_plot("Feature 6274", shap_values_xgb, X)
    plt.savefig(f"/workdir/shap_dependence_plot_f_6274", dpi=200)
    plt.clf()

    # shap summary plot
    shap.summary_plot(shap_values_xgb, dtrain.get_data(), plot_type="bar", show = False)
    plt.savefig(f"/workdir/shap_summary_plot", dpi=200)
    plt.clf()

    # save shap values
    np.savetxt(f"/workdir/shap_values.txt", np.array(shap_values_xgb))

if __name__ == '__main__':
    main()