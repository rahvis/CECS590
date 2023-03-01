import matplotlib.pyplot as plt
import configparser
#Loading config
config = configparser.ConfigParser()
config.read("UncertaintyQuantification/config.ini")
PLOTS_LOCATION = config["location"]["plots_location"]
EXTENSION= '.png'
class Visualize:
    def __init__(self):
        pass
    def plot_graph(self,X,Y,X_label,Y_label,Title):
        plt.loglog(X,Y)
        # naming the x-axis
        plt.xlabel(X_label)
        # naming the y-axis
        plt.ylabel(Y_label)
        # plot title
        plt.title(Title)
        # function to save the plot
        plt.savefig(PLOTS_LOCATION+Title+EXTENSION)
