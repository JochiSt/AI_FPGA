
import json
import numpy as np
import matplotlib.pyplot as plt

clock = np.array([24,20,18,16,14,12,10,8,6,4,2], dtype=float)
latency = np.array([])

worst_latency = np.array([])
best_latency  = np.array([])
est_clk       = np.array([])

used_LUT      = np.array([])
used_FF       = np.array([])
used_DSP      = np.array([])

interval_min  = np.array([])
interval_max  = np.array([])

for clock_ns in clock:
    with open('report_%d.json'%(clock_ns)) as infile:
        data = json.load( infile )
        print(data)

        worst_latency = np.append(worst_latency, data['CSynthesisReport']['WorstLatency'])
        best_latency  = np.append(best_latency,  data['CSynthesisReport']['BestLatency'])
        est_clk       = np.append(est_clk,       data['CSynthesisReport']['EstimatedClockPeriod'])

        interval_min  = np.append(interval_min,  data['CSynthesisReport']['IntervalMin'])
        interval_max  = np.append(interval_max,  data['CSynthesisReport']['IntervalMax'])

        used_LUT      = np.append(used_LUT,      data['CSynthesisReport']['LUT'])
        used_DSP      = np.append(used_DSP,      data['CSynthesisReport']['DSP48E'])
        used_FF       = np.append(used_FF,       data['CSynthesisReport']['FF'])

worst_latency = worst_latency.astype(float) * clock
best_latency  = best_latency.astype(float) * clock

fig, ax1 = plt.subplots(figsize=(8, 6))

################################################################################

ax1.plot(clock, best_latency,  '^-g', label='best latency')
ax1.plot(clock, worst_latency, 'v-g', label='worst latency')

ax1.set_ylabel('latency / ns')
ax1.set_xlabel('designed clock period / ns')
for label in ax1.get_yticklabels():
    label.set_color('g')
ax1.yaxis.label.set_color('g')

################################################################################
# from https://stackoverflow.com/a/31808931
ax2 = ax1.twiny()

# Add some extra space for the second axis at the bottom
fig.subplots_adjust(bottom=0.2)

# Move twinned axis ticks and label from top to bottom
ax2.xaxis.set_ticks_position("bottom")
ax2.xaxis.set_label_position("bottom")

# Offset the twin axis below the host
ax2.spines["bottom"].set_position(("axes", -0.15))

# Turn on the frame for the twin axis, but then hide all 
# but the bottom spine
ax2.set_frame_on(True)
ax2.patch.set_visible(False)

# as @ali14 pointed out, for python3, use this
# for sp in ax2.spines.values():
# and for python2, use this
for sp in ax2.spines.values():
    sp.set_visible(False)
ax2.spines["bottom"].set_visible(True)

ax2.set_xlabel("Clock / MHz")
ax1Ticks = ax1.get_xticks()   
ax2Ticks = ax1Ticks

def tick_function(X):
    X = X * 1e-9    # convert ns into s
    F = 1./X        # turn into frequency
    F = F * 1e-6     # convert into MHz
    return ["%.2f" % z for z in V]

ax2.set_xticks(ax2Ticks)
ax2.set_xbound(ax1.get_xbound())
ax2.set_xticklabels(tick_function(ax2Ticks))

################################################################################

ax2 = ax1.twinx()
ax2.plot(clock, clock - est_clk.astype(float), '.-b' ,label='des. clk - est. clk')
ax2.axhline(0, color='black')
for label in ax2.get_yticklabels():
    label.set_color('b')
ax2.yaxis.label.set_color('b')
ax2.set_ylabel('design period - est. period / ns')

ax3 = ax1.twinx()
ax3.spines.right.set_position(("axes", 1.15))
ax3.plot(clock, interval_min, 'v-r' ,label='min. initiation interval')
ax3.plot(clock, interval_max, '^-r' ,label='max. initiation interval')
for label in ax3.get_yticklabels():
    label.set_color('r')
ax3.yaxis.label.set_color('r')
ax3.set_ylabel('initiation interval / clk cycles')

fig.legend(loc="upper right", framealpha=1)

plt.title('Latency estimation vs. clock')
plt.tight_layout()
plt.savefig("Latency.png")
plt.show()

###############################################################################

fig, ax1 = plt.subplots()

ax1.plot(clock, used_LUT.astype(float), '.-', label='used LUTs')
ax1.plot(clock, used_DSP.astype(float), '.-', label='used DSPs')
ax1.plot(clock, used_FF.astype(float) , '.-', label='used FFs')

fig.legend(loc="upper right", framealpha=1)

ax1.set_yscale('log')
ax1.set_ylabel('used instances')
ax1.set_xlabel('designed clock period / ns')

plt.title('Used instances vs. clock')
plt.tight_layout()
plt.savefig('UsedInstances.png')
plt.show()


