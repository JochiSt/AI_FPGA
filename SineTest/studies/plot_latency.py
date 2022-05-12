
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

for clock_ns in clock:
    with open('report_%d.json'%(clock_ns)) as infile:
        data = json.load( infile )
        print(data)

        worst_latency = np.append(worst_latency, data['CSynthesisReport']['WorstLatency'])
        best_latency  = np.append(best_latency,  data['CSynthesisReport']['BestLatency'])
        est_clk       = np.append(est_clk,       data['CSynthesisReport']['EstimatedClockPeriod'])

        used_LUT      = np.append(used_LUT,      data['CSynthesisReport']['LUT'])
        used_DSP      = np.append(used_DSP,      data['CSynthesisReport']['DSP48E'])
        used_FF       = np.append(used_FF,       data['CSynthesisReport']['FF'])

worst_latency = worst_latency.astype(float) * clock
best_latency  = best_latency.astype(float) * clock

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()
#ax1.plot(clock, worst_latency, label='latency')
ax1.plot(clock, best_latency, '.-g', label='best latency')
ax2.plot(clock, clock - est_clk.astype(float), '.-b' ,label='des. clk - est. clk')

ax2.axhline(0, color='black')
#ax1.legend(loc='best')
fig.legend(loc="upper right", framealpha=1)

ax1.set_ylabel('latency / ns')
ax2.set_ylabel('design period - est. period / ns')
ax1.set_xlabel('designed clock period / ns')

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


