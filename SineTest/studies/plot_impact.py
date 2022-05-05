
import numpy as np
import matplotlib.pyplot as plt

stimulus = np.array([])
ANN_raw = np.array([])

with open('post_quant_train.dat') as f:
    lines = f.readlines()
    for line in lines:
        try:
            stim, raw = line.split(' ')
            stimulus  = np.append( stimulus,  float(stim) )
            ANN_raw = np.append( ANN_raw, int(raw, 16) )
        except:
            pass

fig, ax1 = plt.subplots()

x = np.arange(0, len(quantisations[1:]))
#ax1.plot( x, distances[1:], '.-', label='Mean Absolute Distance')
ax1.errorbar( x, mean_distances[1:], yerr=sigma_distances[1:],
                                        label='Mean Absolute Distance')

# plot the comparison to keras
ax1.axhline(y=mean_distances[0] + sigma_distances[0], color='r',
                                                linestyle='-', label="Keras")
ax1.axhline(y=mean_distances[0] , color='r', linestyle='-', label="Keras")
ax1.axhline(y=mean_distances[0] + sigma_distances[0], color='r',
                                                linestyle='-', label="Keras")

# Set number of ticks for x-axis
ax1.set_xticks(x)
# Set ticks labels for x-axis
ax1.set_xticklabels( quantisations[1:], fontsize=11, rotation = 90)
ax1.set_ylabel('Mean Absolute Difference')

ax1.set_yscale('log')
ax1.legend(loc='best')

plt.title('Impact of Post Training Quantisation HLS4ML')
plt.tight_layout()
plt.savefig("PostQuantEffect.png")
plt.show()
