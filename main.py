from pathlib import Path
import urllib.request
import tarfile
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split


def load_housing_data():
    tarball_path = Path("datasets/housing.tgz")
    if not tarball_path.is_file():
        Path("datasets").mkdir(parents=True, exist_ok=True)
        url = "https://github.com/ageron/data/raw/main/housing.tgz"
        urllib.request.urlretrieve(url, tarball_path)
    with tarfile.open(tarball_path) as housing_tarball:
        housing_tarball.extractall(path="datasets")
    return pd.read_csv(Path("datasets/housing/housing.csv"))


def main():
    housing = load_housing_data()

    housing["income_cat"] = pd.cut(housing["median_income"],
                                     bins=[0., 1.5, 3.0, 4.5, 6.0, np.inf],
                                     labels=[1, 2, 3, 4, 5])

    strat_train_set, strat_test_set = train_test_split(housing,
                                                       test_size=0.2,
                                                       stratify=housing["income_cat"],
                                                       random_state=42)

    train_set, test_set = train_test_split(housing,
                                           test_size=0.2,
                                           random_state=42)

    compare_props = pd.DataFrame({
        "Overall %": income_cat_proportions(housing),
        "Stratified %": income_cat_proportions(strat_test_set),
        "Random %": income_cat_proportions(test_set)
    }).sort_index()
    compare_props.index.name = "Income Category"
    compare_props["Strat. Error %"] = (compare_props["Stratified %"] / compare_props["Overall %"] - 1)
    compare_props["Rand. Error %"] = (compare_props["Random %"] / compare_props["Overall %"] - 1)

    (compare_props * 100).round(2)
    plt.show()


def income_cat_proportions(data):
    return data["income_cat"].value_counts() / len(data)


if __name__ == "__main__":
    main()
