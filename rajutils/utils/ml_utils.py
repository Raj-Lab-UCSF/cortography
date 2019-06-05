import itertools
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def plot_confusion_matrix(cm, classes,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues,
                          save=False,
                          save_name='cm'):

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()
    if save == True:
        plt.savefig('../images/'+str(save_name)+'.pdf', format='pdf')


def calculate_group_distributions(labels_dict, true_labels, num_clusters):
    """
    Calculate distribution of true labels (e.g. G1,G2,G3) in each cluster in labels_dict
    labels_dict (dict): indices of individuals in each cluster
    true_labels (list): list of labels for each individual
    num_clusters (int): number of clusters in labels_dict
    """


    patients_by_cluster = {k: {'c'+str(c): np.where(labels_dict[k]==c)[0] \
                            for c in range(num_clusters)} \
                            for k in labels_dict.keys()}

    group_dist = {}
    for var in patients_by_cluster.keys():
        #var = 'apib', 'atrophy', tau
        cluster_tally = {}
        for cluster, patients in patients_by_cluster[var].items(): #loop over clusters
            cluster_dist = []
            for patient in patients:
                patient_group = true_labels[patient]
                cluster_dist.append(patient_group)
            tally = np.unique(np.array(cluster_dist), return_counts=True)
            cluster_tally.update({cluster:tally})

        group_dist.update({var:cluster_tally})


    def make_plot_ready_distributions(group_dist):
        """
        transform a 'unique' type array (e.g. (array([2,3]), array([1,6])))
        into a count of fixed length (e.g. [0,1,6])
        """
        dist = {}
        for var in group_dist.keys(): #loop over variables (apib, atrophy, tau)
            cluster_dist = {}
            for cluster, unique_dist in group_dist[var].items(): #loop over clusters
                dist_in_cluster = []
                for group in range(3): #loop over the 3 groups
                    #find where the group is represented in the cluster
                    location_group_G_in_cluster = np.where(unique_dist[0] == group)[0]

                    if location_group_G_in_cluster.size == 0: #if group not represented, add 0
                        dist_in_cluster.append(0)
                    else:
                        num_groups_g_in_cluster = unique_dist[1][location_group_G_in_cluster][0]
                        dist_in_cluster.append(num_groups_g_in_cluster)
                cluster_dist.update({cluster:dist_in_cluster})
            dist.update({var:cluster_dist})
        return(dist)

    return(make_plot_ready_distributions(group_dist))

def plot_all_classes_dist(labels_dict, true_labels, num_clusters, save=False, save_name="temp"):
    distributions = calculate_group_distributions(labels_dict, true_labels, num_clusters)

    NUM_VARS = 3 #apib, atrophy, tau
    NUM_GROUPS = 3 #G1, G2, G3

    fig_dim = (20,20)
    fig, axes = plt.subplots(NUM_VARS, num_clusters, figsize=fig_dim)
    xticks = np.arange(NUM_GROUPS)
    ax = axes.ravel()
    p = 0

    for var in labels_dict.keys():
        var_dist = distributions[var]

        ticks = [40]*num_clusters
        for g_count, group in enumerate(var_dist.keys()):
            dist = var_dist[group]

            ax[p].bar(xticks, dist, color=['red','green','blue'])
            ax[p].set_xticks(xticks)
            ax[p].set_yticks(range(0, ticks[g_count],4))

            ax[p].set_xticklabels(['G-1', 'G-2', 'G-3'])
            ax[p].set_xlabel('Spectral Clusters')
            ax[p].set_ylabel('Number of members in class')
            ax[p].set_title(str(var)+'  '+str(group))
            p += 1
    if save == True:
        fig.savefig('../images/'+str(save_name)+'.pdf', format='pdf')
    plt.show()

def make_cm_from_group_dist(group_dist_dict, num_classes):
    """
    Given a group distribution for a class
    e.g. {{'c0': [5, 14, 14], 'c1': [12, 2, 12], 'c2': [1, 1, 24]}}
    redistribute them as G1', G2', G3' according to the majority
    """
    import pandas as pd

    cm_dic = {}
    for var in group_dist_dict.keys():

        confusion_matrix = []
        #turn dict into pandas DataFrame
        df = pd.DataFrame(group_dist_dict[var])
        #find max value for each row (true label) and assign it as new label
        for n in reversed(range(num_classes)):
            old_class = df.iloc[n].idxmax() #calculate max
            new_class = list(df[old_class])
            confusion_matrix.insert(0,new_class) #append to confusion matrix
            df = df.drop(old_class, axis=1) #remove this column from df
        cm = np.transpose(np.array(confusion_matrix))
        cm_dic.update({var:cm})

    return(cm_dic)

def plot_confusion_matrix(cm,
                          class_names,
                          title = ["APIB", "Atrophy", "Tau"],
                          cmap = plt.cm.Reds,
                          save=False,
                          save_name='cm'):




    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Reds)

    plt.title(title, fontsize=24)
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, labels=class_names)
    plt.yticks(tick_marks, labels=class_names)

    fmt = 'd'
    thresh = cm.max() / 2.
    for ii, jj in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(jj, ii, format(cm[ii, jj], fmt),
                   fontsize=24,
                   verticalalignment="center",
                   horizontalalignment="center",
                   color="white" if cm[ii, jj] > thresh else "black")


    plt.tight_layout()

def plot_confusion_matrices(cm_dic,
                            class_names,
                            title = ["APIB", "Atrophy", "Tau"],
                            cmap = [plt.cm.Reds, plt.cm.Blues, plt.cm.Greens],
                            save=False,
                            save_name='cm'):



    NUM_GROUPS = len(cm_dic.keys())
    fig_dim = (20,10)
    fig, axes = plt.subplots(1, NUM_GROUPS, figsize=fig_dim)
    ax = axes.ravel()

    for i, k in enumerate(cm_dic.keys()):
        cm = cm_dic[k]
        ax[i].tick_params(labelsize = 24)

        ax[i].imshow(cm, interpolation='nearest', cmap=cmap[i])

        ax[i].set_title(title[i], fontsize=24)
        # ax[i].set_colorbar()
        tick_marks = np.arange(len(class_names))
        ax[i].set_xticklabels(class_names, rotation=45)
        ax[i].set_xticks(tick_marks)
        ax[i].set_yticklabels(class_names)
        ax[i].set_yticks(tick_marks)

        fmt = 'd'
        thresh = cm.max() / 2.
        for ii, jj in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
            ax[i].text(jj, ii, format(cm[ii, jj], fmt),
                       fontsize=24,
                       verticalalignment="center",
                       horizontalalignment="center",
                       color="white" if cm[ii, jj] > thresh else "black")

        # ax[i].set_ylabel('True label')
        # ax[i].set_xlabel('Predicted label')
    plt.tight_layout()

    if save == True:
        plt.savefig('../images/truth_tables/'+str(save_name)+'.png',
                    format='png',
                    transparent=True)



####
cm_dic = {'1': np.array([[ 0, 14,  4],[ 0,  7, 10],[ 6, 20, 24]]),
          '2': np.array([[ 0, 14,  4],[ 0,  7, 10],[ 6, 20, 24]]),
          '3': np.array([[ 0, 14,  4],[ 0,  7, 10],[ 6, 20, 24]])}



# calculate_accuracy(cm_dic):
#     accuracy_dic = {}
#     for i, k in enumerate(cm_dic.keys()):
#         cm = cm_dic[k]
#
#         for j in




#
