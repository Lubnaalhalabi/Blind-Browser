import numpy as np
import matplotlib.pyplot as plt
import onnxruntime
import torch
import warnings
from segment_anything import sam_model_registry, SamPredictor
from segment_anything.utils.onnx import SamOnnxModel
from scipy.ndimage import label

# Class for SAM segmentation
class SamSegmentation:
    def __init__(self, checkpoint, model_type="vit_h"):
        """
        Initialize the SamSegmentation with a model checkpoint and type.

        Parameters:
        checkpoint (str): Path to the model checkpoint.
        model_type (str): Type of the model to be used. Default is "vit_h".
        """
        self.sam = sam_model_registry[model_type](checkpoint=checkpoint)
        self.sam.to(device='cpu')  # Set the model to use CPU
        self.predictor = SamPredictor(self.sam)
        self.ort_session = None  # Initialize the ONNX runtime session to None

    def load_onnx_model(self, onnx_model_path):
        """
        Load an ONNX model for inference.

        Parameters:
        onnx_model_path (str): Path to the ONNX model file.
        """
        self.ort_session = onnxruntime.InferenceSession(onnx_model_path)

    def export_to_onnx(self, onnx_model_path):
        """
        Export the current model to ONNX format.

        Parameters:
        onnx_model_path (str): Path where the ONNX model will be saved.
        """
        onnx_model = SamOnnxModel(self.sam, return_single_mask=True)
        dynamic_axes = {
            "point_coords": {1: "num_points"},
            "point_labels": {1: "num_points"},
        }
        embed_dim = self.sam.prompt_encoder.embed_dim
        embed_size = self.sam.prompt_encoder.image_embedding_size
        mask_input_size = [4 * x for x in embed_size]

        # Create dummy inputs for the ONNX export
        dummy_inputs = {
            "image_embeddings": torch.randn(1, embed_dim, *embed_size, dtype=torch.float),
            "point_coords": torch.randint(low=0, high=1024, size=(1, 5, 2), dtype=torch.float),
            "point_labels": torch.randint(low=0, high=4, size=(1, 5), dtype=torch.float),
            "mask_input": torch.randn(1, 1, *mask_input_size, dtype=torch.float),
            "has_mask_input": torch.tensor([1], dtype=torch.float),
            "orig_im_size": torch.tensor([1500, 2250], dtype=torch.float),
        }
        output_names = ["masks", "iou_predictions", "low_res_masks"]

        # Suppress warnings during the export
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=torch.jit.TracerWarning)
            warnings.filterwarnings("ignore", category=UserWarning)
            # Export the model to ONNX format
            with open(onnx_model_path, "wb") as f:
                torch.onnx.export(
                    onnx_model,
                    tuple(dummy_inputs.values()),
                    f,
                    export_params=True,
                    verbose=False,
                    opset_version=17,
                    do_constant_folding=True,
                    input_names=list(dummy_inputs.keys()),
                    output_names=output_names,
                    dynamic_axes=dynamic_axes,
                )

    def segment_image(self, image, cluster_centers):
        """
        Segment an image using the SAM model and provided cluster centers.

        Parameters:
        image (numpy.ndarray): The input image to be segmented.
        cluster_centers (list): List of cluster center coordinates.

        Returns:
        numpy.ndarray: The binary mask of the segmented image.
        """
        self.predictor.set_image(image)
        image_embedding = self.predictor.get_image_embedding().cpu().numpy()

        input_point = cluster_centers
        input_label = np.ones(len(input_point))

        # Prepare inputs for ONNX model
        onnx_coord = np.concatenate([input_point, np.array([[0.0, 0.0]])], axis=0)[None, :, :]
        onnx_label = np.concatenate([input_label, np.array([-1])], axis=0)[None, :].astype(np.float32)
        onnx_coord = self.predictor.transform.apply_coords(onnx_coord, image.shape[:2]).astype(np.float32)
        onnx_mask_input = np.zeros((1, 1, 256, 256), dtype=np.float32)
        onnx_has_mask_input = np.zeros(1, dtype=np.float32)

        ort_inputs = {
            "image_embeddings": image_embedding,
            "point_coords": onnx_coord,
            "point_labels": onnx_label,
            "mask_input": onnx_mask_input,
            "has_mask_input": onnx_has_mask_input,
            "orig_im_size": np.array(image.shape[:2], dtype=np.float32)
        }

        # Run inference using ONNX runtime session
        masks, _, low_res_logits = self.ort_session.run(None, ort_inputs)
        masks = masks > self.predictor.model.mask_threshold
        return masks

    def calculate_remaining_clusters(self, mask):
        """
        Calculate remaining clusters after filtering out small components.

        Parameters:
        mask (numpy.ndarray): The binary mask of the segmented image.

        Returns:
        tuple: A tuple containing:
            - filtered_mask (numpy.ndarray): The binary mask after filtering.
            - remaining_pieces (int): The number of remaining clusters.
        """
        labeled_mask, num_pieces = label(mask)
        area_threshold = 2000  # Specify the threshold area here

        # Filter out small components
        for component in range(1, num_pieces + 1):
            component_mask = labeled_mask == component
            if np.sum(component_mask) < area_threshold:
                labeled_mask[component_mask] = 0

        filtered_mask = labeled_mask > 0
        _, remaining_pieces = label(filtered_mask)
        return filtered_mask, remaining_pieces

    def show_mask(self, mask, ax):
        """
        Display a binary mask on an axis.

        Parameters:
        mask (numpy.ndarray): The binary mask to be displayed.
        ax (matplotlib.axes.Axes): The axis on which to display the mask.
        """
        color = np.array([0, 0, 0, 0.9])  # RGBA color for the mask
        h, w = mask.shape[-2:]
        mask_image = mask.reshape(h, w, 1) * color.reshape(1, 1, -1) * 255
        mask_image = mask_image.astype(np.uint8)
        ax.imshow(mask_image)

    def show_results(self, image, masks, cluster_centers, saving_path):
        """
        Show and save the results of segmentation.

        Parameters:
        image (numpy.ndarray): The input image.
        masks (numpy.ndarray): The binary mask of the segmented image.
        cluster_centers (list): List of cluster center coordinates.
        saving_path (str): Path where the result image will be saved.
        """
        plt.figure(figsize=(75,75))
        plt.imshow(image)
        filtered_mask, _ = self.calculate_remaining_clusters(masks)
        self.show_mask(filtered_mask, plt.gca())
        plt.axis('off')
        plt.savefig(saving_path)
        #plt.show()
        plt.close()