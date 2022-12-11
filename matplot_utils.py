from typing import Union
import typing
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon


class FigCanvas(FigureCanvas):

    def __init__(self, sub_rows: int = 1, sub_cols: int = 1):
        self.plt = plt
        self.num_of_axes = sub_rows * sub_cols

        if self.num_of_axes == 1:
            self.fig, self.axes = self.plt.subplots(sub_rows, sub_cols)
            self._axes = [self.axes]
        elif self.num_of_axes > 1:
            self.fig, self._axes = self.plt.subplots(sub_rows, sub_cols)
            for i, ax in enumerate(self._axes, start=1):
                setattr(self, f'ax{i}', ax)
        else:
            raise Exception('Number of sub rows or sub columns could not be smaller or equal to 0')
        self.set_fig_facecolor()
        self.set_plot_axis_visible(visible=False)

        super(FigCanvas, self).__init__(self.fig)

    def set_fig_facecolor(self, color: str = '#efefef') -> None:
        self.fig.patch.set_facecolor(color)

    def set_axes_facecolor(self, color: str = '#efefef') -> None:
        ax: Axes  # type hinting
        for ax in self._axes:
            ax.set_facecolor(color)

    def set_plot_axis_visible(self, visible: bool) -> None:
        visible = 'on' if visible else 'off'
        self.plt.axis(visible)

    @typing.overload
    def set_fig_subplots_adjust(self, left: float, bottom: float, right: float,
                                top: float, wspace: float, hspace: float) -> None:
        ...

    @typing.overload
    def set_fig_subplots_adjust(self, auto: bool) -> None:
        ...

    def set_fig_subplots_adjust(self, *args: tuple) -> None:
        len_args = len(args)
        #
        if len_args == 0:
            raise Exception('No arguments passed! At least one argument is required.')
        elif len_args == 1:
            arg = args[0]
            if isinstance(arg, bool):
                self.fig.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)
            elif isinstance(arg, Union[float, int]):
                self.fig.subplots_adjust(left=arg)
            else:
                raise TypeError(f'The passed argument should be the type of bool, int or float class not {type(arg)}')
        else:
            for arg in args:
                if not isinstance(arg, Union[float, int]):
                    raise TypeError(f'The passed arguments should be the type of int or float class not {type(arg)}')

            args += (6 - len_args) * (None, )
            #
            left = args[0]
            bottom = args[1]
            right = args[2]
            top = args[3]
            wspace = args[4]
            hspace = args[5]
            #
            self.fig.subplots_adjust(left, bottom, right, top, wspace, hspace)
