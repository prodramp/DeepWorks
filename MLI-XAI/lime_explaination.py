"""
Implementation of Local interpretable model-agnostic explanations.
Source: Ribeiro, Marco Tulio, Sameer Singh, and Carlos Guestrin.
"Why should I trust you?: Explaining the predictions of any classifier."
Proceedings of the 22nd ACM SIGKDD international conference on knowledge
discovery and data mining. ACM (2016).
"""
import tensorflow as tf
import numpy as np
from typing import Tuple
from sklearn.metrics import pairwise_distances
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
import skimage
import matplotlib.pyplot as plt

EXPLAINABLE_MODELS = {
    'linear_regression': LinearRegression,
    'decision_tree_regressor': DecisionTreeRegressor
}


class LIME:

    def __init__(self, image: tf.Tensor, model: tf.keras.Model, random_seed: int = 9):
        """
        Parameters
        ----------
        image: tf.Tensor; Image for which the explanation should be made
        model: tf.keras.Model; Base model
        """
        self.image = image
        self.model = model
        self.random_seed = random_seed
        self.super_pixels, self.super_pixel_count = self.create_super_pixels()
        self.perturbation_vectors = self.generate_pertubation_vectors()

    def create_super_pixels(
            self, kernel_size: int = 8, max_dist: int = 1000, ratio: float = 0.2
    ) -> Tuple[np.ndarray, int]:
        """
        Parameters
        ----------
        kernel_size, max_dist, ratio: parameters for skimage.segmentation.quickshift function.
        See https://scikit-image.org/docs/stable/api/skimage.segmentation.html for more info

        Returns
        -------
        super_pixels: np.ndarray (shape==self.image.shape); Contains
        integers to which super pixel area the location belongs
        super_pixel_count: int; total number of different superpixel areas
        """
        super_pixels = skimage.segmentation.quickshift(
            self.image, kernel_size=kernel_size, max_dist=max_dist, ratio=ratio
        )
        super_pixel_count = len(np.unique(super_pixels))
        return super_pixels, super_pixel_count

    def plot_super_pixel_boundary(self):
        """ Plots the boundaries of the superpixel areas """
        super_pixel_boundaries = skimage.segmentation.mark_boundaries(
            self.image.numpy().astype(int), self.super_pixels
        )
        plt.imshow(super_pixel_boundaries)
        plt.title('Superpixel boundaries')

    def generate_pertubation_vectors(self, num_perturbations: int = 100) -> np.ndarray:
        """
        Generates a number of perturbation vectors. These are binary vectors of length
        num_super_pixels, which define if a superpixel is perturbed

        Parameters
        ----------
        num_perturbations: int; total number of perturbations

        Returns
        -------
        np.ndarray (shape=(num_perturbations, super_pixel_count); binary array defining if a
        superpixel area should be perturbed
        """
        if self.random_seed is not None:
            np.random.seed(self.random_seed)
        return np.random.binomial(1, 0.5, size=(num_perturbations, self.super_pixel_count))

    def predict_perturbed_images(self) -> np.ndarray:
        """
        Generates predictions for all perturbed_images

        Returns
        -------
        np.ndarray (shape=(num_perturbations, num_output_classes)); contains predictions for all
        perturbed images
        """
        perturbed_images = self.create_perturbed_images()
        return self.model(perturbed_images).numpy()

    def create_perturbed_images(self) -> np.ndarray:
        """ Creates perturbed images based on all pertubation vectors """
        self.generate_pertubation_vectors()
        return np.apply_along_axis(
            lambda x: self._create_perturbed_image(x), 1, self.perturbation_vectors
        )

    def _create_perturbed_image(self, perturbation_vector: np.ndarray) -> np.ndarray:
        """
        Creatas a single perturbed image

        Parameters
        ----------
        perturbation_vector; np.ndarray (shape=(num_perturbations, super_pixel_count); binary array
        defining if a superpixel area should be perturbed

        Returns
        -------
        np.ndarray (shape==self.image.shape); contains original image info or perturbed image
        dependent on the perturbation_vector
        """
        perturbation_mask = np.isin(self.super_pixels, np.argwhere(perturbation_vector == 1))
        return np.where(np.expand_dims(perturbation_mask, -1), self.image, 0)

    def plot_perturbed_image(self):
        """ Plots a single perturbed image """
        if self.perturbation_vectors is None:
            self.generate_pertubation_vectors()

        if self.random_seed is not None:
            np.random.seed(self.random_seed)
        idx = np.random.randint(len(self.perturbation_vectors))
        perturbed_img = self._create_perturbed_image(self.perturbation_vectors[idx])

        plt.imshow(perturbed_img.astype(int))
        plt.title('Perturbed Image')

    def calculate_perturbation_weights(self, kernel_width: float = 0.25) -> np.ndarray:
        """
        Calculates the perturbation weights. First the distance between the perturbed images
        and the original image is calculated. A kernel function is used to map these distances
        to weights. The smaller the distance to the original image, the larger the weight. The
        intuition behind this is that if a perturbed image is very close to the original image,
        (let's say only 1 perturbed superpixel area), there is a lot of information in this
        sample, as it tells a lot on the 1 perturbed superpixel area importance.

        Parameters
        ----------
        kernel_width: float; defines the width of the kernel that is used

        Returns
        -------
        np.ndarray (shape=(num_perturbations,)); weights for each perturbation
        """
        non_perturbed_vector = np.ones((1, self.super_pixel_count))
        distances = pairwise_distances(
            self.perturbation_vectors, non_perturbed_vector, metric='cosine'
        )
        return np.squeeze(np.sqrt(np.exp(-(distances ** 2) / kernel_width ** 2)))

    def _fit_explainable_model(
            self,
            predictions: np.ndarray,
            weights: np.ndarray,
            explainable_model_type: str = 'decision_tree_regressor'
    ) -> np.ndarray:
        """
        Function to fit an exmplainable model and define the importance of each superpixel area

        Parameters
        ----------
        predictions: np.ndarray (shape=(num_perturbations, num_output_classes)); contains
        predictions for all perturbed images
        weights: np.ndarray (shape=(num_perturbations,)); weights for each perturbation
        explainable_model_type: str containing the type of explainable model

        Returns
        -------
        feature_importances: np.ndarray (shape=(super_pixel_count,)); importance of each superpixel
        for predicting a specific class
        """
        if explainable_model_type not in EXPLAINABLE_MODELS.keys():
            raise ValueError(
                f"Please specify one of the following model_types: {EXPLAINABLE_MODELS.keys()}"
            )

        model = EXPLAINABLE_MODELS[explainable_model_type]()
        model.fit(X=self.perturbation_vectors, y=predictions, sample_weight=weights)
        if 'regression' in explainable_model_type:
            feature_importance = model.coef_
        elif 'tree' in explainable_model_type:
            feature_importance = model.feature_importances_
        else:
            raise ValueError(
                f"Please specify one of the following model_types: {EXPLAINABLE_MODELS.keys()}"
            )

        return feature_importance

    def plot_explainable_image(self, class_to_explain: int = None, num_superpixels: int = 4,
                               explainable_model_type: str = 'decision_tree_regressor'):
        """
        Plots the most important super pixel areas for predicting a specific class

        Parameters
        ----------
        class_to_explain: int; which class to plot the explanations for. If not specified, will
        default to the class with the highest probability
        num_superpixels: int; defines how many superpixel areas will be plotted
        explainable_model_type: str; which explainable model to use to generate explainability plot
        """
        # get perturbed image predictions & weights
        perturbed_image_predictions = self.predict_perturbed_images()
        weights = self.calculate_perturbation_weights()

        if class_to_explain is None:
            class_to_explain = np.argmax(self.model(np.expand_dims(self.image, 0)).numpy())

        # fit simple interpretable model
        feature_importance = self._fit_explainable_model(
            predictions=perturbed_image_predictions[:, class_to_explain],
            weights=weights,
            explainable_model_type=explainable_model_type
        )

        # Define which superpixel areas should be plotted
        superpixels_to_plot = np.argsort(feature_importance)[-num_superpixels:]
        superpixel_vector = np.zeros(self.super_pixel_count)
        np.put(superpixel_vector, superpixels_to_plot, v=1)

        # Create the image
        perturbed_img = self._create_perturbed_image(superpixel_vector)
        plt.imshow(perturbed_img.astype(int))
        plt.title('LIME explanation')