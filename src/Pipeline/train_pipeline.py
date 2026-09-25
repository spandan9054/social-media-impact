from src.Components.data_ingestion import Data, SplitData
from src.Components.data_transformation import DataProcessing
from src.logger import logging
from imblearn.over_sampling import SMOTENC
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
    OrdinalEncoder,
    FunctionTransformer
)
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
import numpy as np
import sys
from src.exception import CustomException


class TrainingPipeline:

    def __init__(self):
        pass

    def Pipelines(self):
        """
        Creates the preprocessing pipelines required before and
        after SMOTENC.
        """

        try:

            # -------------------------------------------------
            # Load data
            # -------------------------------------------------

            X, y = Data.load_data(
                'E:\\Projects\\social_impact\\Social_media_impact_on_life.csv'
            )

            # -------------------------------------------------
            # Train-test split
            # -------------------------------------------------

            split = SplitData(X, y)

            X_train, X_test, y_train, y_test = split.split_data()

            # -------------------------------------------------
            # Get column groups
            # -------------------------------------------------

            data_processing = DataProcessing()

            numerical_cols, label_categorical, ohe_categorical = (
                data_processing.pipeline_columns()
            )

            # -------------------------------------------------
            # Numerical preprocessing
            # -------------------------------------------------

            numerical_pipeline = Pipeline(
                steps=[
                    ('impute', SimpleImputer(strategy='median')),

                    ('log', FunctionTransformer(
                        np.log1p,
                        feature_names_out='one-to-one'
                    ))
                ]
            )

            # -------------------------------------------------
            # Categorical preprocessing for SMOTENC
            # -------------------------------------------------

            categorical_pipeline = Pipeline(
                steps=[
                    ('impute', SimpleImputer(
                        strategy='most_frequent'
                    )),

                    ('ordinal_encoder', OrdinalEncoder(
                        handle_unknown='use_encoded_value',
                        unknown_value=-1
                    ))
                ]
            )

            # -------------------------------------------------
            # Preprocessor before SMOTENC
            # -------------------------------------------------

            preprocessor = ColumnTransformer(
                transformers=[
                    ('num', numerical_pipeline, numerical_cols),

                    (
                        'cat_label',
                        categorical_pipeline,
                        label_categorical
                    ),

                    (
                        'cat_ohe',
                        categorical_pipeline,
                        ohe_categorical
                    )
                ]
            )

            # -------------------------------------------------
            # Number of numerical columns
            # -------------------------------------------------

            numerical_count = len(numerical_cols)

            # All categorical columns come after numerical columns
            categorical_indices = list(
                range(
                    numerical_count,
                    numerical_count
                    + len(label_categorical)
                    + len(ohe_categorical)
                )
            )

            # -------------------------------------------------
            # SMOTENC
            # -------------------------------------------------

            smote = SMOTENC(
                categorical_features=categorical_indices,
                random_state=42
            )

            # -------------------------------------------------
            # Post-SMOTENC preprocessing
            # -------------------------------------------------

            postprocessor = ColumnTransformer(
                transformers=[
                    (
                        'num',
                        StandardScaler(),
                        list(range(numerical_count))
                    ),

                    (
                        'cat_label',
                        OneHotEncoder(
                            handle_unknown='ignore'
                        ),
                        list(
                            range(
                                numerical_count,
                                numerical_count
                                + len(label_categorical)
                            )
                        )
                    ),

                    (
                        'cat_ohe',
                        OneHotEncoder(
                            handle_unknown='ignore'
                        ),
                        list(
                            range(
                                numerical_count
                                + len(label_categorical),
                                numerical_count
                                + len(label_categorical)
                                + len(ohe_categorical)
                            )
                        )
                    )
                ]
            )

            logging.info("Preprocessing pipelines created successfully")

            return (
                preprocessor,
                smote,
                postprocessor,
                X_train,
                X_test,
                y_train,
                y_test
            )

        except Exception as e:
            raise CustomException(e, sys)


"""
CORRECTIONS MADE:

1. Fixed the ColumnTransformer syntax by using the transformers=[] list.

2. Removed OneHotEncoder from the preprocessing performed before SMOTENC.

3. Categorical features are first imputed and ordinal encoded so that
   SMOTENC can correctly identify and process categorical columns.

4. Correct categorical indices are calculated based on the transformed
   feature matrix rather than using X_train.columns.get_loc().

5. SMOTENC is applied only to the training data.

6. A second ColumnTransformer (postprocessor) performs:
       - StandardScaler on numerical features
       - OneHotEncoder on categorical features

7. This prevents the original categorical indices from becoming invalid
   because of OneHotEncoder expansion before SMOTENC.

8. The train/test split is performed only once inside this pipeline.

9. The resulting objects are returned to model_trainer.py so that model
   training can use the resampled training data and untouched test data.
"""