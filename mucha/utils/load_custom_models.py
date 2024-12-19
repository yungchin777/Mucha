import importlib
import os
from . import custom_models
from torchvision.models._api import list_models, get_model

def load_model_from_config(model_name, config, pretrained=False):
    model_category = getattr(custom_models, model_name, None)

    if model_category:
        params = config.get("params", {})
        return model_category(**params)   

    available_models = list_models()

    # list default model in pytorch
    if model_name in available_models:
        print(f"Loading torchvision model: {model_name}")
        weights = "DEFAULT" if pretrained else None
        return get_model(model_name, weights=weights)

    # model is not exist
    raise ValueError(
        f"Model '{model_name}' is not available.\n"
        "Available models:\n"
        f"{available_models}"
    )
