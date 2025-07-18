import torch
from abc import ABCMeta, abstractmethod
from lightx2v.utils.registry_factory import CONV2D_WEIGHT_REGISTER


class Conv2dWeightTemplate(metaclass=ABCMeta):
    def __init__(self, weight_name, bias_name, stride, padding, dilation, groups):
        self.weight_name = weight_name
        self.bias_name = bias_name
        self.stride = stride
        self.padding = padding
        self.dilation = dilation
        self.groups = groups
        self.config = {}

    @abstractmethod
    def load(self, weight_dict):
        pass

    @abstractmethod
    def apply(self, input_tensor):
        pass

    def set_config(self, config=None):
        if config is not None:
            self.config = config


@CONV2D_WEIGHT_REGISTER("Default")
class Conv2dWeight(Conv2dWeightTemplate):
    def __init__(self, weight_name, bias_name, stride=1, padding=0, dilation=1, groups=1):
        super().__init__(weight_name, bias_name, stride, padding, dilation, groups)

    def load(self, weight_dict):
        self.weight = weight_dict[self.weight_name].cuda()
        self.bias = weight_dict[self.bias_name].cuda() if self.bias_name is not None else None

    def apply(self, input_tensor):
        input_tensor = torch.nn.functional.conv2d(input_tensor, weight=self.weight, bias=self.bias, stride=self.stride, padding=self.padding, dilation=self.dilation, groups=self.groups)
        return input_tensor

    def to_cpu(self, non_blocking=False):
        self.weight = self.weight.cpu(non_blocking=non_blocking)
        if self.bias is not None:
            self.bias = self.bias.cpu(non_blocking=non_blocking)

    def to_cuda(self, non_blocking=False):
        self.weight = self.weight.cuda(non_blocking=non_blocking)
        if self.bias is not None:
            self.bias = self.bias.cuda(non_blocking=non_blocking)

    def state_dict(self, destination=None):
        if destination is None:
            destination = {}
        destination[self.weight_name] = self.weight.cpu().detach().clone()
        if self.bias is not None:
            destination[self.bias_name] = self.bias.cpu().detach().clone()
        return destination

    def clear(self):
        attrs = ["weight", "bias", "pinned_weight", "pinned_bias"]
        for attr in attrs:
            if hasattr(self, attr):
                delattr(self, attr)
                setattr(self, attr, None)
