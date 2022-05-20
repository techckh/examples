import numpy
import pandas
import geopandas
import seaborn
import contextily
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN


def scatter_plot(df):
    seaborn.jointplot(x='longitude', y='latitude', data=df, s=0.5)


def scatter_plot_with_map(df):
    joint_axes = seaborn.jointplot(
        x='longitude', y='latitude', data=df, s=0.5
    )
    contextily.add_basemap(
        joint_axes.ax_joint,
        crs="EPSG:4326",
        source=contextily.providers.CartoDB.PositronNoLabels
    )


def hexbin(df):
    # Set up figure and axis
    f, ax = plt.subplots(1, figsize=(12, 9))
    # Generate and add hexbin with 50 hexagons in each
    # dimension, no borderlines, half transparency,
    # and the reverse viridis colormap
    hb = ax.hexbin(
        df['x'],
        df['y'],
        gridsize=50,
        linewidths=0,
        alpha=0.5,
        cmap='viridis_r'
    )
    # Add basemap
    contextily.add_basemap(
        ax,
        source=contextily.providers.CartoDB.Positron
    )
    # Add colorbar
    plt.colorbar(hb)
    # Remove axes
    ax.set_axis_off()


def kernel_density_estimation(df):
    # Set up figure and axis
    f, ax = plt.subplots(1, figsize=(9, 9))
    # Generate and add KDE with a shading of 50 gradients
    # coloured contours, 75% of transparency,
    # and the reverse viridis colormap
    seaborn.kdeplot(
        df['x'],
        df['y'],
        n_levels=50,
        shade=True,
        alpha=0.55,
        cmap='viridis_r'
    )
    # Add basemap
    contextily.add_basemap(
        ax,
        source=contextily.providers.CartoDB.Positron
    )
    # Remove axes
    ax.set_axis_off()


if __name__ == '__main__':
    df = pandas.read_csv('../data/tokyo_clean.csv')

    scatter_plot(df)
    plt.savefig('scatter.png')
    scatter_plot_with_map(df)
    plt.savefig('scatter_map.png')
    hexbin(df)
    plt.savefig('hexbin.png')
    kernel_density_estimation(df)
    plt.savefig('kde.png')
    plt.show()
