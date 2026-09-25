from src.logger import logging
import sys
import os
import joblib

from src.exception import CustomException

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from src.Components.data_transformation import DataProcessing
from src.Pipeline.train_pipeline import TrainingPipeline


class Model:

    def __init__(self):
        pass

    def train(self):
        """
        Performs preprocessing, SMOTENC resampling, Logistic Regression
        training, evaluation, and saves all required model artifacts.
        """

        try:

            # -------------------------------------------------
            # Create training pipeline
            # -------------------------------------------------

            pipeline = TrainingPipeline()

            (
                preprocessor,
                smote,
                postprocessor,
                X_train,
                X_test,
                y_train,
                y_test
            ) = pipeline.Pipelines()

            # -------------------------------------------------
            # Encode target variable
            # -------------------------------------------------

            data_processing = DataProcessing()

            (
                y_train,
                y_test,
                label_encoder
            ) = data_processing.encode_y(
                y_train,
                y_test
            )

            # -------------------------------------------------
            # Transform X_train
            # -------------------------------------------------

            X_train_processed = preprocessor.fit_transform(
                X_train
            )

            # -------------------------------------------------
            # Apply SMOTENC ONLY on training data
            # -------------------------------------------------

            X_train_resampled, y_train_resampled = smote.fit_resample(
                X_train_processed,
                y_train
            )

            logging.info(
                "SMOTENC resampling completed successfully"
            )

            # -------------------------------------------------
            # Post-SMOTENC preprocessing
            # -------------------------------------------------

            X_train_final = postprocessor.fit_transform(
                X_train_resampled
            )

            # -------------------------------------------------
            # Transform X_test
            # -------------------------------------------------

            X_test_processed = preprocessor.transform(
                X_test
            )

            X_test_final = postprocessor.transform(
                X_test_processed
            )

            # -------------------------------------------------
            # Logistic Regression
            # -------------------------------------------------

            lr_model = LogisticRegression(
                max_iter=2000,
                C=100,
                solver='newton-cholesky',
                random_state=42
            )

            # -------------------------------------------------
            # Train model
            # -------------------------------------------------

            lr_model.fit(
                X_train_final,
                y_train_resampled
            )

            logging.info(
                "Logistic Regression model trained successfully"
            )

            # -------------------------------------------------
            # Prediction
            # -------------------------------------------------

            y_pred = lr_model.predict(
                X_test_final
            )

            # -------------------------------------------------
            # Evaluation
            # -------------------------------------------------

            accuracy = accuracy_score(
                y_test,
                y_pred
            )

            precision = precision_score(
                y_test,
                y_pred,
                average='weighted',
                zero_division=0
            )

            recall = recall_score(
                y_test,
                y_pred,
                average='weighted',
                zero_division=0
            )

            f1 = f1_score(
                y_test,
                y_pred,
                average='weighted',
                zero_division=0
            )

            logging.info(f"Accuracy: {accuracy}")
            logging.info(f"Precision: {precision}")
            logging.info(f"Recall: {recall}")
            logging.info(f"F1 Score: {f1}")

            print("\nClassification Report:")
            print(
                classification_report(
                    y_test,
                    y_pred,
                    zero_division=0
                )
            )

            print("\nConfusion Matrix:")
            print(
                confusion_matrix(
                    y_test,
                    y_pred
                )
            )

            print("\nModel Metrics:")
            print(f"Accuracy  : {accuracy:.4f}")
            print(f"Precision : {precision:.4f}")
            print(f"Recall    : {recall:.4f}")
            print(f"F1 Score  : {f1:.4f}")

            # -------------------------------------------------
            # Create artifacts directory
            # -------------------------------------------------

            project_root = os.path.dirname(
                os.path.dirname(
                    os.path.dirname(
                        os.path.abspath(__file__)
                    )
                )
            )

            artifact_path = os.path.join(
                project_root,
                "artifacts"
            )

            os.makedirs(
                artifact_path,
                exist_ok=True
            )

            # -------------------------------------------------
            # Save Logistic Regression model
            # -------------------------------------------------

            joblib.dump(
                lr_model,
                os.path.join(
                    artifact_path,
                    "model.pkl"
                )
            )

            # -------------------------------------------------
            # Save preprocessor
            # -------------------------------------------------

            joblib.dump(
                preprocessor,
                os.path.join(
                    artifact_path,
                    "preprocessor.pkl"
                )
            )

            # -------------------------------------------------
            # Save postprocessor
            # -------------------------------------------------

            joblib.dump(
                postprocessor,
                os.path.join(
                    artifact_path,
                    "postprocessor.pkl"
                )
            )

            # -------------------------------------------------
            # Save label encoder
            # -------------------------------------------------

            joblib.dump(
                label_encoder,
                os.path.join(
                    artifact_path,
                    "label_encoder.pkl"
                )
            )

            logging.info(
                "All model artifacts saved successfully"
            )

            print("\nModel artifacts saved successfully:")
            print(
                f"Location: {artifact_path}"
            )

            return (
                lr_model,
                preprocessor,
                postprocessor,
                label_encoder
            )

        except Exception as e:
            raise CustomException(e, sys)


"""
CORRECTIONS / ADDITIONS MADE:

1. Added:
       import os
       import joblib

2. Added creation of the artifacts directory:
       artifacts/

3. Added dumping of the trained Logistic Regression model:
       model.pkl

4. Added dumping of the fitted first preprocessor:
       preprocessor.pkl

5. Added dumping of the fitted post-SMOTENC processor:
       postprocessor.pkl

6. Added dumping of the fitted LabelEncoder:
       label_encoder.pkl

7. SMOTENC itself is NOT dumped because it is only required during
   training and is not required for prediction.

8. The model is trained using:
       X_train_final
       y_train_resampled

9. The test set is never passed through SMOTENC.

10. The exact fitted preprocessing objects used during training are
    saved so that predict_pipeline.py can apply the same transformations
    to new input data.

11. The artifact path is calculated automatically from the project
    structure, so the paths do not depend on the current terminal
    directory.
"""