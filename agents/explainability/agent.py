import torch
import numpy as np
import cv2
from PIL import Image


class ExplainabilityAgent:
    def __init__(self):
        self.method = "gradcam"

    def generate_heatmap(
        self, model: torch.nn.Module, image: Image.Image, target_class: int
    ) -> np.ndarray:
        heatmap = self._gradcam(model, image, target_class)
        overlay = self._overlay_heatmap(np.array(image), heatmap)
        return overlay

    def _gradcam(
        self, model: torch.nn.Module, image: Image.Image, target_class: int
    ) -> np.ndarray:
        model.eval()
        input_tensor = self._preprocess(image).unsqueeze(0)

        features = None
        gradients = None

        def forward_hook(module, input, output):
            nonlocal features
            features = output

        def backward_hook(module, grad_input, grad_output):
            nonlocal gradients
            gradients = grad_output[0]

        target_layer = self._find_target_layer(model)
        handle_forward = target_layer.register_forward_hook(forward_hook)
        handle_backward = target_layer.register_full_backward_hook(backward_hook)

        output = model(input_tensor)
        model.zero_grad()
        output[0, target_class].backward()

        handle_forward.remove()
        handle_backward.remove()

        weights = gradients.mean(dim=(2, 3), keepdim=True)
        cam = (weights * features).sum(dim=1).squeeze()
        cam = torch.relu(cam)
        cam = cam.detach().numpy()
        cam = cv2.resize(cam, (image.width, image.height))
        cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
        return cam

    def _overlay_heatmap(
        self, image: np.ndarray, heatmap: np.ndarray
    ) -> np.ndarray:
        heatmap_colored = cv2.applyColorMap(
            (heatmap * 255).astype(np.uint8), cv2.COLORMAP_JET
        )
        overlay = cv2.addWeighted(image, 0.6, heatmap_colored, 0.4, 0)
        return overlay

    def _find_target_layer(self, model: torch.nn.Module) -> torch.nn.Module:
        for name, module in model.named_modules():
            if isinstance(module, torch.nn.Conv2d):
                last_conv = module
        return last_conv

    def _preprocess(self, image: Image.Image) -> torch.Tensor:
        from torchvision import transforms
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ])
        return transform(image)
