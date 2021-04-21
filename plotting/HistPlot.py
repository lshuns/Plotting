# @Author: lshuns
# @Date:   2021-04-01, 21:04:38
# @Last modified by:   lshuns
# @Last modified time: 2021-04-21, 22:45:45

### everything about histogram

__all__ = ["HistPlotFunc", "Hist2DPlotFunc", "HistPlotFunc_subplots"]

import math
import logging

import numpy as np

import matplotlib as mpl
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = True
mpl.rcParams['ytick.right'] = True

import matplotlib.pyplot as plt

from matplotlib.ticker import AutoMinorLocator, LogLocator

from .CommonInternal import _vhlines

logging.basicConfig(format='%(name)s : %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def HistPlotFunc(outpath,
                paras, wgs, COLORs, LABELs,
                nbins, XRANGE, YRANGE=None,
                XLABEL=None, YLABEL=None,
                DENSITY=False, HISTTYPE='step', STACKED=False,
                TITLE=None, xtick_min_label=True, ytick_min_label=True,
                vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                xlog=False, ylog=False,
                loc_legend='best'):
    """
    Histogram plot for multiple parameters
    """

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    if DENSITY and (wgs is not None):
        logger.warning('DENSITY and wgs are provided simultaneously!!!')

    fig, ax = plt.subplots()
    if xlog:
        logbins = np.logspace(np.log10(XRANGE[0]), np.log10(XRANGE[1]), nbins)
        plt.hist(x=paras, bins=logbins, density=DENSITY, weights=wgs, color=COLORs, label=LABELs, histtype=HISTTYPE, stacked=STACKED)
    else:
        plt.hist(x=paras, bins=nbins, range=XRANGE, density=DENSITY, weights=wgs, color=COLORs, label=LABELs, histtype=HISTTYPE, stacked=STACKED)

    plt.xlim(XRANGE[0], XRANGE[1])
    if YRANGE is not None:
        plt.ylim(YRANGE[0], YRANGE[1])

    if xlog:
        plt.xscale('log')
    if ylog:
        plt.yscale('log')

    if vlines is not None:
        _vhlines('v', vlines, line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths)

    if hlines is not None:
        _vhlines('h', hlines, line_styles=hline_styles, line_colors=hline_colors, line_labels=hline_labels, line_widths=hline_widths)

    if xtick_min_label:
        if xlog:
            ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax.xaxis.set_minor_locator(AutoMinorLocator())
    if ytick_min_label:
        if ylog:
            ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
        else:
            ax.yaxis.set_minor_locator(AutoMinorLocator())

    if LABELs is not None:
        plt.legend(frameon=False, loc=loc_legend)
    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    if TITLE is not None:
        plt.title(TITLE)

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Histogram plot saved as", outpath)

def Hist2DPlotFunc(outpath,
                x_val, y_val, wg,
                nbins, XRANGE=None, YRANGE=None,
                XLABEL=None, YLABEL=None, CBAR_LABEL=None,
                COLOR_MAP='Reds',
                DENSITY=False, count_scale=[None, None], count_log=False,
                TITLE=None, xtick_min_label=True, ytick_min_label=True,
                vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None):
    """
    2D histogram plot
    """

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    if DENSITY and (wg is not None):
        logger.warning('DENSITY and wgs are provided simultaneously!!!')

    if (XRANGE is not None) and (YRANGE is not None):
        SRANGE = [[XRANGE[0], XRANGE[1]], [YRANGE[0], YRANGE[1]]]
    else:
        SRANGE = None

    fig, ax = plt.subplots()
    if count_log:
        norm = mpl.colors.LogNorm(vmin=count_scale[0], vmax=count_scale[1])
    else:
        norm = mpl.colors.Normalize(vmin=count_scale[0], vmax=count_scale[1])
    h = plt.hist2d(x_val, y_val, bins=nbins, range=SRANGE, density=DENSITY, weights=wg, cmin=count_scale[0], cmax=count_scale[1], norm=norm, cmap=COLOR_MAP)
    cbar = plt.colorbar(h[3])

    if CBAR_LABEL is not None:
        cbar.ax.set_ylabel(CBAR_LABEL, rotation=270)

    if XRANGE is not None:
        plt.xlim(XRANGE[0], XRANGE[1])
    if YRANGE is not None:
        plt.ylim(YRANGE[0], YRANGE[1])

    if vlines is not None:
        _vhlines('v', vlines, line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths)

    if hlines is not None:
        _vhlines('h', hlines, line_styles=hline_styles, line_colors=hline_colors, line_labels=hline_labels, line_widths=hline_widths)

    if xtick_min_label:
        ax.xaxis.set_minor_locator(AutoMinorLocator())
    if ytick_min_label:
        ax.yaxis.set_minor_locator(AutoMinorLocator())

    plt.xlabel(XLABEL)
    plt.ylabel(YLABEL)
    if TITLE is not None:
        plt.title(TITLE)

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("2D histogram plot saved as", outpath)

def HistPlotFunc_subplots(outpath, N_plots,
                            paras_list, wgs_list, COLORs_list, LABELs_list,
                            nbins_list, XRANGE, YRANGE=None,
                            subLABEL_list=None, subLABEL_locX=0.1, subLABEL_locY=0.8,
                            XLABEL=None, YLABEL=None,
                            DENSITY=False, HISTTYPE='step', STACKED=False,
                            TITLE=None, xtick_min_label=True, ytick_min_label=True,
                            vlines=None, vline_styles=None, vline_colors=None, vline_labels=None, vline_widths=None,
                            hlines=None, hline_styles=None, hline_colors=None, hline_labels=None, hline_widths=None,
                            xlog=False, ylog=False,
                            loc_legend='best'):
    """
    Histogram plot for multiple subplots
    """

    if outpath != 'show':
        backend_orig = plt.get_backend()
        plt.switch_backend("agg")

    N_rows = math.ceil(N_plots**0.5)
    N_cols = math.ceil(N_plots/N_rows)
    fig, axs = plt.subplots(N_rows, N_cols, sharex=True, sharey=True)
    fig.subplots_adjust(hspace=0)
    fig.subplots_adjust(wspace=0)

    if DENSITY and (wgs_list is not None):
        logger.warning('DENSITY and wgs are provided simultaneously!!!')

    i_plot = 0
    for i_row in range(N_rows):
        for i_col in range(N_cols):
            if i_plot >= N_plots:
                if N_rows == 1:
                    axs[i_col].axis('off')
                elif N_cols == 1:
                    axs[i_row].axis('off')
                else:
                    axs[i_row, i_col].axis('off')
            else:
                if N_rows == 1:
                    ax = axs[i_col]
                elif N_cols == 1:
                    ax = axs[i_row]
                else:
                    ax = axs[i_row, i_col]

                paras = paras_list[i_plot]
                COLORs = COLORs_list[i_plot]
                if LABELs_list is not None:
                    LABELs = LABELs_list[i_plot]
                else:
                    LABELs = None

                nbins = nbins_list[i_plot]
                if wgs_list is not None:
                    wgs = wgs_list[i_plot]
                else:
                    wgs = None

                if xlog:
                    logbins = np.logspace(np.log10(XRANGE[0]), np.log10(XRANGE[1]), nbins)
                    ax.hist(x=paras, bins=logbins, density=DENSITY, weights=wgs, color=COLORs, label=LABELs, histtype=HISTTYPE, stacked=STACKED)
                else:
                    ax.hist(x=paras, bins=nbins, range=XRANGE, density=DENSITY, weights=wgs, color=COLORs, label=LABELs, histtype=HISTTYPE, stacked=STACKED)

                if (i_plot == 0) and (LABELs is not None):
                    ax.legend(frameon=False, loc=loc_legend)

                if subLABEL_list is not None:
                    LABEL = subLABEL_list[i_plot]
                    ax.text(subLABEL_locX, subLABEL_locY, LABEL, transform=ax.transAxes)

                ax.set_xlim(XRANGE[0], XRANGE[1])
                if YRANGE is not None:
                    ax.set_ylim(YRANGE[0], YRANGE[1])

                if xlog:
                    ax.set_xscale('log')
                if ylog:
                    ax.set_yscale('log')

                if vlines is not None:
                    _vhlines('v', vlines, line_styles=vline_styles, line_colors=vline_colors, line_labels=vline_labels, line_widths=vline_widths, ax=ax)

                if hlines is not None:
                    _vhlines('h', hlines, line_styles=hline_styles, line_colors=hline_colors, line_labels=hline_labels, line_widths=hline_widths, ax=ax)

                if xtick_min_label:
                    if xlog:
                        ax.xaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
                    else:
                        ax.xaxis.set_minor_locator(AutoMinorLocator())
                if ytick_min_label:
                    if ylog:
                        ax.yaxis.set_minor_locator(LogLocator(base=10.0, subs=None, numticks=10))
                    else:
                        ax.yaxis.set_minor_locator(AutoMinorLocator())
            i_plot +=1

    fig.text(0.5, 0.04, XLABEL, ha='center')
    fig.text(0.04, 0.5, YLABEL, va='center', rotation='vertical')

    if TITLE is not None:
        fig.text(0.5, 0.90, TITLE, ha='center')

    if outpath == 'show':
        plt.show()
        plt.close()
    else:
        plt.savefig(outpath, dpi=300)
        plt.close()
        plt.switch_backend(backend_orig)
        print("Histogram plot saved as", outpath)
