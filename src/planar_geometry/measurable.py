# -*- coding: utf-8 -*-
"""
planar_geometry/measurable.py

模块: 可计算度量抽象基类
描述: 定义几何元素的抽象基类层次，基于SOLID原则
版本: 0.1.0

功能:
    - Measurable: 可计算度量根抽象类
    - Measurable1D: 可计算长度抽象类
    - Measurable2D: 可计算面积抽象类

依赖:
    - abc: 抽象基类模块
"""

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from planar_geometry.point import Point2D
    from planar_geometry.curve import Curve
    from planar_geometry.surface import Surface


class Measurable(ABC):
    """
    可计算度量的抽象基类

    说明:
        - 所有几何元素的根抽象类
        - 定义度量接口
        - 使用ABC实现抽象基类模式

    设计原则:
        - ISP: 只暴露必要的接口
        - OCP: 扩展通过继承实现，不修改本类
    """

    @abstractmethod
    def __repr__(self) -> str:
        """
        字符串表示

        返回:
            str: 可读的几何元素描述
        """
        pass


class Measurable1D(Measurable, ABC):
    """
    可计算长度的抽象基类

    说明:
        - 继承Measurable
        - 所有具有长度概念的几何元素继承此类
        - 一维几何元素的抽象

    设计原则:
        - SRP: 只负责长度计算

    继承类:
        - Point2D: 零维元素（长度为0）
        - Curve: 一维曲线元素
    """

    @abstractmethod
    def length(self) -> float:
        """
        计算长度

        说明:
            - 抽象方法，由子类实现
            - 返回几何元素的长度值

        返回:
            float: 长度值
        """
        pass


class Measurable2D(Measurable1D, ABC):
    """
    可计算面积的抽象基类

    说明:
        - 继承Measurable1D（二维图形也有周长）
        - 所有具有面积概念的二维几何元素继承此类
        - 二维几何元素的抽象

    设计原则:
        - LSP: 可替换Measurable1D使用

    继承类:
        - Surface: 曲面/平面图形
    """

    @abstractmethod
    def area(self) -> float:
        """
        计算面积

        说明:
            - 抽象方法，由子类实现
            - 返回几何元素的面积值

        返回:
            float: 面积值
        """
        pass

    def length(self) -> float:
        """
        计算长度（周长）

        说明:
            - 二维图形的长度即周长
            - 默认实现调用perimeter()

        返回:
            float: 周长值
        """
        return self.perimeter()

    @abstractmethod
    def perimeter(self) -> float:
        """
        计算周长

        返回:
            float: 周长值
        """
        pass
