#! /usr/env python3

"""
Radar chart (aka spider or star chart)

This example creates a radar chart, also known as a spider or star chart [1]_.

Although this example allows a frame of either 'circle' or 'polygon', polygon
frames don't have proper gridlines (the lines are circles instead of polygons).
It's possible to get a polygon grid by setting GRIDLINE_INTERPOLATION_STEPS in
matplotlib.axis to the desired number of vertices, but the orientation of the
polygon is not aligned with the radial axes.
"""
import numpy as np
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
import re
from matplotlib.path import Path
from matplotlib.spines import Spine
from matplotlib.projections.polar import PolarAxes
from matplotlib.projections import register_projection
import os


def radar_factory(num_vars, frame="circle"):
    """Create a radar chart with `num_vars` axes.

    This function creates a RadarAxes projection and registers it.

    Parameters
    ----------
    num_vars : int
        Number of variables for radar chart.
    frame : {'circle' | 'polygon'}
        Shape of frame surrounding axes.

    """
    # calculate evenly-spaced axis angles
    theta = np.linspace(0, 2 * np.pi, num_vars, endpoint=False)

    def draw_poly_patch(self):
        # rotate theta such that the first axis is at the top
        verts = unit_poly_verts(theta + np.pi / 2)
        return plt.Polygon(verts, closed=True, edgecolor="k")

    def draw_circle_patch(self):
        # unit circle centered on (0.5, 0.5)
        return plt.Circle((0.5, 0.5), 0.5)

    patch_dict = {"polygon": draw_poly_patch, "circle": draw_circle_patch}
    if frame not in patch_dict:
        raise ValueError("unknown value for `frame`: %s" % frame)

    class RadarAxes(PolarAxes):

        name = "radar"
        # use 1 line segment to connect specified points
        RESOLUTION = 1
        # define draw_frame method
        draw_patch = patch_dict[frame]

        def __init__(self, *args, **kwargs):
            super(RadarAxes, self).__init__(*args, **kwargs)
            # rotate plot such that the first axis is at the top
            self.set_theta_zero_location("N")

        def fill(self, *args, **kwargs):
            """Override fill so that line is closed by default"""
            closed = kwargs.pop("closed", True)
            return super(RadarAxes, self).fill(closed=closed, *args, **kwargs)

        def plot(self, *args, **kwargs):
            """Override plot so that line is closed by default"""
            lines = super(RadarAxes, self).plot(*args, **kwargs)
            for line in lines:
                self._close_line(line)

        def _close_line(self, line):
            x, y = line.get_data()
            # FIXME: markers at x[0], y[0] get doubled-up
            if x[0] != x[-1]:
                x = np.concatenate((x, [x[0]]))
                y = np.concatenate((y, [y[0]]))
                line.set_data(x, y)

        def set_varlabels(self, labels):
            self.set_thetagrids(np.degrees(theta), labels)

        def _gen_axes_patch(self):
            return self.draw_patch()

        def _gen_axes_spines(self):
            if frame == "circle":
                return PolarAxes._gen_axes_spines(self)
            # The following is a hack to get the spines (i.e. the axes frame)
            # to draw correctly for a polygon frame.

            # spine_type must be 'left', 'right', 'top', 'bottom', or `circle`.
            spine_type = "circle"
            verts = unit_poly_verts(theta + np.pi / 2)
            # close off polygon by repeating first vertex
            verts.append(verts[0])
            path = Path(verts)

            spine = Spine(self, spine_type, path)
            spine.set_transform(self.transAxes)
            return {"polar": spine}

    register_projection(RadarAxes)
    return theta


def unit_poly_verts(theta):
    """
    Return vertices of polygon for subplot axes.
    This polygon is circumscribed by a unit circle centered at (0.5, 0.5)
    """
    x0, y0, r = [0.5] * 3
    verts = [(r * np.cos(t) + x0, r * np.sin(t) + y0) for t in theta]
    return verts


class DataProcessor:
    """ Load source data and provide preprocessing for graphing
    """

    def __init__(self):
        self.file = "DMR Table.csv"
        self.dmr = pd.read_csv(self.file)

    def reshape_table(self,):
        """ End the madness that is the CSV. Transpose date columns to row values
        """
        # Remove blank columns
        valid_columns = [key for key in self.dmr.keys() if "Unnamed" not in key]
        self.dmr = self.dmr[valid_columns]
        cols = self.dmr.columns
        dates = [re.findall("(?<=TO ).*", i)[0] for i in cols[4:]]
        dates = [
            i.replace("29", "28") for i in dates
        ]  # Leap year is a problem, apparently
        cols = list(cols[:4]) + list(dates)
        self.dmr.columns = cols
        ##        parameters = self.dmr['PARAMETER'].unique()
        ##        locations = self.dmr[self.dmr.columns[0]].unique()
        self.dmr = pd.melt(
            self.dmr, id_vars=self.dmr.columns[:4], var_name="Date", value_name="Value"
        )
        self.dmr["Date"] = pd.to_datetime(
            self.dmr["Date"], format="%m/%d/%Y"
        )  # Dates are now DTG
        self.dmr["Value"] = pd.to_numeric(self.dmr["Value"], errors="coerce")
        ##        return locations,parameters
        return None

    def simplify_names(self,):
        """Replace long strings with short, intuitive names. Rename some columns
        """

        lexicon = {
            "SELENIUM, TOTAL RECOVERABLE (NO LONGER REQUIRED 9/1/2005)": "Se",
            "BERYLLIUM, (BE) TOTAL RECOVERABLE (NO LONGER REQUIRED 9/1/2005)": "Be",
            "NICKEL, TOTAL RECOVERABLE  (NO LONGER REQUIRED 9/1/2005)": "Ni",
            "CHROMIUM, TOTAL RECOVERABLE  (NO LONGER REQUIRED 9/1/2005)": "Cr",
            "MERCURY, TOTAL RECOVERABLE  (NO LONGER REQUIRED 9/1/2005)": "Hg",
            "CYANIDE, TOTAL  (NO LONGER REQUIRED 9/1/2005)": "Cyanide",
            "BOD, 5 DAY": "BOD",
            "PH": "pH",
            "SOLIDS, TOTAL SUSPENDED": "TSS",
            "OIL & GREASE": "Oil",
            "NITROGEN, TOTAL": "N",
            "NITROGEN, KJELDAHL  (NO LONGER REQUIRED 12-2013)": "N, Kjeldahl",
            "PHOSPHORUS, DISSOLVED": "P",
            "HARDNESS (CACO3) TOTAL": "CaCO3",
            "SILVER, TOTAL RECOVERABLE": "Ag",
            "ZINC, TOTAL RECOVERABLE": "Zn",
            "CADMIUM, TOTAL RECOVERABLE": "Cd",
            "LEAD, TOTAL RECOVERABLE": "Pb",
            "COPPER, TOTAL RECOVERABLE": "Cu",
            "FLOW IN CONDUIT / THRU TREAT. PLANT": "Flow",
            "SOLIDS, TOTAL DISSOLVED": "TDS",
            "STREPTOCOCCI, FECAL MATERIAL": "Streptococci",
            "E.COLI  (CHANGED FROM COLIFORM, FECAL 8/31/2005)": "E.Coli",
            "BOD, CARBONACEOUS 5 DAY (NO LONGER REQUIRED 12-2013)": "BOD, C",
        }
        tmp_param = self.dmr["PARAMETER"]
        for l in lexicon.keys():
            self.dmr.loc[self.dmr.PARAMETER == l, "PARAMETER"] = lexicon[l]
        # Rename columns
        self.dmr.columns = [
            "Location",
            "Parameter",
            "Unit",
            "Frequency",
            "Date",
            "Value",
        ]
        return None

    def get_base_limits(self):
        """ Assume the 95th percentile for all data is a valid upper limit where
        EPA quality limits are not established.
        """
        parameters = self.dmr["Parameter"].unique()
        base_limits = {}
        for p in parameters:
            base_limits[p] = self.dmr["Value"][self.dmr["Parameter"] == p].quantile(
                q=0.95
            )
        return base_limits

    def gen_limits(self, hardness):
        """ Acceptable limits of metals are hardness specific. Create a dictionary of
        upper limits based on AR WQS guidance
        """
        limits = {}
        # Overwrite with hard values where applicable
        limits["pH"] = 9  # Min is 6. Not an obvious way to make this happen
        limits["N"] = 0.69  # EPA Ecoregional
        limits["P"] = 0.05  # EPA Ecoregional
        limits["Cr"] = np.e ** (0.819 * np.log(hardness) + 3.688) * 0.316
        limits["Cu"] = np.e ** (0.9422 * np.log(hardness) - 1.464) * 0.960
        limits["Pb"] = np.e ** (1.273 * np.log(hardness) - 1.460) * (
            1.46203 - np.log(hardness) * 0.145712
        )
        limits["Hg"] = 2.4 * 0.85
        limits["Ni"] = np.e ** (0.8460 * np.log(hardness) + 3.3612) * 0.998
        limits["Se"] = 20
        limits["Ag"] = np.e ** (1.72 * np.log(hardness) - 6.52) * 0.85
        limits["Zn"] = np.e ** (0.8473 * np.log(hardness) + 0.8604) * 0.978
        limits["Cd"] = np.e ** (1.28 * np.log(hardness) - 3.828) * (
            1.36672 - np.log(hardness) * 0.041838
        )
        limits["E.Coli"] = 410
        limits["Streptococci"] = 400
        limits["Cyanide"] = 22.36
        limits["TDS"] = 103  # This is reference only. Little Fource: 179mg/L
        limits["Oil"] = 15
        return limits

    def normalize(self,):
        """ Scale all values to their 95th percentile or EPA maximum limit.
        We are not considering lognormal or other distribution inappropriate
        for this type of scaling.
        """
        base_limits = self.get_base_limits()
        locations = self.dmr["Location"].unique()
        dates = self.dmr["Date"].unique()
        for d in dates:
            for l in locations:
                results = self.dmr[
                    (self.dmr["Location"] == l) & (self.dmr["Date"] == d)
                ]
                hardness = float(results["Value"][results["Parameter"] == "CaCO3"])
                # Convert to float to avoid baggage
                limits = self.gen_limits(hardness)
                params = results["Parameter"]
                for p in params:
                    if p in limits.keys():
                        upper_limit = limits[p]
                    else:
                        upper_limit = base_limits[p]
                    newval = (
                        results.loc[results.Parameter == p, "Value"] * 1.0 / upper_limit
                    )
                    self.dmr.loc[
                        (self.dmr["Location"] == l)
                        & (self.dmr["Date"] == d)
                        & (self.dmr["Parameter"] == p),
                        "Value",
                    ] = newval
        return None

    def format_out(self, start, end=datetime.now()):
        """ Return a list object in a format that lends itself to not having
        to rewrite any of the radar graph code that I'm using. For expedience.
        """

        target_params = [
            "Flow",
            "BOD",
            "pH",
            "TSS",
            "TDS",
            "Oil",
            "N",
            "P",
            "CaCO3",
            "Ag",
            "Zn",
            "Cd",
            "Pb",
            "Cu",
            "Streptococci",
            "E.Coli",
        ]
        data = self.dmr[(self.dmr["Date"] >= start) & (self.dmr["Date"] <= end)]
        locations = data["Location"].unique()
        outlist = [target_params]
        quarters = pd.to_datetime(data["Date"].unique())
        for q in quarters:
            results = []
            for l in locations:
                values = []
                for p in target_params:
                    values.append(
                        float(
                            data["Value"][
                                (data["Date"] == q)
                                & (data["Location"] == l)
                                & (data["Parameter"] == p)
                            ]
                        )
                    )
                results.append(values)
            outlist.append(("{0}/{1}".format(q.month, q.year), results))
        return outlist


if __name__ == "__main__":
    N = 16
    theta = radar_factory(N, frame="polygon")
    if not os.path.isfile("output list"):
        # Data prep
        D = DataProcessor()
        D.reshape_table()
        D.simplify_names()
        D.normalize()
        start = datetime(2017, 3, 1)
        outlist = D.format_out(start)
        data = outlist
        with open("output list", "wb") as outfile:
            pickle.dump(outlist, outfile)
    else:
        with open("output list", "rb") as infile:
            data = pickle.load(infile)

    spoke_labels = data.pop(0)

    fig, axes = plt.subplots(
        figsize=(9, 9), nrows=2, ncols=2, subplot_kw=dict(projection="radar")
    )
    fig.subplots_adjust(wspace=0.25, hspace=0.20, top=0.85, bottom=0.05)

    colors = ["b", "r", "g", "m", "y"]
    # Plot the four cases from the example data on separate axes
    for ax, (title, case_data) in zip(axes.flatten(), data):
        grids = ax.set_rgrids([0.25, 0.5, 0.75, 1, 1.25])
        grids[0][3].set_lw(2)
        grids[0][3].set_c("r")
        grids[0][3].set_ls("dashed")
        ax.set_ylim(0, 1.5)
        ax.set_title(
            title,
            weight="bold",
            size="medium",
            position=(0.5, 1.1),
            horizontalalignment="center",
            verticalalignment="center",
        )
        for d, color in zip(case_data, colors):
            ax.plot(theta, d, color=color)
            ax.fill(theta, d, facecolor=color, alpha=0.25)
        ax.set_varlabels(spoke_labels)

    # add legend relative to top-left plot
    ax = axes[0, 0]
    labels = ("Outfall 1", "Outfall 2", "Outfall 3", "Outfall 6", "Outfall 5")
    legend = ax.legend(labels, loc=(0.9, 0.95), labelspacing=0.1, fontsize="small")

    fig.text(
        0.5,
        0.965,
        "Water Quality Parameters For 2017",
        horizontalalignment="center",
        color="black",
        weight="bold",
        size="large",
    )

    plt.savefig("test-1.png")
